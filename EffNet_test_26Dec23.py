# import library for API
from flask import Flask, render_template , request, make_response
from flask import jsonify
import requests 

# import library for EffNet model
import efficientnet.tfkeras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models
import pandas as pd 
import numpy as np
import os
import json

app = Flask(__name__)

global vectorlist_old 
vectorlist_old = 0

#📍 load EffNet model --------------------------------------------

model_dir ='./EffNet/B5R4_Gender_500.h5' 
model_gender = load_model(model_dir)
height = width = model_gender.input_shape[1]
x = model_gender.get_layer('head_pooling').output
prediction_layer = model_gender.output
model_gender_fv = models.Model(inputs= model_gender.input, outputs=[prediction_layer,x]) 
labels_gender = dict({0: 'Men', 1: 'Women', 2: 'motorcycle'})# Gender label

model_dir ='./EffNet/B5R4_Category_500.h5' 
model_cate = load_model(model_dir)
labels_cate = dict({0: 'Student', 1: 'Working', 2: 'motorcycle'})# Category label

#📍 EffNet model model predict --------------------------------------

def model_predict(img_path):

    img = image.load_img(img_path, target_size=(height, width))
    # Convert it to a Numpy array with target shape.
    x = image.img_to_array(img)
    # Reshape
    x = x.reshape((1,) + x.shape)
    x /= 255.
    
    #🔆 EffNet model - Gender classify --------------------------------
    result = model_gender_fv.predict([x])
    result1 = result[0][0]
    result2 = result[1][0]
    result_gender = np.argmax(result1) #class
    pred_gender = labels_gender[result_gender]
    prob_gender = result1[result_gender]
    vectorlist= result2 #fv
    
 
    #🔆 EffNet model - Category classify ------------------------------
    predict_cate = model_cate.predict([x])[0]
    result_cate = np.argmax(predict_cate)
    pred_cate = labels_cate[result_cate]
    prob_cate = predict_cate[result_cate]
    
    count = 'yes'
    
    return pred_gender, prob_gender, pred_cate, prob_cate, count, vectorlist

def model_predict_multi_img(img_path, vectorlist_old):
    
    #🔆 cerrent image  --------------------------------------------------------
    img = image.load_img(img_path, target_size=(height, width))
    # Convert it to a Numpy array with target shape.
    x = image.img_to_array(img)
    # Reshape
    x = x.reshape((1,) + x.shape)
    x /= 255.
    
#     #🔆 old image  ------------------------------------------------------------
#     img_old  = image.load_img(img_path_old, target_size=(height, width))
#     # Convert it to a Numpy array with target shape.
#     x_old = image.img_to_array(img_old)
#     # Reshape
#     x_old = x_old.reshape((1,) + x_old.shape)
#     x_old /= 255. 
    
    #🔆 for predict Gender ----------------------------------------------------
    # img_array
    result = model_gender_fv.predict([x])
    result1 = result[0][0]
    result2 = result[1][0]
    result_gender = np.argmax(result1) #class
    pred_gender = labels_gender[result_gender]
    prob_gender = result1[result_gender]
    vectorlist= result2 #fv
#     # img_array_old
#     result_old = model_gender_fv.predict([x_old])
#     result2_old = result_old[1][0]
#     vectorlist_old= result2_old #fv
    
    #🔆 for predict Category ---------------------------------------------------
    predict_cate = model_cate.predict([x])[0]
    result_cate = np.argmax(predict_cate)
    pred_cate = labels_cate[result_cate]
    prob_cate = predict_cate[result_cate]
    
    #🔆 Euclidient Distance ----------------------------------------------------
    distance = np.sqrt(np.sum((vectorlist - vectorlist_old)**2))
    
    if distance >= 9.5 :
        count = 'yes'
        
    else:
        count = 'no'

    return pred_gender, prob_gender, pred_cate, prob_cate, distance, count, vectorlist

     

@app.route('/request',methods=['POST'])


def effnet_predict():
    global vectorlist_old 
    payload = request.data.decode("utf-8")
    inmessage = json.loads(payload)
    img_path = inmessage['img_path']
    see = int(inmessage['see'])
    per = int(inmessage['per'])
    
    if see == 1:
        if per == 0:
            pred_gender, prob_gender, pred_cate, prob_cate, count, vectorlist = model_predict(img_path)
            print('A')
            vectorlist_old = vectorlist
        else:
            print('B')
            pred_gender, prob_gender, pred_cate, prob_cate, count, vectorlist_ = model_predict(img_path)

        distance = 0
        return '{} {} {} {} {} {}'.format(pred_gender, prob_gender, pred_cate, prob_cate, distance, count)
    
    else:
        if per == 0:
            pred_gender, prob_gender, pred_cate, prob_cate, distance, count, vectorlist = model_predict_multi_img(img_path, vectorlist_old)
            print('C')
            vectorlist_old = vectorlist
        else:
            pred_gender, prob_gender, pred_cate, prob_cate, count, vectorlist_ = model_predict(img_path)
            print('D')
            distance = 0
            
        return '{} {} {} {} {} {}'.format(pred_gender, prob_gender, pred_cate, prob_cate, distance, count)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5007) 







