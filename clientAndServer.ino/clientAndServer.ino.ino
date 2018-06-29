
//TODO 

/* 
 * IFF Theres multiple arduino client use cases where arduino needs the response 
 * Need to make some sort of function that you give a route too and an optional json object, and it gives you back a json object which was the response
 * of the request. That way we can keep all the ethernet junk out of the ethernet object
 * 
 * 
 * 
 * 
 * 
 * 
 */



#include <TimeLib.h>
#include <Time.h>
#include <DHT.h>



#include <ArduinoJson.h>
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED }; //physical mac address
IPAddress ip(192,168,0,2); // ip in lan
IPAddress gateway(192,168,0,1); // internet access via router
IPAddress subnet(255,255,255,0); //subnet mask
IPAddress myserver(99,253,59,150); // zoomkat web page
EthernetServer server(80); //server port
EthernetClient client;
String readString; 

//// GLOBALS ////

//Light Scheduel Times  [start hr, stop hr]//
  int tankLightsTimes[2] = { 10, 20 };
  int tankLedLightsTimes[2] = {20 , 23 };
  int growLightsTimes[2] = { 9 , 23 };

//RGB LED values
  int rgbLedLightValues[]={ 255 , 255 , 255};

//Manual Lights
  int tankLightsManualOn = 2;
  int growLightsManualOn = 2;
  int tankLedLightsManualOn = 2;

//Pinout

#define growLightsPin A2
#define tankLedLightsPin 7
#define tankLightPin 8


#define TOPMOISTURE 5 //analog
#define TOPMOISTUREPWR 5

#define lightSensorPin 4 //analog
#define DHTPIN 2 
#define DHTTYPE DHT11 

#define ACMOTOR A0
#define DCMOTOR A1


#define ERRORLED 10


unsigned long waterInStartTime;
unsigned long waterInRunTime;
bool cycling = true;
double threshold = 510;
double drainTime = 23000;
unsigned long errorTime = 180000;
unsigned long dryTime = 30000;
unsigned double dcPulseTime = 500;
//// END GLOBALS ////


  
DHT dht(DHTPIN, DHTTYPE);
  
  
  void setup(){

  //Motors
  pinMode(ACMOTOR, OUTPUT);
  pinMode(DCMOTOR, OUTPUT);
  pinMode(tankLightPin, OUTPUT);
  pinMode(growLightsPin, OUTPUT);
  pinMode(tankLedLightsPin, OUTPUT);

  //Moisture Sensors
  pinMode(TOPMOISTURE, INPUT);
  pinMode(TOPMOISTUREPWR, OUTPUT);

  digitalWrite(ACMOTOR,LOW);
  digitalWrite(DCMOTOR,LOW);
  digitalWrite(tankLightPin,LOW);
  digitalWrite(tankLedLightsPin,LOW);
  
  
  //Ethernet
  Ethernet.begin(mac, ip, subnet, gateway);
  delay(2000); 
  Serial.begin(9600); 
  getTimeFromServer();
  getConfiguration();
  server.begin();
    
  }



  
  void loop() {   
    checkForEthernetRequest();
    checkLightSchedule();
    if(cycling){
      cycle();
    }
    sendData("data", readSensors() , false );    
  }



  void cycle() {
      int topMoistureVal = getMoistureReading(TOPMOISTURE , TOPMOISTUREPWR );
      if( topMoistureVal > threshold ){
      waterIntoGrowBed();
      } 
  }




  void waterIntoGrowBed(){
        pulseWaterOut();
        digitalWrite(DCMOTOR, LOW);
        digitalWrite(ACMOTOR, HIGH);
        waterInStartTime = millis();
        
        int topMoistureVal = getMoistureReading(TOPMOISTURE , TOPMOISTUREPWR );
        unsigned long StartTime = millis();
      
      
        while( topMoistureVal > threshold ){
            checkForEthernetRequest();
            digitalWrite(ACMOTOR, HIGH);
            topMoistureVal = getMoistureReading(TOPMOISTURE , TOPMOISTUREPWR );
            unsigned long CurrentTime = millis();
            waterInRunTime = CurrentTime - StartTime;  
      
            if(waterInRunTime > errorTime){
                digitalWrite(ACMOTOR, LOW);
                waterOutofBed();
                errorState();
                return;
            }
        }
       digitalWrite(ACMOTOR, LOW);
       waterOutofBed();
  }

  void pulseWaterOut(){
    digitalWrite(DCMOTOR, HIGH);
    delay(dcPulseTime);
    digitalWrite(DCMOTOR,LOW);
    return;   
    }




  void waterOutofBed(){
      Serial.println("Water Out");
      digitalWrite(DCMOTOR, HIGH);
      digitalWrite(ACMOTOR, LOW );
      delayWithEthernet(drainTime);
      digitalWrite(DCMOTOR, LOW);
      delayWithEthernet(dryTime);
  }




 void delayWithEthernet(unsigned long delayTime){
      unsigned long StartTime = millis();
      unsigned long CurrentTime = millis();
      unsigned long ElapsedTime = CurrentTime - StartTime;
      while(ElapsedTime < delayTime ){
           delay(1000);
           CurrentTime = millis();
           ElapsedTime = CurrentTime - StartTime;
           checkForEthernetRequest();          
      }
     return;   
  }

    
  void errorState(){
    Serial.println("Error State");  
    cycling = false;
    }
    


  int getMoistureReading(int readPin , int powerPin ){
      //Turn Sensor On
      digitalWrite(powerPin, HIGH);    
      delay(400);
      //Get sensor value
      int data = analogRead(readPin);
      //Turn Sensor Off
      digitalWrite(powerPin, LOW);
      return data;  
  }




  
  JsonObject& readSensors(){
      DynamicJsonBuffer jsonBuffer(200);
      JsonObject& data = jsonBuffer.createObject();
      data["light"] = analogRead(lightSensorPin);
      data["temperature"] = dht.readTemperature();
      data["humidity"] = dht.readHumidity();
      delay(600);
      if(cycling){
          data["waterInRunTime"] = waterInRunTime;
          data["threshold"] = threshold;
          data["dryTime"] = dryTime;
          data["drainTime"] = drainTime;
          data["errorTime"] = errorTime;
      }
      return data;    
  }


   
  void checkLightSchedule(){
    
    //Tank Lights
    time_t current = now();
    if( ( hour(current) >= tankLightsTimes[0] ) && ( hour(current) < tankLightsTimes[1]   ) ){
      tankLights(true);  
    }
    else{
      tankLights(false);
    }
  
    //LED Lights
    if( ( hour(current) >= tankLedLightsTimes[0] ) && ( hour(current) < tankLedLightsTimes[1]   ) ){
      tankLedLights(true);  
    }
    else{
      tankLedLights(false);
    }

    //GrowLights
    if( ( hour(current) >= growLightsTimes[0] ) && ( hour(current) < growLightsTimes[1] ) ){
      growLights(true);  
    }
    else{
      growLights(false);
    }

  }



  
  void checkForEthernetRequest(){


    
    EthernetClient client = server.available();
    if (client) {
       digitalWrite(ACMOTOR, LOW);
       digitalWrite(DCMOTOR, LOW);
      while (client.connected()) {
        if (client.available()) {
              char endOfHeaders[] = "\r\n\r\n";
              if (!client.find(endOfHeaders)) {
                Serial.println(F("Invalid response"));
              }
              // Allocate JsonBuffer
              DynamicJsonBuffer jsonBuffer(200);
              // Parse JSON object
              JsonObject& root = jsonBuffer.parseObject(client);
              if (!root.success()) {
                Serial.println(F("Parsing failed!"));
                  //Send Error      
                client.println("HTTP/1.0 200 OK");
                client.println("Content-Type: text/html");
                client.println();
                client.println("<HTML><BODY>Parsing Failed");
                //stop client
                client.stop();    
              }
              else{ 
                //Send Success Response      
                client.println("HTTP/1.0 200 OK");
                client.println("Content-Type: text/html");
                client.println();
                client.println("<HTML><BODY>Success");
                //stop client
                client.stop();
                delay(500);
                readRequest(root);
             }
              
          }
        }
    }
  }
  
  /**   SYNC TIME
   *  
   * Syncs arduino time with server time accurate to the min
   * 
   */
  void getConfiguration(){
      bool done = true;
      //Connect to server
      if (client.connect(myserver, 80)) {
          Serial.println("connected");
          client.print("GET /API/getConfiguration");
          client.println(" HTTP/1.1");
          client.println("Connection: close");
          client.println();
      } 
      else {
        Serial.println("connection failed");
        Serial.println();
        done = false;
      }
      //waitForResponse
      delay(1000);
      char endOfHeaders[] = "\r\n\r\n";
      if (!client.find(endOfHeaders)) {
        Serial.println(F("Invalid response"));
      }
      DynamicJsonBuffer jsonBuffer(200);
      // Parse JSON Response
      JsonObject& reply = jsonBuffer.parseObject(client);
      
      reply.prettyPrintTo(Serial);
    
      client.stop();

      if(!done){
        getTimeFromServer();
      }
  
      setTime(reply["hour"],reply["minute"],0,reply["day"],reply["month"],2018);
      adjustCycleSettings(reply);
      
      return;
  }



  
  /** SEND DATA
   *  Give a destination, and json object and weather or not 
   *  you expect a response. If you do expect a response, a json
   *  object will be returned
   */
  JsonObject&  sendData(String destination , JsonObject& root, bool getResponse){
        
        if (client.connect(myserver, 80)) {
            Serial.println("connected");
            client.print("POST /API/");
            client.print(destination);
            client.println(" HTTP/1.1");
            client.println("User-Agent: Arduino");
            client.println("Connection: close");
            client.println("Content-Type: application/json;");
            client.print("Content-Length: ");
            client.println(root.measureLength());
            client.println();
            root.printTo(client);
        } 
        else {
          Serial.println("connection failed");
          Serial.println();
        }
  
        if(getResponse){
            //waitForResponse
            delay(1000);
            char endOfHeaders[] = "\r\n\r\n";
            if (!client.find(endOfHeaders)) {
              Serial.println(F("Invalid response"));
            }
            DynamicJsonBuffer jsonBuffer(200);          
           // Parse JSON Response
            JsonObject& reply = jsonBuffer.parseObject(client);
            client.stop();
            return reply;
       
        }
        else{
            client.stop();
            return root;
        }
  
        
  
        
  }
  
  
  
  
  /**   ROUTES
   * 
   * 
   * JSON packets from the server come with a "command" parameter. This value dictates its intent and how the rest of the packet is to be
   * interpreted
   */
  void readRequest(JsonObject& root){
    
    root.prettyPrintTo(Serial);
    String command = root["command"];
    
    if( command == "LED"){
      sendData("LEDSwitch", root, false);
    }
    else if( command == "toggleCycling"){
      toggleCycling(root);    
    }
    else if( command =="cycleSettings"){
      adjustCycleSettings(root);
    }
    else if( command == "ChangeLightCycleTime"){
      updateLightSchedule(root);
    }
    else if ( command == "manualLightSwitch"){
     manualLightSwitch(root);
    }
    else if (command == "LightOn"){
      
    }
  }

  void adjustCycleSettings(JsonObject& root){
      
      double givenThreshold  = root["threshold"];
      if(givenThreshold){
        if(givenThreshold > 200 && givenThreshold < 600 ){
          threshold = givenThreshold;
        }      
      }
      double givenDrainTime = root["drainTime"]; 
      if(givenDrainTime){
        drainTime = givenDrainTime;
      }
      double givenErrorTime = root["errorTime"];
      if(givenErrorTime){
        errorTime = givenErrorTime;
      }
      double givenDryTime = root["dryTime"];
      if(givenDryTime){
        dryTime = givenDryTime;
      }
      double givenDcPulse = root["dcPulse"];
      if(givenDcPulse){
        dcPulseTime = givenDcPulse;
       }
      
     return;
        
  }

  void toggleCycling(JsonObject& root){
    
    int state = root["state"];
    if (state == 0){
      cycling = false;
    }
    else{
      cycling = true;
    }
  }


  void manualLightSwitch(JsonObject& root){
     String light = root["light"];
     int state = root["state"];      
     if(light == "tankLights" ){
        tankLightsManualOn = state;
     }
     else if(light == "tankLedLights"){
        tankLedLightsManualOn = state;
     }
     else if(light == "growLights"){
        growLightsManualOn = state;  
     }
     checkLightSchedule();      
  }


  

  //TODO update multiple lights at once using nested json strucure which has an update flag  
  void updateLightSchedule(JsonObject& root){
    
    int startHour = root["startHour"];
    int stopHour = root["stopHour"];

    String light = root["light"];

    if(light == "tankLights" ){
      tankLightsTimes[0] = startHour;
      tankLightsTimes[1] = stopHour ;
    }

    else if(light == "tankLedLights"){
      tankLedLightsTimes[0] = startHour;
      tankLedLightsTimes[1] = stopHour;
    }

    else if(light == "growLights"){
      growLightsTimes[0] = startHour;
      growLightsTimes[1] = stopHour;
    
    }
   checkLightSchedule;  
 }



    
  void tankLights(bool state){
    
    if(tankLightsManualOn==1){
      digitalWrite(tankLightPin, HIGH);
    }
    else if(tankLightsManualOn==0){
      digitalWrite(tankLightPin, LOW);
    }
    else if(state){
      digitalWrite(tankLightPin, HIGH);
    }
    else if(!state){
      digitalWrite(tankLightPin, LOW);
    }

  }



  void tankLedLights(bool state){
    
    if(tankLedLightsManualOn==1){
      digitalWrite(tankLedLightsPin, HIGH);
    }
    else if(tankLedLightsManualOn==0){
      digitalWrite(tankLedLightsPin, LOW);
    }
    else if(state){
      digitalWrite(tankLedLightsPin, HIGH);
    }
    else if(!state){
      digitalWrite(tankLedLightsPin, LOW);
    }
  }



  void growLights(bool state){
        
    if(growLightsManualOn==1){
      digitalWrite(growLightsPin, HIGH);
    }
    else if(growLightsManualOn==0){
      digitalWrite(growLightsPin, LOW);
    }
    else if(state){
      digitalWrite(growLightsPin, HIGH);
    }
    else if(!state){
      digitalWrite(growLightsPin, LOW);
    }
  }

    
 
  
  





