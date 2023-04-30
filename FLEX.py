import firebase
#訂單
def order_FLEX(data ,model):
    # 這裡以下可以用if判斷是<訂單確認>還是<查詢訂單>
    # 如是<訂單確認>就顯示下面
    # 如是<查詢訂單>就多顯示簽約人是誰
    dict_lock_ava = eval(data['可使用所有鎖'])
    str_lock_ava = ""
    for i in dict_lock_ava:
      str_lock_ava = str_lock_ava + i + "\n"
    str_lock_ava = str_lock_ava.strip()
    if(model == "訂單確認"):
      footer = {
      "type": "box",
      "layout": "horizontal",
      "spacing": "sm",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "postback",
            "label": "同意",
            "data": "簽約同意-"+str(data['訂單編號'])
          }
        },
        {
          "type": "button",
          "action": {
            "type": "postback",
            "label": "取消",
            "data": "取消訂單-"+str(data['訂單編號'])
          }
        }
      ],
      "flex": 0
    }
    else:
      footer = ""
    text={
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "訂單 "+str(data['訂單編號']),
          "weight": "bold",
          "size": "xl"
        },
        {
          "type": "box",
          "layout": "vertical",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "box",
              "layout": "baseline",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "租約開始時間",
                },
                {
                  "type": "text",
                  "text": str(data['租約開始時間']),
                }
              ]
            },
            {
              "type": "box",
              "layout": "baseline",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "租約結束時間",
                },
                {
                  "type": "text",
                  "text": str(data['租約結束時間']),
                }
              ]
            },
            {
              "type": "box",
              "layout": "baseline",
              "contents": [
                {
                  "type": "text",
                  "text": "可使用鎖",
                },
                {
                  "type": "text",
                  "text": str_lock_ava,
                  "wrap": True
                }
              ]
            },
            {
              "type": "box",
              "layout": "baseline",
              "contents": [
                {
                  "type": "text",
                  "text": "分享人數限制",
                },
                {
                  "type": "text",
                  "text": str(data['分享人數限制']),
                }
              ]
            },
            {
              "type": "box",
              "layout": "baseline",
              "contents": [
                {
                  "type": "text",
                  "text": "簽約人",
                },
                {
                  "type": "text",
                  "text": str(data['簽約人']),
                }
              ]
            }
          ]
        }
      ]
    },
    "footer": footer
    }
    return text

#訂單同意書
def order_consent(data):
    return{
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "image",
              "url": str(data['LINE_image']),
              "size": "full",
              "aspectMode": "cover"
            }
          ],
          "cornerRadius": "100px",
          "width": "72px",
          "height": "72px",
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": str(data['LINE_name']),
              "size": "xxl"
            },
            {
              "type": "text",
              "text": "同意"+str(data['訂單編號'])+"訂單",
              "size": "xl"
            }
          ],
          "margin": "20px"
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "postback",
            "label": "簽約人正確",
            "data": "簽約人正確-"+str(data['訂單編號'])+"-"+str(data['LINE_name'])
          }
        },
        {
          "type": "button",
          "action": {
            "type": "postback",
            "label": "簽約人錯誤",
            "data": "拒絕-"+str(data['訂單編號'])
          }
        }
      ]
    }
  }

#訂單清單
def order_list(model, order_number):
  contents=[]
  for _order in order_number:
    data = firebase.getdata("所有訂單/"+str(_order))
    data.update({"訂單編號":_order})
    contents.append(order_FLEX(data ,model))
   
  text = {
  "type": "carousel",
  "contents": contents 
  }
  
  return text

#新增卡片
def card(card_ID,user_id):
  if(card_ID == "無"):
    card_ID = "無"
    footer = "新增卡片"
    footer_data = "add_card-"+user_id
  else:
    footer = "刪除"
    footer_data = "del_card-"+user_id
  text = {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "box",
              "layout": "baseline",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "ID：",
                  "color": "#aaaaaa",
                  "size": "xl",
                  "flex": 1
                },
                {
                  "type": "text",
                  "text": card_ID,
                  "color": "#666666",
                  "size": "xl",
                  "flex": 4
                }
              ]
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "spacing": "sm",
      "contents": [
        {
          "type": "button",
          "height": "sm",
          "action": {
            "type": "postback",
            "label": footer,
            "data": footer_data
          }
        }
      ],
    }
  }
  return text