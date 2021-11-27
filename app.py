import os
import sys 
from flask import (
     Flask, 
     request, 
     redirect, 
     url_for, 
     make_response, 
     jsonify, 
     render_template, 
     send_from_directory)
import predict
from predict import TestProcess
import get_recipe
from get_recipe import GetRecipeURL

UPLOAD_FOLDER = './static/user_upload'

app = Flask(__name__, static_folder='./static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recipe')
def mainpage():
    return render_template('recipe.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'upload_file' not in request.files:
            print("ファイルなし")
            return redirect(request.url)
        if request.files['upload_file'].filename:
            #画像オブジェクトを受け取る。
            uploads_files = request.files['upload_file']
            #それぞれの画像に対してuser_uploadまでのパスを定義作成してsaveメソッドを用いて保存する。
            img_path = os.path.join(UPLOAD_FOLDER, uploads_files.filename)
            uploads_files.save(img_path)
            #フォルダ内の何番目の画像がアップロードされたのか取得する
            user_upload=os.listdir(UPLOAD_FOLDER)
            upload_number = int(user_upload.index(uploads_files.filename))
            #predict
            TestProcess(img_path)
        return redirect(url_for('result', upload_number=upload_number))

@app.route('/result<int:upload_number>')
def result(upload_number):
    #分類結果を表示 → predict.name
    #レシピ検索
    GetRecipeURL(predict.name)
    #レシピのURLを表示 → get_recipe.url_list
    print(get_recipe.url_list)
    return render_template(
        'result.html',
        user_upload=os.listdir(UPLOAD_FOLDER)[upload_number],
        predict_name = predict.name,
        food_name = get_recipe.food_name,
        url_list = get_recipe.url_list,
        name_list = get_recipe.recipe_name_list,
        img_list = get_recipe.recipe_img_list)

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5000)