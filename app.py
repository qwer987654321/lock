from flask import Flask, request, abort, render_template
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import json

import random
import string

#引入副程式
import FLEX
import firebase
import mqtt
import threading_test
#import time_schedule
# <== Flask 啟動 ==>
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('HNhpujXRIygreGV6xU09bJ4MhPIAl3G+vEunBklSbVVuAh+w/1pOWlSnouYidHedufJlHOoFuxFtLUNPKMrl9MmjgFTH5s9YQe6I61Pf3VPSbJYmOqc7B7Gx6udXynSsClNDfwzMK9g33q9Ex5xKEAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('22fc185afc54e2590e2b17455ad7b289')

def updata(post_input,user_id):
    profile = line_bot_api.get_profile(user_id)
    print(profile.display_name)
    print(profile.picture_url)
    print(profile.user_id)
    data = firebase.getdata("所有訂單/"+post_input[1])
    data.update({"訂單編號":post_input[1]})
    data.update({"LINE_name":profile.display_name})
    data.update({"LINE_image":profile.picture_url})
    data.update({"user_id":profile.user_id})
    return data

def updata_ALL_MAC_card(dqtt_data,model):
    #要把這個使用者有的鎖給新增至所有card裡，    還要再判斷訂單日期，在期限內的才要新增
    order_number = firebase.getdata("user_info/"+dqtt_data[0]+"/所有訂單編號")
    print(list(order_number.values()))
    for _order in list(order_number.values()):
        data = list(firebase.getdata("所有訂單/"+str(_order)+"/可使用所有鎖").values())
        landlord_ID = firebase.getdata("所有訂單/"+str(_order)).get("房東ID")
        print(data)
        print(landlord_ID)
        for upcard in data:
            if(model == "add"):
                firebase.setdata("user_info/"+landlord_ID+"/"+upcard+"/card/"+dqtt_data[0],dqtt_data[1])
                print(upcard)
            else:
                firebase.deldata("user_info/"+landlord_ID+"/"+upcard+"/card/"+dqtt_data[0])

            mqtt.client.publish("lock-"+str(upcard), "updata___")

@app.route("/")
def showPage():
    return render_template("index.html")

@app.route("/say_hello" ,methods=["POST"])
def submit():
    name=request.form.get("username")
    return "Hello, " + name

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    usrInput = event.message.text
    print("\nmessage_type = "+message_type+"\nuser_id = "+user_id+"\nreply_token = "+reply_token+"\nusrInput = "+usrInput+"\n")
    
    if usrInput == "HI":
        LIFF_URL="https://liff.line.me/1660846886-DkAYQvdM"
        message=TextSendMessage(event.message.text + "LIFF URL = " + LIFF_URL)
        line_bot_api.reply_message(event.reply_token, message)


    #開門　　：查尋<所有訂單>資料表，路徑是剛剛查到的<所有訂單編號>+<"可使用所有鎖">+<大門>，取得鎖的MAC值，發送MQTT到指定的鎖
    if(usrInput == '開門'):
        order_number = firebase.getdata("user_info/"+user_id+"/所有訂單編號")
        #開門時or新增卡片：找<user_info>資料表，裡自己的<所有訂單編號>有沒有訂單，有就做
        print(order_number)
        if(order_number):
            print(list(order_number.values())[0])
            MAC = firebase.getdata("所有訂單/"+str(list(order_number.values())[0])+"/可使用所有鎖")
            print(list(MAC.values()))
            print(len(list(MAC.values())))
            if(len(list(MAC.values())) > 1 ):
                print("有好幾個鎖")
            else:
                print("只有一個鎖")
                lock_MAC = "lock-"+list(MAC.values())[0]
                print(lock_MAC)
                payload = "open_door=" + reply_token
                print("payload = ",type(payload),payload)
                mqtt.client.publish(lock_MAC, payload)
                threading_test.thr(reply_token)
                #line_bot_api.reply_message(reply_token, TextSendMessage(text = "門鎖網路異常，開門失敗"))
        else:
            print("no")
            line_bot_api.reply_message(reply_token, TextSendMessage(text = "您沒有訂單"))    
    
    #新增卡片：查尋<所有訂單>資料表，路徑是剛剛查到的<所有訂單編號>+<"可使用所有鎖">+<大門>，取得鎖的MAC值，發送MQTT到指定的鎖
    if(usrInput == '查詢卡片'):
        card_ID = firebase.getdata("user_info/"+user_id).get('卡片資訊', "無")
        print(card_ID)
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='查詢卡片',contents = FLEX.card(card_ID,user_id)))
    
    #新增訂單：找<user_info>裡自己的<所有鎖>有沒有東西，有就做表示有已經設定好鎖了
    if(usrInput.split(":")[0] == '訂單編號'):
        data = firebase.getdata("所有訂單/"+usrInput.split(":")[1])
        data.update({"訂單編號":usrInput.split(":")[1]})
        firebase.pushdata("user_info/"+user_id+"/所有訂單編號",usrInput.split(":")[1])
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='訂單顯示',contents = FLEX.order_FLEX(data, "訂單顯示")))
        
    #輸入5位數都會視作為輸入訂單編號來判斷
    if(len(usrInput) == 5):    #也可以順便判斷有沒有切約人這個選項，有的話就顯示<此訂單已簽約成功>
        data = firebase.getdata("所有訂單/"+usrInput)
        data.update({"訂單編號":usrInput})
        print(data)
        if(data['簽約人'] == "無"):
            line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='訂單確認',contents = FLEX.order_FLEX(data, "訂單確認")))
        #line_bot_api.reply_message(reply_token, TextSendMessage(text = a))

    #查詢訂單：找<user_info>裡自己的<所有訂單編號>有沒有值，有就在去<所有訂單>查那筆訂單編號顯示出來
    if(usrInput == '查詢訂單'):
        try:
            order_number = firebase.getdata("user_info/"+user_id+"/所有訂單編號")
            line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='訂單顯示',contents = FLEX.order_list("訂單顯示", list(order_number.values()))))
        except:
           line_bot_api.reply_message(reply_token, TextSendMessage(text = "無訂單"))
 
    #查詢歷史訂單：找<user_info>裡自己的<歷史訂單編號>有沒有值，有就在去<所有訂單>查那筆訂單編號顯示出來
    if(usrInput == '查詢歷史訂單'):#顯示樣板
        try:
            order_number = firebase.getdata("user_info/"+user_id+"/歷史訂單編號")
            print(list(order_number.values()))
            line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='訂單顯示',contents = FLEX.order_list("訂單顯示", list(order_number.values()))))
        except:
           line_bot_api.reply_message(reply_token, TextSendMessage(text = "無歷史訂單"))
 
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    post_input = event.postback.data
    reply_token = event.reply_token
    post_input = post_input.split("-")
    print(post_input)
    if(post_input[0] == "help"):
        line_bot_api.reply_message(reply_token, TextSendMessage(text = "LIFF help"))

    if(post_input[0] == "簽約同意"):
        data = updata(post_input,user_id)
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='訂單同意',contents = FLEX.order_consent(data)))
        #line_bot_api.push_message(data['房東ID'],FlexSendMessage("訂單確認",FLEX.order_consent(data)))
    
    if(post_input[0] == "取消訂單"):
        data = updata(post_input,user_id)
        firebase.setdata("所有訂單/"+post_input[1]+"/簽約人","房客取消")

        #line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='訂單顯示',contents = FLEX.order_FLEX(data, "訂單顯示")))
      
    if(post_input[0] == "簽約人正確"):
        firebase.setdata("所有訂單/"+post_input[1]+"/簽約人",post_input[2])
        
        data = updata(post_input,user_id)
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='訂單顯示',contents = FLEX.order_FLEX(data, "訂單顯示")))
    
    if(post_input[0] == "add_card"):
        try:
            order_number = firebase.getdata("user_info/"+user_id+"/所有訂單編號")
            print(list(order_number.values())[0])
            MAC = firebase.getdata("所有訂單/"+str(list(order_number.values())[0])+"/可使用所有鎖")
            print(list(MAC.values()))
            print(len(list(MAC.values())))
            if(len(list(MAC.values())) > 1 ):
                print("有好幾個鎖")

            else:
                print("只有一個鎖")
                lock_MAC = "lock-"+list(MAC.values())[0]
                payload = "add__card=" + reply_token + "=" + user_id
                print("payload = ",type(payload),payload)
                mqtt.client.publish(lock_MAC, payload)
                line_bot_api.reply_message(reply_token, TextSendMessage(text = "請在<大門>前掃卡"))
        except:
            line_bot_api.reply_message(reply_token, TextSendMessage(text = "沒有訂單無法新增卡片"))
    if(post_input[0] == "del_card"):
        firebase.setdata("user_info/"+user_id+"/卡片資訊","無")
        card_ID = firebase.getdata("user_info/"+user_id)["卡片資訊"]
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='查詢卡片',contents = FLEX.card(card_ID,user_id)))
        print(type(user_id),user_id)
        user_id = [user_id]
        print(type(user_id),user_id)
        updata_ALL_MAC_card(list(user_id),"del")



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=port)  
    