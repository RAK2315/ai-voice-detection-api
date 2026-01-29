from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import joblib
import os
from utils import decode_base64_to_audio, extract_features, generate_explanation
from config import API_KEY, MODEL_PATH, SUPPORTED_LANGUAGES

# Initialize FastAPI
app = FastAPI(title="AI Voice Detection API")

# Load model at startup
print("Loading model...")
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully!")


# Request body structure
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str


# Health check endpoint
@app.get("/")
@app.head("/")  # Add HEAD support
def health_check():
    return {"status": "API is running", "message": "Use POST /api/voice-detection"}


# Main detection endpoint
@app.post("/api/voice-detection")
async def detect_voice(
    request: VoiceRequest,
    x_api_key: str = Header(None)
):
    """
    Detect if voice is AI-generated or Human
    """
    
    # 1. Validate API Key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # 2. Validate language
    if request.language.capitalize() not in SUPPORTED_LANGUAGES:
        return {
            "status": "error",
            "message": f"Language must be one of: {', '.join(SUPPORTED_LANGUAGES)}"
        }
    
    # 3. Validate audio format
    if request.audioFormat.lower() != "mp3":
        return {
            "status": "error",
            "message": "Only MP3 format is supported"
        }
    
    temp_audio_path = None
    try:
        # 4. Decode Base64 to audio file
        temp_audio_path = decode_base64_to_audio(request.audioBase64)
        
        # 5. Extract features
        features = extract_features(temp_audio_path)
        features = features.reshape(1, -1)
        
        # 6. Predict
        prediction = model.predict(features)[0]
        confidence = model.predict_proba(features)[0].max()
        
        # 7. Classification
        classification = "AI_GENERATED" if prediction == 1 else "HUMAN"
        
        # 8. Generate explanation
        explanation = generate_explanation(confidence, classification)
        
        # 10. Return response
        return {
            "status": "success",
            "language": request.language,
            "classification": classification,
            "confidenceScore": round(float(confidence), 2),
            "explanation": explanation
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing audio: {str(e)}"
        }
    
    finally:
        # 9. Clean up temp file safely
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

# Run this to start server
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)