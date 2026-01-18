import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load model once
model = tf.keras.models.load_model('final_skin_disease_model.keras')

# Disease classes
DISEASE_CLASSES = [
    'Acanthosis nigricans',
    'Acne',
    'Actinic keratosis',
    'Basal cell carcinoma',
    'Callus',
    'Eczema',
    'Erythema multiforme',
    'Melanoma',
    'Moles',
    'Neurofibromatosis',
    'Nevus',
    'Pityriasis alba',
    'Pityriasis rubra pilaris',
    'Psoriasis',
    'Rosacea',
    'Scabies',
    'Seborrheic keratosis',
    'Squamous cell carcinoma',
    'Tinea corporis',
    'Urticaria',
    'Vascular lesions',
    'Vitiligo'
]

def predict_disease(image):
    """
    Predict skin disease from image
    """
    if image is None:
        return None, "Please upload an image first"
    
    try:
        # Preprocess image
        img = Image.fromarray(image).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        predictions = model.predict(img_array, verbose=0)
        confidence = np.max(predictions[0])
        disease_idx = np.argmax(predictions[0])
        disease_name = DISEASE_CLASSES[disease_idx]
        
        # Get top 5
        top_5_idx = np.argsort(predictions[0])[-5:][::-1]
        
        # Format results
        result_text = f"🩺 **Detected Disease:** {disease_name}\n\n"
        result_text += f"📊 **Confidence:** {confidence*100:.2f}%\n\n"
        result_text += f"**Top 5 Predictions:**\n"
        
        for i, idx in enumerate(top_5_idx, 1):
            result_text += f"{i}. {DISEASE_CLASSES[idx]} - {predictions[0][idx]*100:.2f}%\n"
        
        return result_text, predictions[0]
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# Create custom CSS theme
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 15px;
    color: white;
    margin-bottom: 20px;
    text-align: center;
}
.info-box {
    background: #f0f4ff;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 20px 0;
}
"""

# Create Gradio interface with tabs
with gr.Blocks(title="🏥 DermAI - Skin Disease Detection", css=custom_css) as interface:
    
    # Header
    gr.HTML("""
    <div class="header">
        <h1>🏥 DermAI - Skin Disease Detection AI</h1>
        <p>Advanced Deep Learning Model | MobileNetV2 Transfer Learning</p>
        <p style="font-size: 0.9em; margin-top: 10px;">Detect 22 different skin diseases with 86.8% accuracy</p>
    </div>
    """)
    
    with gr.Tabs():
        
        # ========== MEDICAL TAB ==========
        with gr.Tab("🩺 Medical Diagnosis"):
            
            gr.HTML("""
            <div class="info-box">
                <p><strong>⚠️ DISCLAIMER:</strong> This tool is for educational purposes only. 
                Always consult a dermatologist for professional medical advice.</p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📸 Upload or Capture Image")
                    image_input = gr.Image(
                        label="Skin Image",
                        type="numpy",
                        sources=["upload", "webcam"]
                    )
                    predict_btn = gr.Button("🔍 Analyze Image", size="lg", variant="primary")
                
                with gr.Column():
                    gr.Markdown("### 📊 Diagnosis Results")
                    result_text = gr.Markdown("*Upload an image and click Analyze*")
                    
                    gr.Markdown("### 📈 Confidence Distribution")
                    result_chart = gr.BarPlot(
                        label="Top Classes Distribution",
                        x=None,
                        y=None,
                        visible=False
                    )
            
            # Connect button
            def analyze_and_chart(image):
                text, predictions = predict_disease(image)
                
                if predictions is None:
                    return text, gr.update(visible=False)
                
                # Create chart data
                top_5_idx = np.argsort(predictions)[-5:][::-1]
                diseases = [DISEASE_CLASSES[idx] for idx in top_5_idx]
                confidences = [predictions[idx]*100 for idx in top_5_idx]
                
                import pandas as pd
                chart_data = pd.DataFrame({
                    'Disease': diseases,
                    'Confidence': confidences
                })
                
                return text, gr.update(value=chart_data, visible=True)
            
            predict_btn.click(
                analyze_and_chart,
                inputs=[image_input],
                outputs=[result_text, result_chart]
            )
        
        # ========== DEV LAB TAB ==========
        with gr.Tab("🔬 Dev Lab"):
            
            with gr.Tabs():
                
                # Architecture
                with gr.Tab("🏗️ Architecture"):
                    gr.Markdown("""
                    ### Model Architecture
                    
                    **Base Model:** MobileNetV2 (Transfer Learning)
                    - **Input:** 224×224 RGB Images
                    - **Pre-trained:** ImageNet weights
                    - **Frozen Layers:** Initial training phase
                    - **Fine-tuned:** Last 30 layers unfrozen
                    
                    **Custom Head:**
                    - Global Average Pooling
                    - Dense(256, ReLU)
                    - Dropout(0.5)
                    - Dense(22, Softmax)
                    
                    **Total Parameters:** ~3.5M trainable
                    **Model Size:** 44MB (final_skin_disease_model.keras)
                    """)
                
                # Dataset
                with gr.Tab("📊 Dataset"):
                    gr.Markdown("""
                    ### Dataset Information
                    
                    **Source:** Kaggle - Skin Disease Dataset
                    
                    **Statistics:**
                    - Total Images: 10,000+
                    - Classes: 22 skin disease types
                    - Train/Val Split: 80/20
                    - Image Size: 224×224 pixels
                    
                    **Classes Covered:**
                    1. Acanthosis nigricans
                    2. Acne
                    3. Actinic keratosis
                    4. Basal cell carcinoma
                    5. Callus
                    6. Eczema
                    7. Erythema multiforme
                    8. Melanoma
                    9. Moles
                    10. Neurofibromatosis
                    11. Nevus
                    12. Pityriasis alba
                    13. Pityriasis rubra pilaris
                    14. Psoriasis
                    15. Rosacea
                    16. Scabies
                    17. Seborrheic keratosis
                    18. Squamous cell carcinoma
                    19. Tinea corporis
                    20. Urticaria
                    21. Vascular lesions
                    22. Vitiligo
                    """)
                
                # Training
                with gr.Tab("📈 Training"):
                    gr.Markdown("""
                    ### Training Process
                    
                    **Stage 1: Transfer Learning (5 epochs)**
                    - Learning Rate: 1e-3 (Adam optimizer)
                    - Base Model: Frozen
                    - Batch Size: 32
                    
                    **Stage 2: Fine-tuning (15 epochs)**
                    - Learning Rate: 1e-5 (Adam optimizer)
                    - Unfrozen Layers: Last 30
                    - Early Stopping: Patience=4
                    - Learning Rate Reduction: Factor=0.3, Patience=2
                    
                    **Data Augmentation:**
                    - Rotation: 30°
                    - Zoom: 20%
                    - Shifts: 20% (width & height)
                    - Horizontal Flip: Yes
                    - Rescale: 1/255
                    
                    **Class Weights:** Used to handle imbalanced data
                    """)
                
                # Evaluation
                with gr.Tab("📉 Evaluation"):
                    gr.Markdown("""
                    ### Model Performance
                    
                    **Final Results:**
                    - **Test Accuracy:** 86.8%
                    - **ROC-AUC Score:** 0.912
                    - **Precision:** ~87%
                    - **Recall:** ~87%
                    - **F1-Score:** ~86%
                    
                    **Per-Class Performance:**
                    - Best Classes: Melanoma, Acne, Psoriasis
                    - Challenging: Visually similar lesions
                    - Balanced: Yes (class weights used)
                    """)
                
                # Limitations
                with gr.Tab("⚠️ Limitations"):
                    gr.Markdown("""
                    ### Model Limitations
                    
                    ⚠️ **Important:**
                    1. NOT a medical diagnosis tool - use only for reference
                    2. Requires clear, well-lit images
                    3. Works best with direct, perpendicular angles
                    4. Isolated skin lesion needed
                    5. Background matters - clean background recommended
                    6. May confuse visually similar diseases
                    7. Demographic bias - trained mostly on lighter skin tones
                    8. CPU predictions take 5-10 seconds
                    9. No severity assessment
                    10. Cannot track progression over time
                    
                    **Always consult a dermatologist for accurate diagnosis!**
                    """)
                
                # Future
                with gr.Tab("🚀 Future"):
                    gr.Markdown("""
                    ### Future Improvements
                    
                    **Planned Features:**
                    - Multi-Model Ensemble
                    - Explainability (Grad-CAM visualization)
                    - Real-time webcam analysis
                    - Mobile app (iOS/Android)
                    - Better demographic representation
                    - Severity classification
                    - Image comparison over time
                    - Hospital EHR integration
                    - TensorFlow Lite optimization
                    - Multi-language support
                    """)
                
                # Tech Stack
                with gr.Tab("💻 Tech Stack"):
                    gr.Markdown("""
                    ### Technology Stack
                    
                    **Backend:**
                    - Python 3.10+
                    - TensorFlow 2.16.0
                    - Keras API
                    - NumPy, Pillow, Scikit-learn
                    - Gradio 5.0+ (this interface)
                    
                    **Deployment:**
                    - Hugging Face Spaces
                    - Docker (containerization)
                    - Git/GitHub
                    
                    **Development:**
                    - Jupyter Notebooks
                    - VSCode
                    
                    **Model:**
                    - MobileNetV2 (pre-trained ImageNet)
                    - Transfer Learning + Fine-tuning
                    - 44MB .keras format
                    """)
        
        # ========== ABOUT TAB ==========
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ### About DermAI
            
            DermAI is an AI-powered skin disease detection system built with:
            - **Deep Learning:** MobileNetV2 transfer learning
            - **Accuracy:** 86.8% on 22 disease classes
            - **Purpose:** Educational & reference tool
            
            ### Features
            - 📱 Upload or webcam capture
            - 🔍 Real-time predictions
            - 📊 Confidence scores
            - 📈 Top-5 predictions
            - 🎨 Beautiful UI
            
            ### Creator
            **Jaanvi Mutreja**
            - GitHub: [Skin Disease Detection](https://github.com/Jaanvimutreja/skin-disease-detection)
            - Portfolio: ML & AI Projects
            
            ### Links
            - 📊 Dataset: [Kaggle](https://www.kaggle.com/datasets/pacificrm/skindiseasedataset)
            - 📚 Model: MobileNetV2
            - 🚀 Deployment: Hugging Face Spaces
            
            ### Disclaimer
            ⚠️ **IMPORTANT:** This application is for **educational purposes only** and should NOT be used for actual medical diagnosis. 
            Always consult a licensed dermatologist for professional medical advice and diagnosis.
            
            ---
            
            Made with ❤️ using TensorFlow & Gradio
            """)

# Launch app
if __name__ == "__main__":
    interface.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860
    )
