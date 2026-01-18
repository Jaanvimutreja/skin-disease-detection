import os
import kagglehub
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# ===============================
# 1. Dataset Path Setup
# ===============================

path = kagglehub.dataset_download("pacificrm/skindiseasedataset")

data_dir = os.path.join(path, "SkinDisease", "SkinDisease")
train_dir = os.path.join(data_dir, "train")
test_dir = os.path.join(data_dir, "test")

print("Train directory:", train_dir)
print("Test directory:", test_dir)

# ===============================
# 2. Image Preprocessing
# ===============================

img_size = (224, 224)
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

# ===============================
# 3. CNN Model Architecture
# ===============================

model = Sequential([
    Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation="relu"),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(train_data.num_classes, activation="softmax")
])

# ===============================
# 4. Compile Model
# ===============================

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ===============================
# 5. Train Model
# ===============================

history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=5
)

# ===============================
# 6. Save Model
# ===============================

model.save("skin_disease_cnn_model.h5")
print("Model saved successfully!")
