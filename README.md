# SmartWear: A Wireless Posture Monitoring and Correction System

### 2026-Team-16-SmartWear-A-Wireless-Posture-Monitoring-and-Correction-System

A real-time wearable IoT system that detects and classifies human posture using IMU sensors and Bluetooth communication.

---

## Table of Contents

- Overview
- Hardware Components
- Software and Dependencies
- Usage
- Results and Demonstration

---

## Overview

This project develops a wearable posture monitoring system that detects poor posture in real time.

An ESP32 microcontroller is connected to an IMU sensor (BNO055/BNO085) to collect orientation data such as roll and pitch. The data is transmitted via Bluetooth Low Energy (BLE) to a Raspberry Pi (or mobile device), where posture classification is performed.

The system is capable of detecting:
- Slouching forward (forward head posture)
- Leaning left or right
- Good posture alignment

The system includes automatic calibration and noise filtering to improve stability and usability.

An extended design supports multiple wearable nodes (e.g., head-mounted and waist-mounted sensors) to improve accuracy by comparing relative body angles.

---

## Hardware Components

- ESP32 Development Board (ESP-WROOM-32)
- IMU Sensor (BNO055 or BNO085)
- Breadboard and jumper wires
- Raspberry Pi (for data processing)
- USB cable (power and programming)

Optional:
- Second ESP32 + IMU (for head + waist posture detection)
- Wearable mounting (headphones, belt clip)

---

## Software and Dependencies

### Programming Languages:
- Arduino (ESP32 firmware)
- Python (Raspberry Pi processing)

### Libraries:

ESP32:
- Wire.h
- Adafruit_BNO055
- BLEDevice

Raspberry Pi:
- bleak
- asyncio
- collections

---

## Usage

### 1. ESP32 Setup

- Connect IMU via I2C:
  - SDA → GPIO21
  - SCL → GPIO22
- Upload Arduino code to ESP32
- Set BLE device name:
  SmartWear_ESP32

---

### 2. Raspberry Pi Setup

Create virtual environment:

python3 -m venv venv  
source venv/bin/activate  
pip install bleak  

---

### 3. Run the System

python posture_ble.py  

Make sure:
- ESP32 is powered on
- Bluetooth is enabled

---

### 4. Calibration

- Sit in correct posture
- Stay still for a few seconds
- System automatically records baseline

---

## Results and Demonstration

The system successfully detects posture in real time:

- Good posture → balanced roll and pitch
- Slouching forward → forward tilt detected
- Leaning left/right → roll deviation detected

Features:
- Real-time posture classification
- Bluetooth Low Energy communication
- Noise filtering (moving average)
- Automatic calibration

---

## Future Improvements

- Dual-sensor system (head + waist) for higher accuracy
- Mobile application (Flutter-based)
- Miniaturized wearable hardware (ESP32-C3)
- Haptic feedback (vibration alerts)

---

## Acknowledgements

This project was developed as part of an IoT course project, combining embedded systems, wireless communication, and real-time data processing.
