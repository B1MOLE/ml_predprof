import keras
import numpy as np

def execute_model(text):
    model = keras.models.load_model('here/')
    class_names = ["Business and Corporate", "E-Commerce", "Education", "Entertainment", "News", "Social Networking and Messaging"]
    result = model.predict(np.array([text]))
    # first = np.argmax(result)
    i = 0
    result_str = ""
    for string in class_names:
        result_str += string + ": " + str(result.item(i))
        i += 1
    return result_str
