import cv2
import numpy as np
from keras.models import model_from_json

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1,48,48,1)
    return feature/255.0

# Load the model architecture from JSON file
json_file = open("Model.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)

# Load the model weights
model.load_weights("Model_weights.h5")

def predict_image(image,img_path):
    # Define labels
    label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']

    # Read image
    image = cv2.imread(img_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cropframe = cv2.resize(gray_image, (48, 48))

    # Extract features and make prediction
    cropframe = extract_features(cropframe)
    pred = model.predict(cropframe) 
    prediction_label = label[np.argmax(pred)]
    return prediction_label
