import tensorflow as tf
json_file = open("models/model8.json", "r")
model_json = json_file.read()
json_file.close()
model=tf.keras.models.model_from_json(
    model_json, custom_objects=None
)
model.load_weights('models/model8.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open('models/lite/model-8.tflite', 'wb') as f:
    f.write(tflite_model)
