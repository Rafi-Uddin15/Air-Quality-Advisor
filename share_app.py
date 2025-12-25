from pyngrok import ngrok
import time

# We want to expose the port where Streamlit is running (8502 based on logs)
PORT = 8502

try:
    # 1. Open the tunnel
    public_url = ngrok.connect(PORT).public_url
    print(f"\n=======================================================")
    print(f"🌍 PUBLIC LINK GENERATED: {public_url}")
    print(f"=======================================================\n")
    print("Keep this script running to keep the link active!")
    
    # 2. Keep the script alive
    while True:
        time.sleep(1)

except Exception as e:
    print(f"Error: {e}")
    print("Note: You might need to add an auth token if you haven't used ngrok before.")
    print("Sign up at dashboard.ngrok.com -> Your Authtoken -> Run: ngrok config add-authtoken <TOKEN>")
