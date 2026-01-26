import requests
import base64

# 1. Convert audio to Base64
audio_path = r"D:\REHAAN\1. Ml Projects\5. AI Voice Detection\data\human\Hindi\human_hindi_1.mp3"

with open(audio_path, "rb") as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

# 2. Prepare request
url = "http://localhost:8000/api/voice-detection"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "sk_voice_detection_12345_secret"
}
data = {
    "language": "Hindi",
    "audioFormat": "mp3",
    "audioBase64": audio_base64
}
# 3. Send request
print("Sending request...")
response = requests.post(url, json=data, headers=headers)

# 4. Print result
print("\nResponse:")
print(response.json())



'''
TO TEST THE API, FOLLOW THESE STEPS:
You need TWO Command Prompt windows open at same time:
Window 1: Run API Server
bashcd "D:\REHAAN\1. Ml Projects\5. AI Voice Detection\api"
python main.py
```

**Keep this window OPEN!** It should show:
Loading model...
✅ Model loaded successfully!
Uvicorn running on http://0.0.0.0:8000
Window 2: Run Test Script
bashcd "D:\REHAAN\1. Ml Projects\5. AI Voice Detection"
python test_api.py
'''