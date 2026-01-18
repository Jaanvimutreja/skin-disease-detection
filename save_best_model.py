import tensorflow as tf

# load trained model (jo actually exist karta hai)
model = tf.keras.models.load_model("skin_disease_cnn_model.h5")

# save final deployment-ready model
model.save("final_skin_disease_model.keras")

print("Final model saved successfully!")
