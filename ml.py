import tensorflow as tf
import numpy as np

#I think this clears up memory if any is used??
#Dont know why this is needed, but my vscode crashed multiple times due to OOM :))
tf.keras.backend.clear_session()

#Loads ML model
model = tf.keras.models.load_model('saved_model/my_model')


def predictLetter(img):
    return model.predict(np.asarray(img).reshape(-1, 28,28))
