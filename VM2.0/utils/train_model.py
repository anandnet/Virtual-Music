"""import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import TensorBoard

tensorboard = TensorBoard(log_dir="logs/")
batch_size = 32
img_height = 100
img_width = 100

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "dataset/",
    validation_split=0.2,
    color_mode="grayscale",
    subset="training",
    seed=190,
    image_size=(img_height, img_width),
    batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "test_ds/",
    validation_split=0.2,
    color_mode="grayscale",
    subset="validation",
    seed=180,
    image_size=(img_height, img_width),
    batch_size=batch_size)

print(train_ds)
class_names = train_ds.class_names
print(class_names)

normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(
    1./255)
normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
# -----------------
first_image = image_batch[0]

# Notice the pixels values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

num_classes = 6


model = tf.keras.Sequential([
    layers.experimental.preprocessing.Rescaling(1./255,input_shape=(img_height, img_width, 1)),
    layers.Conv2D(32, 3, activation='relu',padding='same'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, activation='relu',padding='same'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu',padding='same'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
])


model.compile(
    optimizer='adam',
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])

model.summary()

checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
epochs = 10

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=[cp_callback, tensorboard],
)
model.save('saved_model/trained_model')
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

"""
from keras.callbacks import TensorBoard
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json
import os
tensorboard = TensorBoard(log_dir="logs/")

classifier=None
if(os.path.exists("models/model8.h5")):
    print("Model exist")
    json_file = open("models/model8.json", "r")
    model_json = json_file.read()
    json_file.close()
    classifier=model_from_json(
        model_json, custom_objects=None
    )
    classifier.load_weights('models/model8.h5')
else:
    # Step 1 - Building the CNN
    # Initializing the CNN
    classifier = Sequential()

    # First convolution layer and pooling
    classifier.add(Convolution2D(32, (3, 3), input_shape=(100, 100, 1), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    # Second convolution layer and pooling
    classifier.add(Convolution2D(32, (3, 3), activation='relu'))
    # input_shape is going to be the pooled feature maps from the previous convolution layer
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Flattening the layers
    classifier.add(Flatten())

    # Adding a fully connected layer
    classifier.add(Dense(units=128, activation='relu'))
    classifier.add(Dense(units=8, activation='softmax'))  # softmax for more than 2

# Compiling the CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[
                'accuracy'])  # categorical_crossentropy for more than 2


train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory('dummy_ds/',
                                                 target_size=(100, 100),
                                                 batch_size=8,
                                                 color_mode='grayscale',
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory('dummy_test_ds/',
                                            target_size=(100, 100),
                                            batch_size=8,
                                            color_mode='grayscale',
                                            class_mode='categorical')
classifier.fit_generator(
    training_set,
    steps_per_epoch=500,  # No of images in training set#600
    epochs=30,
    validation_data=test_set,
    validation_steps=40,#30
    callbacks=[tensorboard])  # No of images in test set

# Saving the model
model_json = classifier.to_json()
with open("models/model8.json", "w") as json_file:
    json_file.write(model_json)
classifier.save_weights('models/model8.h5')

