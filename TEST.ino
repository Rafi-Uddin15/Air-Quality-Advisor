#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.println("timestamp_ms,temperature_c,humidity_pct,mq135_raw");
}

void loop() {
  unsigned long t_ms = millis();

  float h = dht.readHumidity();
  float temp = dht.readTemperature(); // Celsius
  int mq = analogRead(A0);            // 0–1023

  if (isnan(h) || isnan(temp)) {
    return;  // skip if DHT fails
  }

  Serial.print(t_ms);
  Serial.print(",");
  Serial.print(temp, 2);
  Serial.print(",");
  Serial.print(h, 2);
  Serial.print(",");
  Serial.println(mq);

  delay(2000); // every 2 s
}
