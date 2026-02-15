import requests
import base64

# 1. Convert audio to Base64
audio_path = r"D:\REHAAN\1. Ml Projects\5. AI Voice Detection\data\human\Tamil\7303.mp3"

with open(audio_path, "rb") as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

# 2. Prepare request - USE LIVE URL
#url = "http://localhost:8000/api/voice-detection"  # Change port if 
# cd "D:\REHAAN\1. Ml Projects\5. AI Voice Detection\api"
url = "https://ai-voice-detection-api-tgt8.onrender.com/api/voice-detection"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "sk_voice_detection_12345_secret"
}
data = {
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": audio_base64
}

# 3. Send request
print("Testing LIVE API...")
response = requests.post(url, json=data, headers=headers)

# 4. Print result
print("\nResponse:")
print(response.json())
print(f"\nStatus Code: {response.status_code}")