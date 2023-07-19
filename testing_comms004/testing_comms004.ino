#define dirPin 5
#define stepPin 4
#define dirPin2 13
#define stepPin2 12
#define stepsPerRevolution 400

char data = '0'; // Initialize data to '0'

void setup() {
  Serial.begin(9600);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
}

void loop() {
  while (Serial.available()) {
    data = Serial.read();
  }

  // Only execute an action when a valid command is received
  if (data == '1') {
    Serial.println("Motor 1");
    delay(1000);
    digitalWrite(dirPin, HIGH);
    for (int i = 0; i < 8000; i++) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(50);
      digitalWrite(stepPin, LOW);
    }
    Serial.println("Finished number 1");
    delay(1000);
    data = '0'; // Reset data to '0' after the action is completed
  } else if (data == '2') {
    Serial.println("Now in number 2");
    digitalWrite(dirPin2, LOW);
    while (data != 'S') {
      data = Serial.read();
      digitalWrite(stepPin2, HIGH);
      delayMicroseconds(200);
      digitalWrite(stepPin2, LOW);
      data = '0';
    }
    Serial.println("Finished number 2");
    delay(1000);
    data = '0'; // Reset data to '0' after the action is completed
  } else if (data == '3') {
    Serial.println("Now in number 3");
    digitalWrite(dirPin2, HIGH);
    while (data != 'S') {
      data = Serial.read();
      digitalWrite(stepPin2, HIGH);
      delayMicroseconds(200);
      digitalWrite(stepPin2, LOW);
    }
    Serial.println("Finished number");
    delay(1000);
    data = '0';
  } else if (data == '4') { // Go down for measurement
    digitalWrite(dirPin2, LOW);
    for (int i = 0; i < 2000; i++) {
      digitalWrite(stepPin2, HIGH);
      delayMicroseconds(50);
      digitalWrite(stepPin2, LOW);
      delayMicroseconds(1000);
    }
    delay(1000);
    data = '0';
  } else if (data == '5') { // Go up for measurement
    digitalWrite(dirPin2, HIGH);
    for (int i = 0; i < 2000; i++) {
      digitalWrite(stepPin2, HIGH);
      delayMicroseconds(50);
      digitalWrite(stepPin2, LOW);
      delayMicroseconds(100);
    }
    delay(1000);
    data = '0';
  }
}
