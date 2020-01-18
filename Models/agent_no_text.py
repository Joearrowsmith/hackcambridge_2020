import random
import gym
import numpy as np
import os.path
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

import tensorflow as tf



class DQNAgent:
    def __init__(self):
        self.grid_state_size = (9, 9, 7) # 9 x 9, 7 one hot
        self.message_state_size = (4,11) # 4 directions, 2 messages at most seperated by ;
        self.action_size = 10

        self.recurrent_memory = 25
        self.memory = deque(maxlen=1000)

        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001

        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    """Huber loss for Q Learning
    References: https://en.wikipedia.org/wiki/Huber_loss
                https://www.tensorflow.org/api_docs/python/tf/losses/huber_loss
    """

    def _huber_loss(self, y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond  = K.abs(error) <= clip_delta

        squared_loss = 0.5 * K.square(error)
        quadratic_loss = 0.5 * K.square(clip_delta) + clip_delta * (K.abs(error) - clip_delta)

        return K.mean(tf.where(cond, squared_loss, quadratic_loss))



    def _build_model(self, batch_size, time_steps=25, window_onehot_shape=(9,9,7), dropout=0.0, recurrent_dropout=0.0):
        self.units = 5

        # Grid --------------
        self.grid_input_shape = (None, time_steps, *window_onehot_shape)
        
        grid_inputs = tf.keras.Input(shape=grid_input_shape, name='reccurrent_grid_inputs')

        self.grid_layer_1 = tf.keras.layers.ConvLSTM2D(self.units, (3,3), padding="same", activation="relu", recurrent_activation="tanh", 
                dropout=dropout, recurrent_dropout=dropout, return_sequences=True, stateful=False)
        self.maxpool_1 = tf.keras.layers.MaxPool2D((2,2))

        self.grid_layer_2 = tf.keras.layers.ConvLSTM2D(self.units, (3,3), padding="same", activation="relu", recurrent_activation="tanh", 
                dropout=dropout, recurrent_dropout=dropout, return_sequences=True, stateful=False)
        self.maxpool_2 = tf.keras.layers.MaxPool2D((2,2))
        self.flat = tf.keras.layers.Flatten()
        
        # ------------------

        self.dense_merge = tf.keras.layers.Dense(self.units)
        self.output = tf.keras.layers(self.units, activation='linear')

        # ------------------

        grid_x = self.grid_layer_1(self.grid_inputs)
        grid_x = self.maxpool_1(grid_x)
        grid_x = self.grid_layer_2(grid_x)
        grid_x = self.maxpool_2(grid_x)
        grid_x = self.flat(grid_x)
        grid_x = self.dense_merge(grid_x)
        merge_outputs = self.output(grid_x)

        model = keras.Model(grid_inputs, merge_outputs, name='model_output')

        model.compile(loss=self._huber_loss,
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                # a = self.model.predict(next_state)[0]
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * np.amax(t)
                # target[0][action] = reward + self.gamma * t[np.argmax(a)]
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        if os.path.isfile(name):
            self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)