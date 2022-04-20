
from datetime import datetime, timedelta
from dingtalkchatbot.chatbot import DingtalkChatbot

def send_msg(msg, title='TEST', mobiles=['15501267660'], TOKEN=None):
    DINGTALK_URL = 'https://oapi.dingtalk.com/robot/send?access_token='
    if TOKEN is None:
        print(11)
        TOKEN = 'fc3fbd95e6cd46bc44066940fbbfd80e1bc370aa26fa871c270796f3c659c903'

    rb = DingtalkChatbot(DINGTALK_URL+TOKEN)
    rb.send_markdown(
        title=title, 
        text= f'### [{title}]\n'
            f'> #### {msg}\n\n'
            f'> ###### {datetime.now().isoformat()}\n',
            at_mobiles=mobiles)

if __name__ == '__main__':
    send_msg('test: haha', title='TFT RETRAIN')