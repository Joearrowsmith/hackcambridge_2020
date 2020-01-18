import tensorflow as tf

from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

import backend.grid
import Models.grid_functions


MAP = backend.grid.generate_random_map()
window = MAP[34:43, 34:43]
window_onehot = Models.grid_functions.encode_grid_onehot(window)

# Building CNN with 3 convolutional
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=window_onehot.shape))
model.add(layers.MaxPooling2D((1, 1)))
model.add(layers.Dropout(0.2))

model.add(layers.Conv2D(64, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((1, 1)))
model.add(layers.Dropout(0.2))

model.add(layers.Conv2D(128, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((1, 1)))
model.add(layers.Dropout(0.2))

model.summary()

model.compile(optimizer='adam',
              loss='crossentropy',
              metrics=['accuracy'])
