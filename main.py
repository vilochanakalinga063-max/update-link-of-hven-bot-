import telebot
import os
import urllib.parse
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Direct Submission Bot Active"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# --- Settings ---
API_TOKEN = '8717215830:AAGbjq3i310-Fuf2rk5ifxS3ociKc6CaUGo' 
bot = telebot.TeleBot(API_TOKEN)

# පෝස්ට් එක වැටෙන්න ඕනේ චැනල් එකේ ID එක
MAIN_CHANNEL_ID = '-1003793313921' 

# යූසර්ට ශෙයා කරන්න දෙන ලින්ක් එක
MY_CHANNEL_PROMO_LINK = "https://t.me/+UwbKbKQ3Z9Y5NjE1"

MY_WEBSITE_URL = "https://merry-churros-da0304.netlify.app/?url="

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {'step': 'GET_LINK'}
    bot.reply_to(message, "👋 හරි දැන් ඔයාගේ Channel ලින්ක් එක එවන්න.")

@bot.message_handler(func=lambda message: True)
def handle_steps(message):
    user_id = message.from_user.id
    if user_id not in user_data: return

    state = user_data[user_id].get('step')

    if state == 'GET_LINK':
        if "t.me/" in message.text:
            user_data[user_id]['link'] = message.text.strip()
            user_data[user_id]['step'] = 'GET_NAME'
            bot.reply_to(message, "✅ දැන් ඒ චැනල් එකේ නම එවන්න.")
        else:
            bot.reply_to(message, "❌ වලංගු ලින්ක් එකක් එවන්න.")

    elif state == 'GET_NAME':
        display_name = message.text.strip()
        submitted_link = user_data[user_id]['link']
        
        bot.reply_to(message, f"🙌 හරි දැන් මේ මගේ චැනල් එකේ ලින්ක් එක ඔයාගේ ගෲප් එකේ ශෙයා කරන්න: {MY_CHANNEL_PROMO_LINK}\n\nවිනාඩි 10ක් හො 15ක් අතුලත ඔයා share කරපු එක බලල මන් මගෙ channel එකේ ඔයාගෙ link එක දාන්නම්.")
        
        # විනාඩි 13කින් කෙලින්ම චැනල් එකට පෝස්ට් කරනවා
        Thread(target=post_to_channel, args=(display_name, submitted_link)).start()
        del user_data[user_id]

def post_to_channel(name, link):
    # විනාඩි 13ක් බලා ඉන්නවා (පරීක්ෂා කිරීමට තත්පර 10ක් දාලා බලන්න)
    time.sleep(360) 
    
    final_web_link = f"{MY_WEBSITE_URL}{urllib.parse.quote(link, safe='')}"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"{link}", url=final_web_link))
    
    caption = f"📍 **{name}**\n\nLink here 👇"
    
    try:
        bot.send_message(MAIN_CHANNEL_ID, caption, reply_markup=markup, parse_mode="Markdown")
        print(f"✅ Posted directly to channel: {name}")
    except Exception as e:
        print(f"❌ Channel Posting Error: {e}")

if __name__ == "__main__":
    t = Thread(target=run)
    t.daemon = True
    t.start()
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
