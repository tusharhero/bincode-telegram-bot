import telebot
from io import BytesIO
from PIL import Image
import os

# imports latest version of bincode
import requests
url = 'https://raw.githubusercontent.com/tusharhero/bincode/main/bincode.py'
bincode = requests.get(url)
open('bincode.py', 'wb').write(bincode.content)
import bincode as bc



def send_except(
    reason,
    chat_id,
    ):
    print(reason)
    reason_message ="""
        Oops, an error occured!
        Possible reason: \n
        """ + reason
    bot.send_message(
        chat_id, 
        reason_message
        )
    

# getting the API key
#f = open("API_KEY")
#API_KEY = f.read()
API_KEY = os.environ['KEY']
print(API_KEY)
# declaring the bot with API key
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(
    commands=[
        'start',
        'help'
        ]
    )

def send_welcome(message):

    chat_id = message.chat.id

    welcome = """
    Hello there!
    To make a bincode out of your text:
    `/txt2bincode <your text here>`

    To read a bincode just send it!

    If you want to use the camera try your best to crop it!
    """

    bot.send_message(
    chat_id, 
    welcome,
    parse_mode="Markdown"
    )
@bot.message_handler(
    commands=[
        'txt2bincode'
        ]
    )

def send_bincode(message):
    chat_id = message.chat.id
    try:
        txt = message.text[13:] # slicing to remove the command part from the text

        bincode = bc.txt2bincode(txt)
        # send it.
        bot.send_photo(chat_id, photo= bincode)
    except:
        send_except("Text is too big", chat_id)


@bot.message_handler(
    content_types=[
        'image',
        'photo'
        ]
)

def send_txt(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.photo[-1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)
    
        stream = BytesIO(downloaded_file)

        bincode = Image.open(stream).convert("1")
        bincode = bc.correctbincode(bincode)
        txt = bc.bincode2txt(bincode)
        bot.send_message(
        chat_id, 
        txt
        )
    except:
        try:
            txt = "We couldn't convert it to text but here is the raw data \n" + str(bc.rdbincodeimg(bincode))
            bot.send_message(
                chat_id,
                txt
                )
        except:
            send_except("Image not bincode or not of correct size", chat_id)



bot.infinity_polling()