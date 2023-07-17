#include <SoftwareSerial.h>
SoftwareSerial HC06(8, 9); // HC06-TX Pin 8, HC06-RX to Arduino Pin 9

void setup() {
  Serial.begin(9600);     // Start the Serial Monitor for debugging
  HC06.begin(9600);       // Baudrate 9600, choose your own baudrate
}

void loop() {
  if (HC06.available() > 0) {
    char receive = HC06.read(); // Read from Serial Communication
    Serial.print("Received: ");
    Serial.println(receive);
    if (receive == '1') {
      String data = "Hey there";
      HC06.println(data);
      Serial.println("Sent: Hey there");
      delay(100); // Add a small delay to ensure data is transmitted
    }
    else {
      HC06.println("Bye there");
      Serial.println("Sent: Bye there");
      delay(100); // Add a small delay to ensure data is transmitted
    }
  }
  else {
    Serial.println("Nothing transmitted");
    delay(200);
  }
}
