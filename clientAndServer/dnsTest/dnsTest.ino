
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
IPAddress dnServer(192,168,0,1);
IPAddress ip(192,168,0,2); // ip in lan
IPAddress gateway(192,168,0,1); // internet access via router
IPAddress subnet(255,255,255,0); //subnet mask
char myserver[] = "http://www.aquaponicsiot.sdhwcyirgh.ca-central-1.elasticbeanstalk.com";

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
double dcPulseTime = 500;
unsigned long dataDelayStartTime;
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
  Ethernet.begin(mac, ip, dnServer ,gateway, subnet);
  delay(2000); 
  Serial.begin(9600); 
  server.begin();
  dataDelayStartTime = millis();  
  }



  
  void loop() {
    
    if (client.connect(myserver, 80)) {
     Serial.println("connected");
     // Make a HTTP request:
     client.println("GET /API/getConfiguration HTTP/1.0");
     client.println();
    } 
    else {
     // if you didn't get a connection to the server:
     Serial.println("connection failed");
    }


   // if the server's disconnected, stop the client:
   if (!client.connected()) {
     Serial.println();
     Serial.println("disconnecting.");
     client.stop();
     // do nothing forevermore:
     while(true);
   }
   
      
  }


  





