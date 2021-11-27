from bs4 import BeautifulSoup
import requests
import urllib
import urllib.parse
import time
import predict

def GetRecipeURL(name):
    #野菜によって検索名を変える
    #最初に空の変数を定義すれば、条件分岐しても同じ変数を使える
    global food_name
    food_name = ''
    if name == 'キャベツ':
      food_name = name + 'の芯'
    elif name == 'カブ':
      food_name = name + 'の葉'
    else:
      food_name = name + 'の皮'

    #料理名をURLに入れるための処理
    name_quote = urllib.parse.quote(food_name)
    #URLを指定し、Webページを取得
    base_url = 'https://recipe.rakuten.co.jp/search/' + name_quote
    response = requests.get(base_url)
    #文字化けが起こらないようにする
    response.encoding = response.apparent_encoding
    #Webページを解析する
    bs = BeautifulSoup(response.text, 'html.parser')

    #<li class='recipe_ranking__item'></li>を取得する
    li_tag_list = bs.find_all('li', class_='recipe_ranking__item', limit=3)
    
    #urlを格納するリスト
    #他のpyファイル(app.py)でも使用したい変数はglobal宣言する
    global url_list
    url_list = []

    #その中の<a href=''></a>を取得する
    #find_allはリストで返されるからfor文を使う
    for li_tag in li_tag_list:
      for a_tag in li_tag.find_all('a'):
        href = a_tag.attrs['href']
        #URLを結合し、url_listにappend
        url = 'https://recipe.rakuten.co.jp/' + href
        url_list.append(url)
    
    global recipe_name_list
    recipe_name_list = []

    for li_tag_name in li_tag_list:
      for span_tag in li_tag_name.find_all('span', class_='recipe_ranking__recipe_title omit_2line'):
        recipe_name_list.append(span_tag.get_text())

    global recipe_img_list
    recipe_img_list = []

    for li_tag_img in li_tag_list:
      for img_tag in li_tag_img.find_all('img'):
        img_url = img_tag.attrs['src']
        recipe_img_list.append(img_url)
    
    # global recipe_dict
    # recipe_dict = dict(zip(url_list, recipe_name_list))
    # print(recipe_dict)

    time.sleep(1)

    