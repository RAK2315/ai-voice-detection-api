import librosa
import numpy as np
import base64
import io
from pydub import AudioSegment
import tempfile
import os
import joblib

# Load scaler globally
SCALER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "scaler.pkl")
scaler = joblib.load(SCALER_PATH)

def decode_base64_to_audio(base64_string):
    """Convert Base64 string to audio file"""
    try:
        audio_bytes = base64.b64decode(base64_string)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.write(audio_bytes)
        temp_file.close()
        return temp_file.name
    except Exception as e:
        raise ValueError(f"Error decoding audio: {str(e)}")


def extract_features(audio_path):
    """Enhanced feature extraction (MUST MATCH TRAINING!)"""
    y, sr = librosa.load(audio_path, sr=16000)
    
    # 1. MFCCs (40 coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    mfccs_max = np.max(mfccs, axis=1)
    mfccs_min = np.min(mfccs, axis=1)
    
    # 2. Spectral features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    
    # 3. Temporal features
    zcr = librosa.feature.zero_crossing_rate(y)
    
    # 4. Chroma features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    
    # 5. Tempo and rhythm
    tempo = librosa.beat.tempo(y=y, sr=sr)
    
    # Aggregate all features
    features = np.concatenate([
        mfccs_mean,
        mfccs_std,
        mfccs_max,
        mfccs_min,
        [np.mean(spectral_centroid), np.std(spectral_centroid)],
        [np.mean(spectral_rolloff), np.std(spectral_rolloff)],
        [np.mean(spectral_contrast), np.std(spectral_contrast)],
        [np.mean(spectral_bandwidth), np.std(spectral_bandwidth)],
        [np.mean(zcr), np.std(zcr)],
        [np.mean(chroma), np.std(chroma)],
        tempo
    ])
    
    # CRITICAL: Scale features
    features_scaled = scaler.transform([features])[0]
    
    return features_scaled


def generate_explanation(confidence, classification):
    """Generate explanation for the classification"""
    if classification == "AI_GENERATED":
        if confidence > 0.9:
            return "Strong AI indicators: unnatural spectral consistency and robotic prosody patterns detected"
        elif confidence > 0.75:
            return "High probability of AI generation based on voice characteristics and temporal patterns"
        elif confidence > 0.6:
            return "Moderate AI-like features detected in audio analysis"
        else:
            return "Some AI characteristics present but confidence is low"
    else:  # HUMAN
        if confidence > 0.9:
            return "Strong human characteristics: natural voice variations, breath patterns, and organic prosody"
        elif confidence > 0.75:
            return "Voice exhibits clear human qualities with natural acoustic variations"
        elif confidence > 0.6:
            return "Human voice detected with typical natural speech patterns"
        else:
            return "Human classification but with some unusual acoustic features"








'''
decode_base64_to_audio(): Converts Base64 string → temp MP3 file
extract_features(): Extracts 173 features from audio (same as training)
generate_explanation(): Creates human-readable explanation
'''