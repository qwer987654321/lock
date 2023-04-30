import threading
import time
import app
# 子執行緒的工作函數
def job(name):
  for i in range(3):
    print("Child thread:", i+1,name)
    time.sleep(1)
  try:
    app.line_bot_api.reply_message(name, app.TextSendMessage(text = "開門失敗"))
    print("傳送失敗")
  except:
     print("開門成功")

def thr(reply):
    # 建立一個子執行緒
    t = threading.Thread(target = job, args=(reply,))
# 執行該子執行緒
    t.start()

# 主執行緒繼續執行自己的工作
#for i in range(3):
#  print("Main thread:", i)
#  time.sleep(1)


# 等待 t 這個子執行緒結束
#t.join()
