#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 3     // Digital pin connected to the DHT sensor 
#define LEDLPIN 11    // Degital pin connected to the LED notifying the light
#define LEDHPIN 12    // Degital pin connected to the LED notifying the humidity
#define LEDTPIN 13    // Degital pin connected to the LED notifying the temperature

#define DHTTYPE    DHT11     // DHT 11

DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;

void setup() {
  Serial.begin(9600);
  // Initialize device.
  dht.begin();
  Serial.println(F("DHT11 Unified Sensor Example"));
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));
  // Set delay between sensor readings based on sensor details.
  delayMS = sensor.min_delay / 1000;

  pinMode(LEDLPIN,  OUTPUT);
  pinMode(LEDHPIN, OUTPUT);
  pinMode(LEDTPIN, OUTPUT);
}

void loop() {
  // Delay between measurements.
  delay(delayMS);

  int value = analogRead(A0);

  Serial.println("Analog  Value: ");
  Serial.println(value);
    
  if (value < 80) {
      digitalWrite(LEDLPIN, HIGH);
      Serial.println("LIGHT LEAK!");
  } else {
      digitalWrite(LEDLPIN,  LOW);
  }

  // Get temperature event and print its value.
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  }
  else {
    Serial.print(F("Temperature: "));
    Serial.print(event.temperature);
    Serial.println(F("°C"));

    if (event.temperature < 15) {
      digitalWrite(LEDTPIN, HIGH);
      Serial.println("TOO COLD!");
    } else if (event.temperature > 30) {
      digitalWrite(LEDTPIN, HIGH);
      Serial.println("TOO HOT!");
    }
    else {
      digitalWrite(LEDTPIN,  LOW);
    }
  }
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  }
  else {
    Serial.print(F("Humidity: "));
    Serial.print(event.relative_humidity);
    Serial.println(F("%"));

    if (event.relative_humidity < 30) {
      digitalWrite(LEDHPIN, HIGH);
      Serial.println("TOO DRY!");
    } 
    else if (event.relative_humidity > 50) {
      digitalWrite(LEDHPIN, HIGH);
      Serial.println("TOO WET!");
    }
    else {
      digitalWrite(LEDHPIN,  LOW);
    }
  }

  Serial.println(value);
}