#------------mqtt----------------
import paho.mqtt.client as mqtt
#import ast
import app
import firebase

def delay_time():
    print("30秒後")
    

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時 
    # 地端程式將會重新訂閱
    client.subscribe("locks")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    print(msg.topic+" "+ msg.payload.decode('utf-8'))
    #msg_dict = ast.literal_eval(msg.payload.decode('utf-8'))
    #print("msg_dict = ",msg_dict)
    try:
        mqtt_data = msg.payload.decode('utf-8').split("-")
        print(mqtt_data)
        if(mqtt_data[0] == "open_door"):
            app.line_bot_api.reply_message(mqtt_data[1], app.TextSendMessage(text = "成功開門"))
            print("成功傳送")
        if(mqtt_data[0] == "add__card"):
            print("開始新增卡片")
            firebase.setdata("user_info/"+mqtt_data[2]+"/卡片資訊",mqtt_data[3])
            #card_ID = firebase.getdata("user_info/"+mqtt_data[2])["卡片資訊"]
            #app.line_bot_api.reply_message(mqtt_data[1], FlexSendMessage(alt_text='查詢卡片',contents = FLEX.card(card_ID,user_id)))
            #app.line_bot_api.reply_message(mqtt_data[1], app.TextSendMessage(text = "新增成功"))
            print("成功新增卡片")
            del mqtt_data[0:2]
            print(mqtt_data)
            app.updata_ALL_MAC_card(mqtt_data,"add")

    except:
        return
# 初始化地端程式
client = mqtt.Client()    
# 設定連線的動作
client.on_connect = on_connect
# 設定接收訊息的動作
client.on_message = on_message
# 設定登入帳號密碼
client.username_pw_set("user","password")
# 設定連線資訊(IP, Port, 連線時間)
client.connect("broker.emqx.io", 1883, 60)

client.loop_start()
#------------mqtt----------------