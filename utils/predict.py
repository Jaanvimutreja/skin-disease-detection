import numpy as np

def predict_image(model, image, class_names):
    preds = model.predict(image)
    idx = np.argmax(preds)
    confidence = float(preds[0][idx])
    return {
        "label": class_names[idx],
        "confidence": confidence
    }
