import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix

# -------- PATHS --------
MODEL_PATH = "skin_disease_cnn_model.h5"
DATASET_PATH = r"C:\Users\jaanv\.cache\kagglehub\datasets\pacificrm\skindiseasedataset\versions\6\SkinDisease\SkinDisease"

# -------- LOAD MODEL --------
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully")

# -------- TEST DATA GENERATOR --------
test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    directory=DATASET_PATH + r"\test",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    shuffle=False
)

# -------- EVALUATION --------
loss, accuracy = model.evaluate(test_generator)
print(f"\nTest Accuracy: {accuracy*100:.2f}%")
print(f"Test Loss: {loss:.4f}")

# -------- PREDICTIONS --------
y_pred = model.predict(test_generator)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = test_generator.classes

# -------- CLASS NAMES --------
class_names = list(test_generator.class_indices.keys())

# -------- CONFUSION MATRIX --------
cm = confusion_matrix(y_true, y_pred_classes)
print("\nConfusion Matrix:")
print(cm)

# -------- CLASSIFICATION REPORT --------
report = classification_report(
    y_true,
    y_pred_classes,
    target_names=class_names
)

print("\nClassification Report:")
print(report)
