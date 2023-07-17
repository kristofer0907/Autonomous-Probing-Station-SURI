#include <SoftwareSerial.h>

SoftwareSerial BT(8, 9); // RX, TX

void setup() {
  Serial.begin(9600);
  BT.begin(9600);

  Serial.println("Enter a number (1, 2, or 3) to get a phrase:");
}

void loop() {
  if (Serial.available()) {
    int number = Serial.parseInt();

    if (number == 1) {
      BT.println("You entered 1: Hello!");
      Serial.println("Sent phrase: Hello!");
    } else if (number == 2) {
      BT.println("You entered 2: How are you?");
      Serial.println("Sent phrase: How are you?");
    } else if (number == 3) {
      BT.println("You entered 3: Goodbye!");
      Serial.println("Sent phrase: Goodbye!");
    } else {
      BT.println("Invalid number. Please enter 1, 2, or 3.");
      Serial.println("Invalid number entered.");
    }
  }

  if (BT.available()) {
    Serial.write(BT.read());
  }
}
