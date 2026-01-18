import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import json
from io import BytesIO
import base64

st.set_page_config(
    page_title="DermAI - Skin Disease Detection",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ================= SESSION STATE =================
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "last_image_key" not in st.session_state:
    st.session_state.last_image_key = 0

# ================= LOAD MODEL =================
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model("final_skin_disease_model.keras")
        st.success("✓ Model loaded successfully")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

model = load_model()

# ⚠️ SAME ORDER AS TRAINING
CLASS_NAMES = [
    "Acne", "Actinic Keratosis", "Benign Tumors", "Bullous",
    "Candidiasis", "Drug Eruption", "Eczema", "Infestations",
    "Lichen", "Lupus", "Moles", "Psoriasis",
    "Rosacea", "Seborrheic Keratoses", "Skin Cancer",
    "Sun Damage", "Tinea", "Unknown Normal",
    "Vascular Tumors", "Vasculitis", "Vitiligo", "Warts"
]

def preprocess_image(img):
    """Preprocess image for model prediction"""
    try:
        if isinstance(img, str):
            # Base64 encoded image
            img_bytes = base64.b64decode(img)
            img = Image.open(BytesIO(img_bytes))
        
        img = img.convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise Exception(f"Image preprocessing error: {str(e)}")

def make_prediction(image_data):
    """Make prediction on image"""
    try:
        if model is None:
            return {"error": "Model not loaded", "label": "Error", "confidence": 0.0, "success": False}
        
        processed_image = preprocess_image(image_data)
        preds = model.predict(processed_image, verbose=0)[0]
        idx = int(np.argmax(preds))
        confidence = float(preds[idx])
        
        return {
            "label": CLASS_NAMES[idx],
            "confidence": confidence,
            "success": True
        }
    except Exception as e:
        return {"error": str(e), "label": "Error", "confidence": 0.0, "success": False}

# ================= HIDDEN FILE UPLOADER FOR API =================
# This is triggered by iframe JavaScript via hidden channel
st.write("""
<style>
.streamlit-file-uploader { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Create hidden file uploader that iframe can trigger
uploaded_file = st.file_uploader(
    "Image Prediction",
    type=["jpg", "jpeg", "png", "gif", "bmp"],
    key=f"prediction_upload_{st.session_state.last_image_key}",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    result = make_prediction(uploaded_file)
    st.session_state.prediction_result = result
    st.session_state.last_image_key += 1
    st.rerun()

# ================= LOAD AND RENDER FRONTEND HTML =================
html_path = os.path.join(os.path.dirname(__file__), "frontend", "index.html")

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Pass prediction result to frontend via JavaScript injection
    prediction_json = json.dumps(st.session_state.prediction_result) if st.session_state.prediction_result else "null"
    
    # Inject script that makes prediction result available to iframe
    injected_html = html_content.replace(
        "</body>",
        f"""<script>
// Prediction result from Streamlit backend
window.STREAMLIT_PREDICTION_RESULT = {prediction_json};
if (window.STREAMLIT_PREDICTION_RESULT !== null) {{
  console.log('✓ Prediction result available:', window.STREAMLIT_PREDICTION_RESULT);
}}
</script>
</body>"""
    )
    
    st.components.v1.html(injected_html, height=1200, scrolling=True)
else:
    st.error(f"HTML file not found: {html_path}")
    st.info("Please ensure the frontend/index.html file exists in the project directory.")
