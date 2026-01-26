import librosa
import numpy as np
import base64
import io
from pydub import AudioSegment
import tempfile
import os

def decode_base64_to_audio(base64_string):
    """Convert Base64 string to audio file"""
    try:
        # Decode base64
        audio_bytes = base64.b64decode(base64_string)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.write(audio_bytes)
        temp_file.close()
        
        return temp_file.name
    except Exception as e:
        raise ValueError(f"Error decoding audio: {str(e)}")


def extract_features(audio_path):
    """Extract audio features (same as in notebook)"""
    
    # Load audio
    y, sr = librosa.load(audio_path, sr=16000)
    
    # 1. MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    
    # 2. Spectral features
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))
    
    # 3. Zero crossing rate
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    
    # 4. Chroma features
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
    
    # Combine all features
    features = np.concatenate([
        mfccs_mean,
        mfccs_std,
        [spectral_centroid, spectral_rolloff, spectral_contrast, zcr, chroma]
    ])
    
    return features


def generate_explanation(confidence, classification):
    """Generate explanation for the classification"""
    
    if classification == "AI_GENERATED":
        if confidence > 0.8:
            return "High spectral consistency and unnatural pitch patterns typical of AI-generated voices detected"
        elif confidence > 0.6:
            return "Moderate AI indicators found in voice characteristics and temporal patterns"
        else:
            return "Some AI-like features detected but confidence is low"
    else:  # HUMAN
        if confidence > 0.8:
            return "Natural voice variations, breath patterns, and human-like prosody detected"
        elif confidence > 0.6:
            return "Voice shows human characteristics with natural variations"
        else:
            return "Human voice detected but with some unusual patterns"