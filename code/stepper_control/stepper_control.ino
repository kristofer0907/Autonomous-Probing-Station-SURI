#include <Stepper.h>
/*Example sketch to control a stepper motor with A4988 stepper motor driver and Arduino without a library. More info: https://www.makerguides.com */

// Define stepper motor connections and steps per revolution:
#define dirPin 5
#define stepPin 4
#define dirPin2 13
#define stepPin2 12
#define stepsPerRevolution 200

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
}

void loop() {
  digitalWrite(dirPin, HIGH);
  for (int i = 0; i < 8000; i++) 
  {
  Serial.println("This is y axis ");
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(50);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(1000);
  }
  
  digitalWrite(dirPin2, LOW);
  for (int i = 0; i < 1000; i++) 
  {
  Serial.println("This is x-axis");
  digitalWrite(stepPin2, HIGH);
  delayMicroseconds(50);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(1000);
  }
  delay(5);
  digitalWrite(dirPin2, HIGH);
  for (int i = 0; i < 1000; i++) 
  {
  Serial.println("This is x-axis again");

  digitalWrite(stepPin2, HIGH);
  delayMicroseconds(50);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(1000);
  }
}
