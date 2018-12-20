import csv
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib



# Restore the model's state,
# this requires a model with the same architecture.
model = joblib.load("train_model.m")

# print(model.predict(np.ones((10, 8))))


def predict(input_x):
    """
    infer mode
    @param input_x: shape=(8,)
    """
    return model.predict([input_x])[0]


if __name__ == "__main__":
    print(predict([618.5526727970789,621.0007778241641,623.4488828512496,617.1340521342489,616.8250679494433,2.4406429211378238,50]))