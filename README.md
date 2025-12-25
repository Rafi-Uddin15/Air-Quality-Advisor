# AI-Powered Indoor Environmental Advisor 🍃

Welcome to our IoT project! This system goes beyond simple air quality monitoring. It combines low-cost hardware with **Machine Learning** to accurately predict Air Quality Index (AQI) and uses an **AI Advisor** logic to give you actionable health advice in real-time.

## 🚀 Project Overview

We built this solution to solve a common problem: commercial air monitors are expensive, and cheap DIY sensors are often inaccurate and hard to understand.
Our system performs three main tasks:
1.  **Senses**: Captures Temperature, Humidity, and Gas levels (MQ-135) using an Arduino.
2.  **Predicts**: Uses a **Random Forest** Machine Learning model to correct sensor drift and output a standard AQI.
3.  **Advises**: A "Glassmorphism" Dashboard tells you exactly what to do (e.g., "Open a window", "Turn on purifier") based on the data.

---

## 🛠️ Hardware Requirements

*   **Arduino Uno R3** (or compatible board)
*   **DHT11** Temperature & Humidity Sensor
*   **MQ-135** Gas Sensor (Air Quality)
*   **MB102** Breadboard Power Supply (Recommended for stable gas readings)
*   Jumper wires & Breadboard

---

## 💻 Software & Libraries

The system relies on a Python backend for data processing and visualization.
*   **Python 3.8+**
*   **Libraries:**
    *   `serial` (Communication with Arduino)
    *   `streamlit` (The Dashboard UI)
    *   `pandas` (Data handling)
    *   `scikit-learn` (Machine Learning model)
    *   `plotly` (Graphs and Gauges)

---

## 📂 File Structure Explained

Here is what every file in this repository does:

*   `TEST.ino`: **The Firmware**. Upload this to your Arduino. It reads sensors and sends data via USB.
*   `log_to_csv.py`: **The Bridge**. Reads the serial data from Arduino and saves it to a CSV file in real-time.
*   `train_model.py`: **The Brain**. Run this once to train the Machine Learning model (`aqi_model.pkl`) using historical data.
*   `advisor.py`: **The Logic**. Contains the ML prediction function and the "Expert System" rules for health advice.
*   `dashboard.py`: **The Interface**. The main Streamlit application that you see on your screen.

---

## ⚡ How to Run the Project

Follow these steps to get everything up and running:

### 1. Hardware Setup
Connect your sensors to the Arduino:
*   **DHT11 Data** → Pin 2
*   **MQ-135 Analog** → Pin A0
*   Upload `TEST.ino` to your board using the Arduino IDE.

### 2. Python Environment
Install the required dependencies:
```bash
pip install pyserial streamlit pandas scikit-learn plotly joblib
```

### 3. Start Data Collection
Run the logger script. Make sure to update the `COM_PORT` in the code if needed (e.g., COM3, /dev/ttyUSB0).
```bash
python log_to_csv.py
```
*Keep this running in a separate terminal window.*

### 4. Launch the Dashboard
In a new terminal, launch the interface:
```bash
streamlit run dashboard.py
```
The app will open in your browser, showing live metrics and AI advice!

---

## 👥 Authors
**Group IOT-GRP-07** - *CSE406 (Internet of Things)*
*   Rafi Uddin
*   Md. Sakib Hasan
*   Sumona Sharmin Israt
*   Md. Hasibul Hassan Himel

---
*Built with ❤️ and Code.*
