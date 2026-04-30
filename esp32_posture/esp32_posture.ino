#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

// BLE UUIDs
#define SERVICE_UUID        "12345678-1234-1234-1234-1234567890ab"
#define CHARACTERISTIC_UUID "abcdefab-1234-1234-1234-abcdefabcdef"

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;

class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
  }

  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
    pServer->startAdvertising();
  }
};

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  delay(1000);

  if (!bno.begin()) {
    Serial.println("No BNO055 detected");
    while (1);
  }

  delay(1000);
  bno.setExtCrystalUse(true);

  // BLE setup
  BLEDevice::init("SmartWear_ESP32");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  BLEService *pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_NOTIFY |
                      BLECharacteristic::PROPERTY_READ
                    );

  pCharacteristic->addDescriptor(new BLE2902());
  pService->start();

  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->start();

  Serial.println("BLE started. Waiting for Raspberry Pi...");
}

void loop() {
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

  float heading = euler.x();
  float roll    = euler.z();
  float pitch   = euler.y();

  String data = String(heading, 2) + "," + String(roll, 2) + "," + String(pitch, 2);

  Serial.println(data);

  if (deviceConnected) {
    pCharacteristic->setValue(data.c_str());
    pCharacteristic->notify();
  }

  delay(200);
}