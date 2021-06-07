from re import template
from flask import Flask, session, render_template, url_for, jsonify, request, redirect
from pymongo import results
import translate, sentiment, synthesize, cognition, database
import json
import certifi
from flask_session.__init__ import Session
from flask_pymongo import PyMongo
from bson import ObjectId
import sys,struct
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['SESSION_TYPE']='redis'
# app.config['SECRET_KEY'] = 'dun want do fyp'
app.secret_key = 'dun want do fyp'
app.config['JSON_AS_ASCII'] = False
app.config["MONGO_URI"] = "mongodb://admin03:admin03@cluster0-shard-00-00.ozhyv.mongodb.net:27017,cluster0-shard-00-01.ozhyv.mongodb.net:27017,cluster0-shard-00-02.ozhyv.mongodb.net:27017/fyp?ssl=true&replicaSet=atlas-gvd5u7-shard-0&authSource=admin&retryWrites=true&w=majority"

mongo = PyMongo(app,tlsCAFile=certifi.where())
# sess = Session(app)


@app.route('/')
def index():
    session["cart"]=[]
    session["restaurantID"]=""
    return redirect(url_for('home'))

@app.route('/home')
def home():
    session["restaurantID"]=""
    return render_template('index.html')

@app.route('/translate-text', methods=['POST'])
def translate_text():
    data = request.get_json()
    text_input = data['text']
    translation_output = data['to']
    response = translate.get_translation(text_input, translation_output)
    return jsonify(response)

@app.route('/sentiment-analysis', methods=['POST'])
def sentiment_analysis():
    data = request.get_json()
    input_text = data['inputText']
    input_lang = data['inputLanguage']
    output_text = data['outputText']
    output_lang =  data['outputLanguage']
    response = sentiment.get_sentiment(input_text, input_lang, output_text, output_lang)
    return jsonify(response)

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text_input = data['text']
    voice_font = data['voice']
    tts = synthesize.TextToSpeech(text_input, voice_font)
    tts.get_token()
    audio_response = tts.save_audio()
    return audio_response


@app.route('/image-to-text',methods=['POST'])
def image_to_text():
    data = request.get_data()
    link = "https://static8.orstatic.com/userphoto2/photo/1G/15SD/0895PJ1F4BBFCF940BE9A2px.jpg"
    response = cognition.get_imagetext(link)
    print(type(response))
    return jsonify(response)
    


@app.route('/restaurant',methods=['GET'])
def serach_res():
    restaurantName = request.args.get('restName', '')  
    if restaurantName:
        criteria = {"$text": {"$search":restaurantName} } 
        docs = list(mongo.db.shop.find(criteria))
    else:
        docs = list(mongo.db.shop.find())
    for doc in docs:
        print(doc)
    return render_template("restaurant_list.html",docs=docs)


@app.route('/detail/<lang>/<rest_id>',methods=['GET',"POST"])
def res_detail(lang,rest_id):
    r_docs = mongo.db.shop.find_one({"_id": ObjectId(rest_id)})       #only contain one document!!
    session["restaurantID"]= rest_id
    session["language"] = lang
    if r_docs:
        if (lang=="zh"):
            m_id = r_docs["menu"]["zh"]
            m_docs = mongo.db.menu.find_one({"_id":m_id})
        elif (lang=="en"):
            m_id = r_docs["menu"]["en"]
            m_docs = mongo.db.en_menu.find_one({"_id":m_id})
        elif (lang=="jp"):
            m_id = r_docs["menu"]["jp"]
            m_docs = mongo.db.jp_menu.find_one({"_id":m_id})
        elif (lang=="kr"):
            m_id = r_docs["menu"]["kr"]
            m_docs = mongo.db.kr_menu.find_one({"_id":m_id})
        print (r_docs,m_docs)
        return render_template("restaurant.html", r_docs=r_docs,m_docs=m_docs,lang=lang)       
    else:
        return "No record found"

@app.route('/dish/<lang>',methods=["GET","POST"])
def dish_choose(lang):
    m_id = request.args.get('id', '')
    d_index= request.args.get('index', '')
    r_id = request.args.get('r_id', '')
    r_docs = mongo.db.shop.find_one({"_id":ObjectId(r_id)})
    if (lang=="zh"):
        m_docs = mongo.db.menu.find_one({"_id":ObjectId(m_id)})
    elif (lang=="en"):
        m_docs = mongo.db.en_menu.find_one({"_id":ObjectId(m_id)})
    elif (lang=="jp"):
        m_docs = mongo.db.jp_menu.find_one({"_id":ObjectId(m_id)})
    elif (lang=="kr"):
        m_docs = mongo.db.kr_menu.find_one({"_id":ObjectId(m_id)})

    if m_docs:
        d_info = m_docs["dish"][int(d_index)]
    if m_docs:
        d_inf = m_docs["dish"][int(d_index)]
        if not ((d_inf["type"] == "Drink") or (d_inf["type"] == "飲品")):
            requirement = list(mongo.db.req.find({"category":"food"}))
        else:
            requirement = list(mongo.db.req.find({"category":"drink"}))
    # print(m_docs,r_docs)
        return render_template('dish.html', m_docs=m_docs,d_inf=d_info,r_docs=r_docs,d_index=d_index,lang=lang,req=requirement)
        print(d_info)
    # return "apple"

@app.route('/add_sum', methods=['POST'])
def add_sum():
    data = request.get_json()
    toppings = data['food_array']
    oprice = float(data['oprice'])
    soup = data["soup"]
    mid = data['mid']
    menu = {}
    lang = session.get('language')
    if (lang == "zh"):
        menu = mongo.db.menu.find_one({"_id":ObjectId(mid)})
    elif (lang == "en"):
        menu = mongo.db.en_menu.find_one({"_id":ObjectId(mid)})
    elif (lang=="jp"):
        menu = mongo.db.jp_menu.find_one({"_id":ObjectId(mid)})
    elif (lang=="kr"):
        menu = mongo.db.kr_menu.find_one({"_id":ObjectId(mid)})

    if (menu["topping"] and toppings):
        for e in toppings:
            oprice+=float(menu["topping"][int(e)]["price"])
    try:
        if (menu["soup"]):
            oprice+=float(menu["soup"][int(soup)]["price"])
    except:
        oprice = oprice
    return jsonify(oprice)


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload/restaurant')
def uploadRestaurant():
    return render_template('upload_r.html')

@app.route('/add_chart', methods=['POST'])
def add_chart():
    topping = request.form.getlist("topping")
    req = request.form.getlist("req")
    soup = request.form.get("soup")
    spicy = request.form.get("spicy")
    mid = request.form.get("mid")
    rid = request.form.get("rid")
    d_index = request.form.get("dindex")
    price = request.form.get("price")
    lang = session.get('language')
    
    c_id = mongo.db.shop.find_one({"_id":ObjectId(rid)},{"menu.zh":1,"_id":0})

    if (lang=="zh"):
        menu = mongo.db.menu.find_one({"_id":ObjectId(mid)})
        cmenu = menu
    elif (lang == 'en'):
        menu = mongo.db.en_menu.find_one({"_id":ObjectId(mid)})
        cmenu = mongo.db.menu.find_one({"_id":ObjectId(c_id["menu"]["zh"])})
    elif (lang == 'jp'):
        menu = mongo.db.jp_menu.find_one({"_id":ObjectId(mid)})
        cmenu = mongo.db.menu.find_one({"_id":ObjectId(c_id["menu"]["zh"])})
    elif (lang == 'kr'):
        menu = mongo.db.kr_menu.find_one({"_id":ObjectId(mid)})
        cmenu = mongo.db.menu.find_one({"_id":ObjectId(c_id["menu"]["zh"])})

    dish_info = menu["dish"][int(d_index)]
    dish_infoC = cmenu["dish"][int(d_index)]

    name = dish_info["name"]
    nameC = dish_infoC["name"]
    
    if soup is not None:
        soupName=menu["soup"][int(soup)]["name"]
        soupNameC=cmenu["soup"][int(soup)]["name"]
    else: 
        soupName="" 
        soupNameC=""
    if spicy is not None:
        taste=menu["level"][int(spicy)]
        tasteC=cmenu["level"][int(spicy)]
    else: 
        taste=""
        tasteC=""
    topping_name = []
    topping_nameC =[]
    for t in topping:
        topping_name.append(menu["topping"][int(t)]["name"])
        topping_nameC.append(cmenu["topping"][int(t)]["name"])
    reqC = []
    for r in req:
        temp = mongo.db.req.find_one({"$or":[{"c_name":r},{"e_name":r}]},{"c_name":1,"_id":0})
        reqC.append(temp["c_name"])

    try:
        cart_item = {'name': name, 'topping':topping_name, 
                    'soup':soupName, 'spicy':taste, 'req':req,
                    'price':price}
        cart_itemC = {'name': nameC, 'topping':topping_nameC, 
                    'soup':soupNameC, 'spicy':tasteC, 'req':reqC,
                    'price':price}

        if 'cart' not in session:
            session['cart'] = []
            session['cartC'] = []
        cart_list = session['cart']
        cart_listC = session['cartC']
        cart_list.append(cart_item)
        cart_listC.append(cart_itemC)
        session['cart'] = cart_list
        session['cartC'] = cart_listC
        print(session.get('cart'))
        print(session.get('cartC'))
        return render_template('script.html',cart_list=session.get('cart'),cart_listC=session.get('cartC'),lang=session.get('language'))
    except:
        return "error"

@app.route('/view_cart', methods=['POST','GET'])
def view_chart():
    if 'cart' not in session:
            session['cart'] = []
    if 'cartC' not in session:
            session['cartC'] = []
    return render_template('script.html',cart_list=session.get('cart'),r_id=session.get('restaurantID'),lang=session.get('language'))

@app.route('/view_cart/delete/<int:session_index>', methods=['POST','GET'])
def delete_cart(session_index):
    cart_list = session['cart']
    cart_list.pop(session_index)
    session['cart'] = cart_list
    cart_listC = session['cartC']
    cart_listC.pop(session_index)
    session['cartC'] = cart_listC
    return redirect(url_for('view_chart'))

@app.route('/view_cart/empty', methods=['POST','GET'])
def empty_cart():
    session.pop("cart")
    session.pop("cartC")
    return redirect(url_for('view_chart'))

@app.route('/manage/<lang>/edit',methods=['GET'])
def edit_menu_list(lang):
    rest_id = request.args.get('rest_id', '')
    r_docs = mongo.db.shop.find_one({"_id": ObjectId(rest_id)})
    m_id = r_docs["menu"]["zh"]
    m_docs = mongo.db.menu.find_one({"_id": ObjectId(m_id)})
    f_m_docs = database.show_edit(lang,rest_id)
    return render_template("manage.html",m_doc = m_docs, f_m_doc= f_m_docs,r_docs=r_docs,lang=lang)

@app.route('/manage/update',methods=["POST"])
def update_menu():
    data = request.get_json()
    print(data)
    database.update_data(data)
    return jsonify("nothing")

@app.route('/manage/upload/image',methods=["POST"])
def image_upload():
    # f = request.form.get['imgInp']
    # filename = f.filename
    # print(request.files['imgInp'])
    return "done"

@app.route('/set')
def set_cookie():
    session['cart'] = []
    return 'done'

   