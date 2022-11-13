from flask import Flask, render_template, request, jsonify

import numpy as np

import imageConverter
import ml

app = Flask(__name__)

app.config['SECRET_KEY'] = "TEST"

#Prediction labels, mostly unused
numbers = [0,1,2,3,4,5,6,7,8,9]
upper = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
targetLabels = numbers + upper + lower


#Shows html site, most likely redundant code her:)
@app.route('/', methods=['GET','POST'])
def home():

    return render_template('index.html')

@app.route('/predictImage', methods=['GET', 'POST'])
def get_Img():

    b64img = request.json['b64img']
    imageConverter.convertBase64ToPng(b64img)  # b64img is the base64 representation of the canvas
    
    img = imageConverter.imageConvert() #Use own created function to convert 128x128 to 28x28
    
    prediction = ml.predictLetter(img) #Use ml model to guess letter

    predictionVal = np.argmax(prediction) # Gets highest prediction%

    return jsonify(upper[predictionVal])  # Return what the ml model predicts


if __name__ == '__main__':
    app.run(debug=True)