#include <Arduino.h>
#include <Servo.h>

int trig = 9;
int echo = 10;
int servoPIN = 11;
int angle = 0;
bool forward = true;
Servo servo;

void setup() {
  Serial.begin(115200);
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
  servo.attach(servoPIN);
  servo.write(angle);
}

void loop() {
  if (forward){
    angle += 1;
    if (angle >= 180){
      forward = false;
    }
    servo.write(angle);
  }
  else if (forward == false)
  {
    angle -= 1;
    if (angle <= 0){
      forward = true;
    }
    servo.write(angle);
  }

  digitalWrite(trig, LOW);
  delayMicroseconds(2);

  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  unsigned long duration = pulseIn(echo, HIGH, 30000);
  int distance = duration * 0.0343 / 2.0;
  
  Serial.print(distance);
  Serial.print(",");
  Serial.println(angle);

  delay(60);
}
