import tensorflow as tf
import numpy as np

print(tf.__version__)

model = tf.keras.Sequential([  # Adds a densely - connected layer with 64 units to the model:
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation=None)
])

model.compile(optimizer=tf.train.AdamOptimizer(0.001),
              loss='mse',
              metrics=['mse', 'mae'])

# Restore the model's state,
# this requires a model with the same architecture.
model.load_weights('./weights/my_model')

# print(model.predict(np.ones((10, 8))))


def predict(input_x):
    """
    infer mode
    @param input_x: shape=(8,)
    """
    return model.predict(np.array([input_x]))[0][0]


if __name__ == "__main__":
    print(predict([569.6155675,546.5017095,546.5017095,639.0927378,645.9957218,2.198143228,50,0]))