import pyrebase
import time

config = {
  "apiKey": "AIzaSyCBJjlHRCgHSIAe2Y5ROmcrVaowQ4d_2cc",
  "authDomain": "esp32-lock-project.firebaseapp.com",
  "databaseURL": "https://esp32-lock-project-default-rtdb.firebaseio.com",
  "storageBucket": "esp32-lock-project.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


data = {"name": "Mortimer","name2": "chang","name3": "feng"}

def pushdata(path, data):
    db.child(path).push(data)

def setdata(path, data):
    db.child(path).set(data)

def updata(path, data):
    db.child(path).update(data)

def deldata(path):
    db.child(path).remove()

def getdata(path):
    try:
        data_key_val={}
        data_key = ""
        dara_val = ""
        user = db.child(path).get()
        for user in user.each():
            #print(user.key(),user.val())
            #print(type(user.key()),user.key())
            #print(type(user.val()),user.val())
            data_key += str(user.key())+"\n"
            dara_val += str(user.val())+"\n"
            data_key_val[str(user.key())] = str(user.val())
        #print("data_key = \n"+data_key)
        #print("dara_val = \n"+dara_val)
        #return data_key, dara_val
        return data_key_val
    except:
        return False

def getvaldata(path):
    try:
        data_val = []
        user = db.child(path).get()
        for user in user.each():
            #print(user.val())
            data_val.append(user.val())
        return data_val
    except:
        return False
    
def get_card_data(path):
    return db.child(path).get().val()


def CLIENT(path,data): #驗證用戶
    client = db.child(path).get()
    for i in client.each():
        print(i.key())
        print(i.val())
        if data == i.key():
            print("驗證成功!!!")
            return True
        else:
            print("驗證失敗...")
    return False

#card = getdata("user_info/U13c4146fdcf64e20e538ba3f1df08035")["卡片資訊"]
#print(type(card))
#print(card)
#order_number = getvaldata("user_info/U13c4146fdcf64e20e538ba3f1df08035/卡片資訊")
#print(order_number)

#time.sleep(5)

#n = getvaldata("所有訂單/uMJdq/可使用所有鎖")
#print(n)
  
#n = getdata("user_info/U13c4146fdcf64e20e538ba3f1df08035/卡片資訊")
#print(n)

#deldata("aaaaa/card","abc")

#users = db.child("landlord-2").child("lock-001").get()
#print(users.val())


#etag = db.child("users").child("Morty").get_etag()

#db.child("users").child("Morty").conditional_set(data, etag["ETag"])


#response = db.child("users").child("Morty").conditional_remove(etag["ETag"])
