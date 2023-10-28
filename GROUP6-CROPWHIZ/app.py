#from flask import Flask, render_template, request, Markup

from flask import Flask, render_template, request
from markupsafe import Markup

import pandas as pd
from utils.fertilizer import fertilizer_dict
import os
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import pickle
from numpy import asarray
from io import BytesIO
from PIL import Image
import tensorflow as tf

MODEL = tf.keras.models.load_model("./potatoes")
CLASS_NAME = ["Early Blight","Late Blight","Healthy"]

classifier = load_model('Trained_model.h5')
#classifier._make_predict_function()
classifier.make_predict_function()

crop_recommendation_model_path = 'Crop_Recommendation.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

app = Flask(__name__)

@ app.route('/fertilizer-predict', methods=['POST'])
def fertilizer_recommend():

    crop_name = str(request.form['cropname'])
    N_filled = int(request.form['nitrogen'])
    P_filled = int(request.form['phosphorous'])
    K_filled = int(request.form['potassium'])

    df = pd.read_csv('Data/Crop_NPK.csv')

    N_desired = df[df['Crop'] == crop_name]['N'].iloc[0]
    P_desired = df[df['Crop'] == crop_name]['P'].iloc[0]
    K_desired = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = N_desired- N_filled
    p = P_desired - P_filled
    k = K_desired - K_filled

    if n < 0:
        key1 = "NHigh"
    elif n > 0:
        key1 = "Nlow"
    else:
        key1 = "NNo"

    if p < 0:
        key2 = "PHigh"
    elif p > 0:
        key2 = "Plow"
    else:
        key2 = "PNo"

    if k < 0:
        key3 = "KHigh"
    elif k > 0:
        key3 = "Klow"
    else:
        key3 = "KNo"

    abs_n = abs(n)
    abs_p = abs(p)
    abs_k = abs(k)

    response1 = Markup(str(fertilizer_dict[key1]))
    response2 = Markup(str(fertilizer_dict[key2]))
    response3 = Markup(str(fertilizer_dict[key3]))
    return render_template('Fertilizer-Result.html', recommendation1=response1,
                           recommendation2=response2, recommendation3=response3,
                           diff_n = abs_n, diff_p = abs_p, diff_k = abs_k)


def pred_pest(pest):
    try:
        test_image = image.load_img(pest, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifier.predict_classes(test_image)
        return result
    except:
        return 'x'

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/CropRecommendation.html")
def crop():
    return render_template("CropRecommendation.html")

@app.route("/FertilizerRecommendation.html")
def fertilizer():
    return render_template("FertilizerRecommendation.html")

@app.route("/PesticideRecommendation.html")
def pesticide():
    return render_template("PesticideRecommendation.html")

@app.route('/DiseasePrediction.html')
def disease_prediction():
    return render_template('DiseasePrediction.html')


def read_as_np_array(data):
    image = np.array(Image.open(BytesIO(data)))
    return image



@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']  # fetch input
        file_read = file.read()
        filename = file.filename

        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
        image = read_as_np_array(file_read)
        image_batch = np.expand_dims(image,0)
        prediction = MODEL.predict(image_batch)

        predict_class = CLASS_NAME[np.argmax(prediction[0])]
        confidence = np.max(prediction[0])
        
        predict_html = {
            'class': predict_class,
            'confidence':float(confidence)
        }
        # print('img/user uploaded/'+filename)


        return render_template('disease-result.html',prediction=predict_html,user_file='img/user uploaded/'+filename)
    else:
        return "welcome to predict"
    

@ app.route('/crop_prediction', methods=['POST'])
def crop_prediction():
    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['potassium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        my_prediction = crop_recommendation_model.predict(data)
        final_prediction = my_prediction[0]
        return render_template('crop-result.html', prediction=final_prediction, pred='img/crop/'+final_prediction+'.jpg')

if __name__ == '__main__':
    app.run(debug=True)

            #133  file.save(file_path)



        # pred = pred_pest(pest=file_path)
        # if pred == 'x':
        #     return render_template('unaptfile.html')
        # if pred[0] == 0:
        #     pest_identified = 'aphids'
        # elif pred[0] == 1:
        #     pest_identified = 'armyworm'
        # elif pred[0] == 2:
        #     pest_identified = 'beetle'
        # elif pred[0] == 3:
        #     pest_identified = 'bollworm'
        # elif pred[0] == 4:
        #     pest_identified = 'earthworm'
        # elif pred[0] == 5:
        #     pest_identified = 'grasshopper'
        # elif pred[0] == 6:
        #     pest_identified = 'mites'
        # elif pred[0] == 7:
        #     pest_identified = 'mosquito'
        # elif pred[0] == 8:
        #     pest_identified = 'sawfly'
        # elif pred[0] == 9:
        #     pest_identified = 'stem borer' 159