import datetime
from io import BytesIO
import os
import requests
import telebot

token = os.environ.get('bot_token')

print('Telegram bot token is: ' + token)

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Cartoonizer redraws your picture in an anime-like style."
                                      "\n"
                                      "\nSend a picture to see."
                                      "\n"
                                      "\nYou can send it both compressed and without compression.")


@bot.message_handler(content_types=['photo'])
def photo_command(message):
    with open("/var/cartoonizer/logs.txt", "a", encoding='UTF-8') as logs:
        print(message.from_user, file=logs)
    photo_name = datetime.datetime.now().strftime('%d-%m-%yT%H-%M-%S') + '.jpg'
    file = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file.file_path)
    file_data = post_request(data={'name': photo_name}, files={'file': downloaded_file})
    file_buffer = BytesIO(file_data)
    bot.send_photo(chat_id=message.chat.id, photo=file_buffer)


@bot.message_handler(content_types=['document'])
def document_command(message):
    file_name = datetime.datetime.now().strftime('%d-%m-%yT%H-%M-%S')
    file = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file.file_path)
    file_extension = os.path.splitext(file.file_path)[1]
    file_data = post_request(data={'name': file_name + file_extension}, files={'file': downloaded_file})
    file_buffer = BytesIO(file_data)
    bot.send_document(chat_id=message.chat.id, document=file_buffer)


def post_request(data, files):
    url = 'http://127.0.0.1:5000/upload'
    message = requests.post(url, files=files, data=data)
    return message.content


bot.polling(none_stop=True)
