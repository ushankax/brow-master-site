import requests
import environ

env = environ.Env()
environ.Env.read_env()


def telegram_bot_sendtext(bot_message):
    bot_token = env('bot_token')
    bot_chat_id = env('bot_chat_id')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id +\
                '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)

    return response.json()
