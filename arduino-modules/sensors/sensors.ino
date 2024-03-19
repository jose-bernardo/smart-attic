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

bool humidityWarning = false;
bool temperatureWarning = false;
bool lightWarning = false;

float maxTemperature = 25;
float minTemperature = 15;
float maxHumidity = 60;
float minHumidity = 30;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1000);
  Serial.flush();
  // Initialize device.
  dht.begin();
  //Serial.println(F("DHT11 Unified Sensor Example"));
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  /*
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
  */
  // Set delay between sensor readings based on sensor details.
  delayMS = sensor.min_delay;

  pinMode(LEDLPIN, OUTPUT);
  pinMode(LEDHPIN, OUTPUT);
  pinMode(LEDTPIN, OUTPUT);
}

void loop() {
    // Reconfigure values if requested
    if (Serial.available() > 0) {
        Serial.println("Configuring...");

        minTemperature = Serial.readStringUntil('\n').toFloat();
        maxTemperature = Serial.readStringUntil('\n').toFloat();
        minHumidity = Serial.readStringUntil('\n').toFloat();
        maxHumidity = Serial.readStringUntil('\n').toFloat();

        Serial.println("Operating with new configuration");
    }

    Serial.println("Min temperature:");
    Serial.println(minTemperature);
    Serial.println("Min temperature:");
    Serial.println(maxTemperature);
    Serial.println("Min humidity:");
    Serial.println(minHumidity);
    Serial.println("Max humidity:");
    Serial.println(maxHumidity);

    int lightValue = analogRead(A0);

    if (lightValue > 80) {
        if (!lightWarning) {
            lightWarning = true;
            digitalWrite(LEDLPIN, HIGH);
            Serial.println("warning light");
        }
    } else {
        lightWarning = false;
        digitalWrite(LEDLPIN,  LOW);
    }

    // Get temperature event and print its value.
    sensors_event_t event;
    dht.temperature().getEvent(&event);
    if (isnan(event.temperature)) {
        Serial.println(F("error reading temperature!"));
    } else {
        Serial.print("measurement temperature ");
        Serial.println(event.temperature);

        if (event.temperature < minTemperature) {
            if (!temperatureWarning) {
                temperatureWarning = true;
                digitalWrite(LEDTPIN, HIGH);
                Serial.println("warning temperature cold");
            }
        } else if (event.temperature > maxTemperature) {
            if (!temperatureWarning) {
                temperatureWarning = true;
                digitalWrite(LEDTPIN, HIGH);
                Serial.println("warning temperature hot");
            }
        } else {
            temperatureWarning = false;
            digitalWrite(LEDTPIN,  LOW);
        }
    }
    // Get humidity event and print its value.
    dht.humidity().getEvent(&event);
    if (isnan(event.relative_humidity)) {
        Serial.println(F("error reading humidity!"));
    } else {
        Serial.print("measurement humidity ");
        Serial.println(event.relative_humidity);

        if (event.relative_humidity < minHumidity) {
            if (!humidityWarning) {
                humidityWarning = true;
                digitalWrite(LEDHPIN, HIGH);
                Serial.println("warning humidity dry");
            }
        } else if (event.relative_humidity > maxHumidity) {
            if (!humidityWarning) {
                humidityWarning = true;
                digitalWrite(LEDHPIN, HIGH);
                Serial.println("warning humidity wet");
            }
        } else {
            humidityWarning = false;
            digitalWrite(LEDHPIN,  LOW);
        }

        // Delay between measurements.
        delay(delayMS);
    }
}