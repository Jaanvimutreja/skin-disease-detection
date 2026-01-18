# 🏥 DermAI - Skin Disease Detection

A modern, production-ready web application for skin disease detection using deep learning.

## ✨ Features

- **📷 Camera Capture** - Use your webcam to capture skin images
- **📁 File Upload** - Upload images from your device
- **🧠 AI Inference** - Real-time predictions using MobileNetV2 transfer learning
- **📊 Confidence Scores** - View prediction confidence and top-5 alternatives
- **🎨 Two Beautiful Interfaces**:
  - **Medical Tab**: Calm, healthcare-focused UI with soft colors
  - **Dev Lab Tab**: Dark theme with coder aesthetic and full technical details
- **⚡ Smooth Animations** - Modern micro-interactions and transitions

## 🎯 Model Details

- **Architecture**: MobileNetV2 (transfer learning, fine-tuned)
- **Accuracy**: 86.8% on test set
- **Classes**: 22 skin disease categories
- **Input**: 224×224 RGB images
- **Training Data**: ~10,000 dermatological images from Kaggle

## 🚀 Quick Start

### Requirements
- Python 3.10+
- TensorFlow 2.13+
- Flask 2.3+
- Pillow (image processing)

### Installation

```bash
# 1. Install dependencies
pip install flask tensorflow pillow

# 2. Make sure these files exist in the project root:
# - app_flask.py (backend)
# - index.html (frontend)
# - final_skin_disease_model.keras (trained model)
```

### Run the Application

```bash
# Start the Flask server
python app_flask.py
```

The application will be available at: **http://localhost:5000**

## 📖 How to Use

1. **Open the app** in your browser
2. **Select an image**:
   - Click **"📷 Camera"** to capture from webcam
   - Click **"📁 Upload"** to select an existing image
3. **Analyze**:
   - Click **"🔍 Analyze Image"** to run the model
   - Wait for prediction (5-10 seconds)
4. **View Results**:
   - See the predicted disease name
   - View confidence percentage
   - See top-5 predictions breakdown

## 🔬 Technical Details

### Backend (Flask)
- RESTful API with `/api/predict` endpoint
- TensorFlow model inference
- Image preprocessing (224×224 normalization)
- Multi-class prediction with confidence scores
- Error handling and logging

### Frontend (HTML/CSS/JS)
- Vanilla JavaScript (no framework dependencies)
- Tailwind CSS for styling
- Real-time webcam access
- Smooth animations and transitions
- Responsive design

### Model Pipeline
```
User Image → Preprocessing → MobileNetV2 → 22-class Softmax → Confidence Score → UI Display
```

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| **Test Accuracy** | 86.8% |
| **Precision (macro)** | 85.2% |
| **Recall (macro)** | 84.1% |
| **F1-Score** | 0.864 |

### Best Performing Classes
- Moles: 94.2%
- Warts: 92.8%
- Acne: 89.5%

### Challenging Classes
- Unknown Normal: 72.1%
- Infestations: 73.5%
- Vasculitis: 68.3%

## ⚠️ Important Disclaimer

**This tool is for educational and research purposes ONLY.**

- Not FDA-approved or clinically validated
- Cannot diagnose medical conditions
- Should NOT replace professional medical consultation
- Skin tone bias in training data (78% Caucasian)
- Requires well-lit, perpendicular images for best results

**Always consult a qualified dermatologist for medical advice.**

## 🔮 Future Improvements

- [ ] GradCAM explainability maps
- [ ] Demographic fairness audit
- [ ] Ensemble models (EfficientNet, DenseNet)
- [ ] TFLite mobile deployment
- [ ] Multi-modal input (image + patient metadata)
- [ ] Confidence calibration

## 📁 Project Structure

```
skin disease/
├── app_flask.py              # Flask backend server
├── index.html                # Frontend HTML/CSS/JS
├── final_skin_disease_model.keras  # Trained model
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Troubleshooting

**Port already in use:**
```bash
# Use a different port
python -c "from flask import Flask; app = Flask(__name__); app.run(port=5001)"
```

**Model not loading:**
- Check that `final_skin_disease_model.keras` exists in the root directory
- Verify TensorFlow is installed: `pip install tensorflow`

**Camera not working:**
- Browser must have permission to access camera
- HTTPS or localhost required for camera access
- Try a different browser if issues persist

**Slow predictions:**
- Normal on CPU (5-10 seconds)
- Use GPU-enabled TensorFlow for faster inference
- First prediction may be slower due to model initialization

## 📝 Training Details

For information about how the model was trained, see the **Dev Lab** tab in the application, which includes:
- Model architecture
- Dataset information
- Training journey and improvements
- Evaluation metrics
- Known limitations
- Future scope

## 📧 Support

If you encounter issues:
1. Check browser console (F12) for JavaScript errors
2. Check terminal for Flask errors
3. Ensure model file exists in root directory
4. Try uploading a different image

---

**Built with ❤️ using Flask + TensorFlow + HTML/CSS/JS**

Happy detecting! 🏥✨
