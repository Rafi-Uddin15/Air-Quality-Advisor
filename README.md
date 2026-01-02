# 🍃 AI-Powered Indoor Environmental Advisor
### IoT Smart Monitor with Machine Learning Predictions

![Arduino](https://img.shields.io/badge/Arduino-Hardware-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![IoT](https://img.shields.io/badge/IoT-Sensors_&_Data-blue?style=for-the-badge)
![Machine Learning](https://img.shields.io/badge/ML-Random_Forest-orange?style=for-the-badge)

---

## 🌍 Overview
Low-cost air sensors drift over time. This project solves that problem by combining **IoT Hardware** with a **Machine Learning Calibration Layer**. It reads raw data from MQ-135 sensors and uses a trained **Random Forest** model to predict the *accurate* Air Quality Index (AQI), providing actionable health advice.

---

## 🛠️ The System
1.  **Sensing Layer (Arduino)**:
    *   **MQ-135**: For CO2 and NH3 detection.
    *   **DHT11**: Temperature and Humidity context.
    *   Data is transmitted via Serial (USB) to the PC.

2.  **Intelligence Layer (Python)**:
    *   **Drift Correction**: ML model corrects sensor inaccuracies based on humidity/temp levels.
    *   **Advisor Logic**: An Expert System (Rule-based) that suggests actions (e.g., *"High CO2 detected: Turn on ventilation"*).

3.  **Visualization Layer (Streamlit)**:
    *   Real-time "Glassmorphism" dashboard showing live gauges and history charts.

---

## ⚡ How to Build
### Hardware Wiring
*   **MQ-135** -> A0 (Analog)
*   **DHT11** -> D2 (Digital)
*   Board: Arduino Uno R3

### Software
1.  Upload `TEST.ino` to Arduino.
2.  Run the Python logger: `python log_to_csv.py`
3.  Launch Dashboard: `streamlit run dashboard.py`

---
**Author**: Rafi Uddin | [LinkedIn](https://www.linkedin.com/in/rafi-uddin15)
