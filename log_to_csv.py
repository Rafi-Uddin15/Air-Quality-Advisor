import serial
import csv
import os

PORT = "COM6"      # change to your port
BAUD = 9600
OUT_FILE = "air_quality_log.csv"

ser = serial.Serial(PORT, BAUD, timeout=1)

with open(OUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp_ms", "temperature_c", "humidity_pct", "mq135_raw"])
    print("Logging... Press Ctrl+C to stop.")

    try:
        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue
            writer.writerow(parts)
            f.flush()
            os.fsync(f.fileno()) # Force write to disk immediately
            print(parts)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        ser.close()
