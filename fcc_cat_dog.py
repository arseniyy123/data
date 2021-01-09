"""
Here you have the code to classify images of dogs and cats. It uses Tensorflow and Keras to create a
convolutional neural network that correctly classifies images of cats and dogs at least 66% of the time.

The process is: - DEFINING PROJECT PATHS AND PARAMETERS FOR PRE PROCESSING
                - LOADING THE IMAGES
                - RECREATION THE TRAIN DATA SET
                - DEFINING CNN
                - TRAINING CNN
                - SAVING MODEL
                - MODEL EVALUATION

The structure of the dataset files that are downloaded looks like this:

    cats_and_dogs
    |__ train:
        |______ cats: [cat.0.jpg, cat.1.jpg ...]
        |______ dogs: [dog.0.jpg, dog.1.jpg ...]
    |__ validation:
        |______ cats: [cat.2000.jpg, cat.2001.jpg ...]
        |______ dogs: [dog.2000.jpg, dog.2001.jpg ...]
    |__ test: [1.jpg, 2.jpg ...]

You can tweak epochs and batch size if you like, but it is not required.
"""

#LIBRARIES
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import matplotlib.pyplot as plt

#DEFINING PROJECT PATHS
PATH = 'cats_and_dogs'
train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

# PARAMETERS FOR PRE PROCESSING.
batch_size = 128
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

#LOADING THE IMAGES
train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

train_image_generator = ImageDataGenerator(rescale=1./255)
validation_image_generator = ImageDataGenerator(rescale=1./255)
test_image_generator = ImageDataGenerator(rescale=1./255 )

train_data_gen = train_image_generator.flow_from_directory(directory=train_dir, target_size=(IMG_HEIGHT, IMG_WIDTH), batch_size=batch_size, class_mode="binary")
val_data_gen = validation_image_generator.flow_from_directory(directory=validation_dir, target_size=(IMG_HEIGHT, IMG_WIDTH), batch_size=batch_size, class_mode="binary")
test_data_gen = test_image_generator.flow_from_directory(directory=PATH, target_size=(IMG_HEIGHT, IMG_WIDTH), batch_size=batch_size, classes=['test'], shuffle=False)

#VISUALIZATION FUNCTION
def plotImages(images_arr, probabilities = False):
    fig, axes = plt.subplots(len(images_arr), 1, figsize=(5,len(images_arr) * 3))
    if probabilities is False:
      for img, ax in zip( images_arr, axes):
          ax.imshow(img)
          ax.axis('off')
    else:
      for img, probability, ax in zip( images_arr, probabilities, axes):
          ax.imshow(img)
          ax.axis('off')
          if probability > 0.5:
              ax.set_title("%.2f" % (probability*100) + "% dog")
          else:
              ax.set_title("%.2f" % ((1-probability)*100) + "% cat")
    plt.show()

sample_training_images, _ = next(train_data_gen)
plotImages(sample_training_images[:5])

#RECREATION OF train_image_generator TO REDUCE RISK OF OVERFITTING CREATING MORE TRAINING DATA FROM EXISTING TRAINING
#EXAMPLES USING RANDOM TRANFORMATIONS
train_image_generator = ImageDataGenerator(zca_epsilon=1e-06, 
                                           rotation_range=30, 
                                           width_shift_range=0.11, 
                                           height_shift_range=0.1, 
                                           shear_range=0.1, 
                                           zoom_range=0.25, 
                                           channel_shift_range=0.0, 
                                           horizontal_flip=True, 
                                           vertical_flip=True, 
                                           rescale=1./255)

#REDEFINING TRAINING DATA SET
train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                     directory=train_dir,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     class_mode='binary')

augmented_images = [train_data_gen[0][0][0] for i in range(5)]

plotImages(augmented_images)

#DEFINING THE STRUCTURE OF NETWORK, CNN
model = Sequential()
#CONVOLUTION AND POOLING LAYERS
model.add(Conv2D(32, (3,3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(128, (2,2), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
#ADDING DENSE LAYER
model.add(Flatten()) #poner datos en una linea
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
#ADDING OPTIMIZER AND LOSS FUNCTION
model.compile(optimizer='adam', metrics='accuracy',loss='binary_crossentropy')
model.summary()

#TRAINING AND SAVING WEIGHTS
checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

history = model.fit(x=train_data_gen, 
                    validation_data=val_data_gen, 
                    epochs=epochs,
                    callbacks=[cp_callback])
#SAVING MODEL
# complete way
model.save("cat_and_dog_model")
#new_model = tf.keras.models.load_model('cat_and_dog_model')
# HDF5 format
model.save('cat_and_dog_model.h5')
#new_model = tf.keras.models.load_model('cat_and_dog_model.h5')

# Loads the weights
#model.load_weights(checkpoint_path)


#VISUALIZATION FOR ACCURACY AND LOSS OF THE MODEL

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

#GETTING PROBABILITIES FOR TEST DATA, WHERE 0 = CAT AND 1 = DOG
probabilities = model.predict(x=test_data_gen).flatten()

#CHECKING

answers =  [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
            1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 
            0, 0, 0, 0, 0, 0]
correct = 0

for probability, answer in zip(probabilities, answers):
  if round(probability) == answer:
    correct +=1

percentage_identified = (correct / len(answers))

print(f"Your model correctly identified {round(percentage_identified, 2)}% of the images of cats and dogs.")