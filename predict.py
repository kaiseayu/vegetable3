import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing import image
import os
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import os.path as op


file_name = 'vgg16_vegetable_name'
hw={'height':224, 'width':224}

def TestProcess(imgname):
    modelname_text = open(file_name + "model.json").read()
    json_strings = modelname_text.split('##########')
    #野菜の名前の読み込み
    textlist = json_strings[1].replace("[", "").replace("]", "").replace("\'", "").split()
    #モデル構造の読み込み
    model = model_from_json(json_strings[0]) 
    #重みの読み込み
    model.load_weights(file_name + 'weight.h5')
    #画像の前処理
    img = load_img(imgname, target_size=(hw['height'], hw['width']))
    TEST = img_to_array(img)/255
    #予測
    pred = model.predict(np.array([TEST]), batch_size=1, verbose=0)
    
    global name
    name = textlist[np.argmax(pred)].replace(",", "")