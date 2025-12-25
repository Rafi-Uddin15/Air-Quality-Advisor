import joblib
import pandas as pd
import random

# --- CONFIG ---
MODEL_FILE = "aqi_model.pkl"

# --- KNOWLEDGE BASE (RAG Context) ---
# In a full RAG system, this would be a vector database (like ChromaDB). 
# For now, we use a structured dictionary as our Knowledge Base.
KNOWLEDGE_BASE = {
    "good": [
        "Air quality is fantastic! Enjoy the fresh air.",
        "Perfect conditions. Great time for a walk or run.",
        "Sensors report clean air. No action needed.",
        "Indoor environment is healthy and safe.",
        "Low pollution levels detected. Keep it up!"
    ],
    "moderate": [
        "Air quality is okay, but could be better.",
        "Sensitive individuals might feel slight discomfort.",
        "CO2 or dust levels are rising slightly.",
        "Consider opening a window if outdoor air is clean.",
        "Monitor the situation; it's within acceptable limits."
    ],
    "unhealthy": [
        "Warning: Pollutant levels are high!",
        "Active children and adults should avoid exertion.",
        "Ventilation recommended immediately.",
        "Possible VOCs or smoke detected. Check sources.",
        "Air quality is deteriorating. Take precautions."
    ],
    "hazardous": [
        "EMERGENCY: Air is dangerous!",
        "Evacuate or seal the room immediately.",
        "Gas leak or fire potential. Check sensors!",
        "Do not breathe this air without filtration.",
        "Critical pollution levels detected."
    ]
}

class AirAdvisor:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            self.model = joblib.load(MODEL_FILE)
            print("Model loaded successfully.")
        except FileNotFoundError:
            print(f"Warning: {MODEL_FILE} not found. Running in 'heuristic' mode until model is trained.")

    def predict_aqi(self, mq135_val, temp, hum):
        if self.model:
            # Prepare input dataframe matching training feature names
            # Trained on: field5 (Gas), field3 (Temp), field4 (Hum)
            input_data = pd.DataFrame([[mq135_val, temp, hum]], columns=['field5', 'field3', 'field4'])
            return self.model.predict(input_data)[0]
        else:
            # Fallback Heuristic if model isn't trained yet
            # (Just a rough estimation so the app doesn't crash)
            return (mq135_val / 10) + (temp * 0.5)

    def get_advice(self, current_aqi):
        category = "good"
        if 50 < current_aqi <= 100:
            category = "moderate"
        elif 100 < current_aqi <= 200:
            category = "unhealthy"
        elif current_aqi > 200:
            category = "hazardous"
        
        # "Retrieving" advice from our Knowledge Base
        advice_list = KNOWLEDGE_BASE.get(category, KNOWLEDGE_BASE["good"])
        return category.upper(), random.choice(advice_list)

# Singleton instance
advisor = AirAdvisor()
