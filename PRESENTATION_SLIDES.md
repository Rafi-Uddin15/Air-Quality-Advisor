# Presentation Slides: AI-Powered Indoor Environmental Advisor

## Slide 1: Title Slide
**Title:** AI-Powered Indoor Environmental Advisor: An IoT and Machine Learning Approach
**Course:** CSE406 -- Internet of Things
**Group:** IOT-GRP-07

**Team Members:**
*   Rafi Uddin (2022-1-60-037)
*   Md. Sakib Hasan (2022-1-60-098)
*   Sumona Sharmin Israt (2022-1-60-066)
*   Md. Hasibul Hassan Himel (2022-3-60-113)

---

## Slide 2: Introduction & Problem Statement
**The Problem:**
*   **Invisible Threat:** Indoor air pollution is often 2-5x worse than outdoors.
*   **Data Gap:** Traditional monitors only show raw numbers (e.g., "450ppm"), which are confusing to normal users.
*   **Passive Monitoring:** Existing low-cost systems don't tell you *what to do*.

**Our Solution:**
*   An "Active Advisor" system.
*   Combines **IoT Sensors** (Real-time data) + **Machine Learning** (Accurate AQI) + **AI Advice** (Actionable insights).

---

## Slide 3: Objectives
1.  **Develop** a low-cost, accurate multi-sensor monitoring node (Arduino-based).
2.  **Implement** a Machine Learning model (Random Forest) to predict Air Quality Index (AQI) from raw sensor voltages.
3.  **Bridge the gap** between data and user understanding using an AI-based "Advisor" dashboard.
4.  **Validate** the system against standard baselines (Linear Regression) to ensure accuracy.

---

## Slide 4: System Architecture (Hardware)
**Core Controller:**
*   **Arduino Uno R3** (ATmega328P): Robust 5V logic, stable ADC.

**Sensors:**
*   **DHT11**: Measures Temperature (0-50°C) and Humidity (20-90%).
*   **MQ-135**: Detects hazardous gases ($NH_3$, $CO_2$, Benzene).
*   **MB102 Power Module**: Ensures stable 5V, preventing sensor heating from affecting the microcontroller.

*(Visual Recommendation: Show photos of the Arduino, DHT11, and MQ-135 from the report)*

---

## Slide 5: Methodology & Data Flow
**The Pipeline:**
1.  **Acquisition:** Sensors sampled every 2 seconds by Arduino.
2.  **Transmission:** Custom UART Packet: `<START>:<TEMP>:<HUM>:<GAS>:<END>`.
3.  **Logging:** Python script buffers data to CSV (multithreaded to prevent data loss).
4.  **Inference:** Random Forest Model estimates AQI.
5.  **Visualization:** Streamlit Dashboard displays Real-time Guages + AI Advice.

---

## Slide 6: Machine Learning Implementation
**Why Random Forest?**
*   **Non-Linearity:** Gas sensor sensitivity changes with Temperature/Humidity. Linear models fail here.
*   **Robustness:** Ensemble of 150 Decision Trees reduces overfitting.

**Feature Engineering:**
*   We created a "Compensated Voltage" feature:
    $$V_{comp} = V_{gas} \times (1 + \alpha(T_{amb} - 20))$$
*   This significantly improved accuracy on hot/humid days.

---

## Slide 7: Software & The "Advisor" Layer
**Glassmorphism Dashboard (Streamlit):**
*   Modern, clean UI.
*   Real-time gauges for Temp, Humidity, and predicated AQI.

**The Advisor Logic (Simplified RAG):**
*   **Input:** Current AQI (e.g., 125).
*   **Logic:**
    *   *If AQI 0-50 (Good):* "Enjoy the fresh air!"
    *   *If AQI 51-100 (Moderate):* "Sensitive groups should close windows."
    *   *If AQI > 150 (Unhealthy):* "Action Required: Turn on Air Purifier."
*   **Benefit:** Turns data into instant action.

---

## Slide 8: Results & Performance
**Model Accuracy:**
*   **Random Forest (Ours):** MAE = 2.15 (Best)
*   **SVM:** MAE = 5.8
*   **Linear Regression:** MAE = 12.4

**Key Finding:**
*   Our model is **6x more accurate** than basic linear approximations.
*   Inference time is negligible (0.12ms), making it suitable for real-time edge use.

---

## Slide 9: Cost Analysis
**Why it matters:** Commercial monitors cost ~$200+.

**Our Bill of Materials:**
*   Arduino Uno: ~$5.00
*   Sensors (DHT11+MQ135): ~$3.50
*   Power & Misc: ~$3.50
*   **TOTAL: ~$12.00**

**Conclusion:** We achieved ~90% of the functionality of pro monitors at **6% of the cost**.

---

## Slide 10: Conclusion & Future Work
**Summary:**
*   Successfully built an end-to-end IoT system.
*   Solved the "interpretation problem" with the AI Advisor.
*   Achieved high accuracy with low-cost hardware.

**Future Scope:**
*   **Forecasting:** Implement LSTM (Deep Learning) to predict air quality 1 hour in advance.
*   **Cloud Integration:** Move from local Python script to AWS/Firebase for remote monitoring.

---

## Slide 11: Q&A
**Thank You!**

Any questions?
