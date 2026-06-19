#include <WiFi.h>

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  Serial.println();
  // Serial.println("ESP32 MAC Address: ");
  Serial.println(WiFi.macAddress());


}

void loop() {
  // put your main code here, to run repeatedly:

}
