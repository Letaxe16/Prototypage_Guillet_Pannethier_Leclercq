/*
  Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleNotify.cpp
  Ported to Arduino ESP32 by Evandro Copercini
  updated by chegewara and MoThunderz
*/
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include "Adafruit_VL53L0X.h"


Adafruit_VL53L0X lox = Adafruit_VL53L0X();

BLEServer* pServer = NULL;
BLECharacteristic* pChar_angle_received = NULL;
BLECharacteristic* pChar_angle_send = NULL;
BLECharacteristic* pChar_obstacle_send = NULL;
BLECharacteristic* pChar_mode_received = NULL;
BLECharacteristic* pChar_speed_command = NULL;

BLEDescriptor *pDescr;
BLE2902 *pBLE2902;

int pChar2_value_int = 0;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t value = 0;
int distance_obs;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "3474d367-44ea-4a8b-9975-1b6affc2c253"
#define CHAR1_UUID          "7466421d-6449-4307-a960-e69253b712cd"
#define CHAR2_UUID          "9ea1c638-0a94-4117-b10b-acf70db2aaac"
#define CHAR3_UUID          "a673d20d-283d-4d66-8c5a-7ee1421d91a3"
#define CHAR4_UUID          "c84fdb5f-ef44-495f-8420-9e9d3f288ec6"
#define CHAR5_UUID          "91c42b70-b484-4c1a-8663-a2e14cde8b6b"
#define CHAR6_UUID          "115116ae-982d-4022-b788-7f8d7a8fc909"
#define CHAR7_UUID          "b0ef15be-2f49-480c-b707-45bd117c584e"

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

class CharacteristicCallBack_angle_handler: public BLECharacteristicCallbacks {   // Handle angle command reception
  void onWrite(BLECharacteristic *pChar) override { 
    std::string pChar2_value_stdstr = pChar->getValue();
    String pChar2_value_string = String(pChar2_value_stdstr.c_str());
    int pChar2_value_int = pChar2_value_string.toInt();
    Serial.println("Angle_cam:" + String(pChar2_value_int)); 
  }
};

class CharacteristicCallBack_mode_handler: public BLECharacteristicCallbacks {    // Handle switch mode command reception

  void onWrite(BLECharacteristic *pChar) override {

    std::string pChar4_value_stdstr = pChar->getValue();
    String pChar4_value_string = String(pChar4_value_stdstr.c_str());
    int pChar4_value_int = pChar4_value_string.toInt();
    Serial.println("Mode_status:" + String(pChar4_value_int));

  }

};

class CharacteristicCallBack_speed_handler: public BLECharacteristicCallbacks {    // Handle speed mode command reception

  void onWrite(BLECharacteristic *pChar) override {

    std::string pChar6_value_stdstr = pChar->getValue();
    String pChar6_value_string = String(pChar6_value_stdstr.c_str());
    int pChar6_value_int = pChar6_value_string.toInt();
    Serial.println("Speed_command:" + String(pChar6_value_int));

  }

};

void setup() {
  Serial.begin(9600);

  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }

  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X\n"));
    while(1);
  }

  // Create the BLE Device
  BLEDevice::init("Axel_ESP32");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pChar_angle_received = pService->createCharacteristic(
                      CHAR2_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  
                    );  

  pChar_angle_send = pService->createCharacteristic(
                      CHAR3_UUID,
                      BLECharacteristic::PROPERTY_NOTIFY
                    );  

  pChar_mode_received = pService->createCharacteristic(
                      CHAR4_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  
                    );  
  
  pChar_obstacle_send = pService->createCharacteristic(
                      CHAR1_UUID,
                      BLECharacteristic::PROPERTY_NOTIFY
                    ); 

  pChar_speed_command = pService->createCharacteristic(
                      CHAR6_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  
                    );  
  // Create a BLE Descriptor
  
  pDescr = new BLEDescriptor((uint16_t)0x2901);
  pDescr->setValue("A very interesting variable");
  pChar_angle_send->addDescriptor(pDescr);
  pChar_obstacle_send->addDescriptor(pDescr);
  
  pBLE2902 = new BLE2902();
  pBLE2902->setNotifications(true);
  
  // Add all Descriptors here
  pChar_angle_send->addDescriptor(pBLE2902);
  pChar_obstacle_send->addDescriptor(pBLE2902);

  pChar_angle_received->addDescriptor(new BLE2902());
  pChar_mode_received->addDescriptor(new BLE2902());
  pChar_speed_command->addDescriptor(new BLE2902());
  
  
  // After defining the desriptors, set the callback functions
  pChar_angle_received->setCallbacks(new CharacteristicCallBack_angle_handler());
  pChar_mode_received->setCallbacks(new CharacteristicCallBack_mode_handler());  
  pChar_speed_command->setCallbacks(new CharacteristicCallBack_speed_handler());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
}

void loop() {

  VL53L0X_RangingMeasurementData_t measure;
    
  lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!

  if (measure.RangeStatus != 4) {  // phase failures have incorrect data
    Serial.print("TOF:" + String(measure.RangeMilliMeter) + "\n"); 
    distance_obs = (int) measure.RangeMilliMeter;
  } else {
    uint16_t max = 2000;
    Serial.println("TOF:" +  String(max));
    distance_obs = 10000;
  }

  // notify changed value
  if (deviceConnected) {

    pChar_obstacle_send->setValue(distance_obs);
    pChar_obstacle_send->notify();
    delay(50);

    delay(200);
  }
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
      delay(200); // give the bluetooth stack the chance to get things ready
      pServer->startAdvertising(); // restart advertising
      oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
      // do stuff here on connecting
      oldDeviceConnected = deviceConnected;
  }
}
