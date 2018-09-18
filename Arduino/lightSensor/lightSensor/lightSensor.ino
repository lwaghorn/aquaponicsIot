
#define lightSensorPin 4


void setup() {
  Serial.begin(9600); 
  pinMode(lightSensorPin, INPUT);
}

void loop() {
  
 Serial.println(readLightSensor());
 delay(1000);
}

int readLightSensor(){
  int total = 0;
  int samples = 20;
  for(int i = 0 ; i<20 ; i++){
      int val = analogRead(lightSensorPin);
      if(val == 0){
        samples--;
      }
      else{
        total += val;
      }
      delay(200);
  }
  if(samples > 0){
    return total/samples;
  }
  else{
    return 0;
  }
  }
