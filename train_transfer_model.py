import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import kagglehub

# ----------------------------
# DATASET PATH
# ----------------------------
path = kagglehub.dataset_download("pacificrm/skindiseasedataset")
data_dir = os.path.join(path, "SkinDisease", "SkinDisease")
train_dir = os.path.join(data_dir, "train")
test_dir = os.path.join(data_dir, "test")

# ----------------------------
# IMAGE SETTINGS
# ----------------------------
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# ----------------------------
# DATA GENERATORS
# ----------------------------
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.2,
    horizontal_flip=True
)

test_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

test_data = test_gen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# ----------------------------
# MOBILE NET V2 (CNN)
# ----------------------------
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base CNN
base_model.trainable = False

# ----------------------------
# CUSTOM CLASSIFIER
# ----------------------------
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)

output = Dense(train_data.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

# ----------------------------
# COMPILE MODEL
# ----------------------------
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ----------------------------
# TRAIN MODEL
# ----------------------------
history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=10
)

# ----------------------------
# SAVE MODEL
# ----------------------------
model.save("skin_disease_mobilenet_model.h5")
print("Transfer learning model saved!")
