"""
DermAI - Skin Disease Detection App
Flask Backend with TensorFlow Model Integration
Production-Ready for Render Deployment
"""

from flask import Flask, send_file, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import os
from io import BytesIO
import logging

# ============================================
# INITIALIZE FLASK APP
# ============================================
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# LOAD MODEL (ONCE AT STARTUP)
# ============================================
try:
    model_path = os.environ.get('MODEL_PATH', 'final_skin_disease_model.keras')
    if os.path.exists(model_path):
        MODEL = tf.keras.models.load_model(model_path)
        logger.info("✓ Model loaded successfully")
    else:
        logger.warning(f"Model not found at {model_path}")
        MODEL = None
except Exception as e:
    logger.error(f"✗ Failed to load model: {str(e)}")
    MODEL = None

# ============================================
# CLASS NAMES (MUST MATCH TRAINING ORDER)
# ============================================
CLASS_NAMES = [
    "Acne", "Actinic Keratosis", "Benign Tumors", "Bullous",
    "Candidiasis", "Drug Eruption", "Eczema", "Infestations",
    "Lichen", "Lupus", "Moles", "Psoriasis",
    "Rosacea", "Seborrheic Keratoses", "Skin Cancer",
    "Sun Damage", "Tinea", "Unknown Normal",
    "Vascular Tumors", "Vasculitis", "Vitiligo", "Warts"
]

# ============================================
# PREPROCESSING FUNCTION
# ============================================
def preprocess_image(img):
    """Resize and normalize image for model"""
    try:
        img = img.convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise Exception(f"Preprocessing error: {str(e)}")

# ============================================
# PREDICTION FUNCTION
# ============================================
def predict_disease(image):
    """Run model inference on image"""
    try:
        if MODEL is None:
            return {
                "success": False,
                "error": "Model not loaded",
                "label": "Error",
                "confidence": 0.0
            }
        
        # Preprocess
        processed = preprocess_image(image)
        
        # Predict
        preds = MODEL.predict(processed, verbose=0)[0]
        idx = int(np.argmax(preds))
        confidence = float(preds[idx])
        
        # Get top 5 predictions
        top_5_indices = np.argsort(preds)[-5:][::-1]
        top_5 = {
            CLASS_NAMES[i]: float(preds[i]) 
            for i in top_5_indices
        }
        
        return {
            "success": True,
            "label": CLASS_NAMES[idx],
            "confidence": confidence,
            "top_5": top_5
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "label": "Error",
            "confidence": 0.0
        }

# ============================================
# ROUTES
# ============================================

@app.route("/")
def index():
    """Serve main HTML page"""
    return send_file("index.html", mimetype="text/html")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """API endpoint for predictions"""
    try:
        # Check if image file is present
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image file provided"
            }), 400
        
        file = request.files["image"]
        
        if file.filename == "":
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Load image
        img = Image.open(BytesIO(file.read()))
        
        # Predict
        result = predict_disease(img)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    model_status = "loaded" if MODEL is not None else "not_loaded"
    return jsonify({
        "status": "ok",
        "model": model_status,
        "classes": len(CLASS_NAMES)
    })

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        "success": False,
        "error": "File too large. Max size: 16MB"
    }), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "success": False,
        "error": "Server error"
    }), 500

# ============================================
# RUN SERVER
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏥 DermAI - Skin Disease Detection")
    print("="*60)
    print(f"Model Status: {'✓ Loaded' if MODEL else '✗ Not Loaded'}")
    print(f"Classes: {len(CLASS_NAMES)}")
    print("\n📱 Server running at: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=False, host="localhost", port=5000, threaded=True)
