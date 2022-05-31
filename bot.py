import telebot
from io import BytesIO
from PIL import Image

# imports latest version of bincode
import requests
url = 'https://raw.githubusercontent.com/tusharhero/bincode/main/bincode.py'
bincode = requests.get(url)
open('bincode.py', 'wb').write(bincode.content)
import bincode as bc

# getting the API key
f = open("API_KEY")
API_KEY = f.read()

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

    txt = message.text[13:] # slicing to remove the command part from the text

    bincode = bc.txt2bincode(txt)
    # send it.
    bot.send_photo(chat_id, photo= bincode)

@bot.message_handler(
    content_types=[
        'image',
        'photo'
        ]
)

def send_txt(message):
    chat_id = message.chat.id

    file_info = bot.get_file(message.photo[-1].file_id)

    downloaded_file = bot.download_file(file_info.file_path)
    
    stream = BytesIO(downloaded_file)

    bincode = Image.open(stream).convert("1")
    
    txt = bc.bincode2txt(bincode)
    bot.send_message(
    chat_id, 
    txt
    )

bot.polling()