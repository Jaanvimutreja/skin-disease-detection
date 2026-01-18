import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix

# ===============================
# LOAD FINAL MODEL
# ===============================
MODEL_PATH = "final_skin_disease_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully.")

# ===============================
# CORRECT DATASET PATH (CONFIRMED)
# ===============================
DATASET_PATH = r"C:\Users\jaanv\.cache\kagglehub\datasets\pacificrm\skindiseasedataset\versions\6\SkinDisease\SkinDisease\test"

print("Checking dataset path...")
print("Dataset path:", DATASET_PATH)

if not os.path.exists(DATASET_PATH):
    print("Error: Test dataset directory not found.")
    exit()

# ===============================
# DATA GENERATOR
# ===============================
datagen = ImageDataGenerator(rescale=1./255)

test_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    shuffle=False
)

# ===============================
# EVALUATION
# ===============================
loss, acc = model.evaluate(test_gen)
print("Final Test Accuracy:", round(acc * 100, 2), "%")
print("Final Test Loss:", round(loss, 4))

# ===============================
# PREDICTIONS
# ===============================
y_pred = model.predict(test_gen)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = test_gen.classes

# ===============================
# METRICS
# ===============================
print("\nConfusion Matrix:\n")
print(confusion_matrix(y_true, y_pred_classes))

print("\nClassification Report:\n")
print(
    classification_report(
        y_true,
        y_pred_classes,
        target_names=list(test_gen.class_indices.keys())
    )
)
