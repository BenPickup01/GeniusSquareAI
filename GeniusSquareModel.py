from gym import Env
from gym.spaces import Box, Discrete, Tuple

from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import GreedyQPolicy

from keras import *
from keras.src.layers import Conv2D, MaxPooling2D, Reshape, Concatenate, Dropout, Activation, Conv1D
from keras.src.optimizers import Nadam, Adam

from PlayGeniusSquare import *
import tensorflow as tf

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten


class GeniusSquare(Env):
    def __init__(self):
        self.cumulative_reward = 0

        self.grid_shape = (6, 6, 1)
        self.grid = PlayBoard()
        self.grid.place_blockers()

        self.state = np.array(self.grid.get_grid()).reshape((1, 1, 6, 6))

        self.observation_space = Box(low=0, high=1, shape=self.grid_shape)

        # The action space is a tuple of the position of the tetroid, the rotation of the tetroid,
        # if the tetroid is inverted
        self.action_space = Tuple([
            Discrete(6),
            Discrete(6),
            Discrete(4),
            Discrete(2)
        ])

        self.game_steps = 8
        self.tetroid_number = 0
        print("OBJECT DEFINED")

    def step(self, action):
        # have the step number be the tetroid number
        print("ACTION HERE", action)

        # Convert the action into the position, rotation, invert and tetroid
        # Get the inedx of the largest value in action[0] and action[1]
        position = [action[0].idxmax(), action[1].idxmax()]
        rotation = action[2].idxmax()
        invert = action[3].idxmax()

        action = np.array(action)
        tetroid_number = self.tetroid_number

        reward = self.grid.place_tetroid(position, rotation, tetroid_number, invert)
        self.grid.show_grid()

        self.tetroid_number += 1
        self.state = np.array(self.grid.get_grid()).reshape((1, 1, 6, 6))
        self.cumulative_reward += reward[1]

        done = reward[1] < 3 or tetroid_number == self.game_steps

        return self.state, reward[1], done, {}

    def reset(self, seed=None, options=None):
        print("RESET")
        self.grid = PlayBoard()
        self.grid.place_blockers()
        self.state = np.array(self.grid.get_grid()).reshape((1, 1, 6, 6))
        self.cumulative_reward = 0
        return self.state

    def render(self, mode='human'):
        print(self.grid.show_grid())


def build_model():
    input_shape = (None, 1, 1, 6, 6)

    input_layer = Input(input_shape)
    layer1 = Reshape((6, 6, 1))(input_layer)  # Reshape to (1, 6, 6, 1)
    layer2 = Conv2D(32, (2, 2), activation='relu', padding='same')(layer1)
    layer3 = MaxPooling2D((2, 2))(layer2)
    layer4 = Flatten()(layer3)
    layer5 = Dense(32, activation='relu')(layer4)
    layer6 = Dense(32, activation='relu')(layer5)

    position_x = Dense(6, activation='relu')(layer6)
    position_y = Dense(6, activation='relu')(layer6)
    invert = Dense(2, activation='relu')(layer6)
    rotation = Dense(4, activation='relu')(layer6)

    output_layer = Concatenate()([position_x, position_y, invert, rotation])
    model = Model(inputs=input_layer, outputs=output_layer)

    return model


def build_agent(model, actions):
    policy = GreedyQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,
                   nb_actions=actions, nb_steps_warmup=50, target_model_update=1e-2, )
    return dqn


class GeniusSquareMultiOutputModel():

    def build_piece_input(self):
        x = Dense(32)
        x = Activation("relu")(x)

        return x

    def build_grid_input(self):
        x = Conv1D(36, 2, padding='same')
        x = Activation("relu")(x)

        return x

    def make_default_hidden_layers(self, inputs):

        x = Dense(32)
        x = Activation("relu")(x)
        return x

    def build_position_branch(self, inputs, name, num_positions=6):
        x = self.make_default_hidden_layers(inputs)

        x = Dense(128)(x)
        x = Activation("relu")(x)
        x = Dropout(0.5)(x)
        x = Dense(num_positions)(x)
        x = Activation("sigmoid", name=name)(x)
        x = Reshape((num_positions, 1))(x)

        return x

    def build_rotation_branch(self, inputs, number_rotations=4):
        x = self.make_default_hidden_layers(inputs)

        x = Dense(128)(x)
        x = Activation("relu")(x)
        x = Dropout(0.5)(x)
        x = Dense(number_rotations)(x)
        x = Activation("sigmoid", name="Rotation")(x)
        x = Reshape((number_rotations, 1))(x)

        return x

    def build_invert_branch(self, inputs, possible_inverts=2):
        x = self.make_default_hidden_layers(inputs)

        x = Dense(128)(x)
        x = Activation("relu")(x)
        x = Dropout(0.5)(x)
        x = Dense(possible_inverts)(x)
        x = Activation("sigmoid", name="Invert")(x)
        x = Reshape((possible_inverts, 1))(x)
        return x

    def assemble_full_model(self, rotations, inverts, size):
        input_shape = (None, 38)
        inputs = Input(shape=input_shape)

        x_branch = self.build_position_branch(inputs, "X_Position", size)
        y_branch = self.build_position_branch(inputs, "Y_Position", size)
        rotation_branch = self.build_rotation_branch(inputs, rotations)
        invert_branch = self.build_invert_branch(inputs, inverts)

        model = Model(inputs=inputs,
                      outputs=[x_branch, y_branch, rotation_branch, invert_branch], name="Genius Square Model")
        return model


model = GeniusSquareMultiOutputModel().assemble_full_model(4, 2, 6)

print("PRAY: \n ")
model.summary()
# Make a test grid to check the model
grid = PlayBoard()
grid.place_blockers()
grid_positions = grid.get_grid()


predictions = model.predict(np.array(grid_positions).reshape((1, 1, 36)))


for i in predictions:
    print(i[0].argmax())

actions = 4

dqn = build_agent(model, actions)

dqn.compile(Nadam(), metrics=['mae'])

dqn.fit(GeniusSquare(), nb_steps=300000, visualize=False, verbose=1)
dqn.save_weights('dqn_weights.h5f', overwrite=True)
