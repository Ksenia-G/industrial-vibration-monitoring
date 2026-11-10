#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

// 200 Гц = новое измерение каждые 5000 микросекунд.
static const uint32_t kPeriodUs = 5000;

void setup() {
  Serial.begin(115200);
  delay(500);
  if (!mpu.begin()) {
    Serial.println("MPU not found");
    while (true) {
      delay(100);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
}

void loop() {
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  const uint32_t t0 = micros();

  mpu.getEvent(&accel, &gyro, &temp);
  Serial.print(t0);
  Serial.print(',');
  Serial.print(accel.acceleration.x, 3);
  Serial.print(',');
  Serial.print(accel.acceleration.y, 3);
  Serial.print(',');
  Serial.println(accel.acceleration.z, 3);

  while (micros() - t0 < kPeriodUs) {
  }
}
