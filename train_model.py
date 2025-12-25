import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import os

# --- CONFIG ---
DATASET_FILE = "indoor_data.csv"
MODEL_FILE = "aqi_model.pkl"

def train():
    print("Loading dataset...")
    if not os.path.exists(DATASET_FILE):
        print(f"ERROR: {DATASET_FILE} not found.")
        return

    try:
        df = pd.read_csv(DATASET_FILE)
        print(f"Loaded {len(df)} rows.")
        
        # Mapping based on 'inspect_indices.py' and user metadata:
        # field2: MQ135 Composite AQI (Target)
        # field3: Temp (Input)
        # field4: Hum (Input)
        # field5: eCO2 (Input - We use this as a proxy for raw MQ135 voltage behavior)
        
        # Clean data
        df = df.dropna(subset=['field2', 'field3', 'field4', 'field5'])
        
        X = df[['field5', 'field3', 'field4']]
        y = df['field2'] # Target AQI

        # Renaming for clarity in the saved model object if we wanted, but sticking to positions for now.
        print(f"Using columns: Gas (eCO2 proxy)='field5', Temp='field3', Hum='field4' -> Target='field2 (AQI)'")
        
        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Model Training (Random Forest handles non-linear calibration well)
        print("Training Random Forest Model...")
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluation
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        print(f"Model Trained! Mean Absolute Error: {mae:.2f} AQI points")
        
        # Save Model
        joblib.dump(model, MODEL_FILE)
        print(f"Model saved to {MODEL_FILE}")

    except Exception as e:
        print(f"An error occurred during training: {e}")
        print("Tip: Check if your Kaggle CSV column names match the script's expectations.")

if __name__ == "__main__":
    train()
