#import firebase
#
#data1 = {"name6": "bb-bb-bb-bb"}
#
#firebase.getvaldata("aaaaa/card")

import random
import string
import app
import firebase

#A = ''.join(random.sample(string.ascii_letters + string.digits, 5))
#print(A)

firebase.setdata("user_info/U13c4146fdcf64e20e538ba3f1df08035/卡片資訊","SS-SS-SS-SS")
#card_ID = firebase.getdata("user_info/"+j[2])["卡片資訊"]
#app.line_bot_api.reply_message(j[1], FlexSendMessage(alt_text='查詢卡片',contents = FLEX.card(card_ID,user_id)))
#app.line_bot_api.reply_message(j[1], app.TextSendMessage(text = "新增成功"))
print("成功新增卡片")
#要把這個使用者有的鎖給新增至所有card裡，    還要再判斷訂單日期，在期限內的才要新增
order_number = firebase.getdata("user_info/U13c4146fdcf64e20e538ba3f1df08035/所有訂單編號")
print(list(order_number.values()))
for _order in list(order_number.values()):
    data = list(firebase.getdata("所有訂單/"+str(_order)+"/可使用所有鎖").values())
    landlord_ID = firebase.getdata("所有訂單/"+str(_order)).get("房東ID")
    print(data)
    print(landlord_ID)
    for upcard in data:
        firebase.setdata("user_info/"+landlord_ID+"/"+upcard+"/card"+"/U13c4146fdcf64e20e538ba3f1df08035","SS-SS-SS-SS")
        print(upcard)