#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 10
#define DHTTYPE DHT22
DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(8, OUTPUT);
  pinMode(11, OUTPUT);
  digitalWrite(8, LOW);
  digitalWrite(11, HIGH);
}

void loop() {
  delay(1000);
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("T_E"));
  }
  else {
    Serial.print(F("T_"));
    Serial.print(event.temperature);
    Serial.println();
    Serial.println();
  }
}
