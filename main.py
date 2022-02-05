#!/usr/bin/python3

# Libraries
import threading
import time
import telegram
from traceback import print_tb
from humanfriendly import format_timespan as left
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Config
TOKEN = "token removed, got yours"

# Functions
def timer(second=0, minute=0, hour=0, end_msg:str="", chn=str):
    interval = second + (minute*60) + (hour*3600)  
    tmp = bot.send_message(chat_id=chn, text=f"{left(interval)} {end_msg}")

    while(interval>0):
        print(f"{left(interval)} left")
        time.sleep(30)
        interval -= 30
        if(interval > 0):
            tmp.edit_text(f"{left(interval)} {end_msg}")
        else:
            tmp.edit_text(f"0 seconds {end_msg}")

def sec(update, context):
    global toggeled

    if(toggeled):
        h, m, s, msg, chn = update.message.text.split(":")

        h = int(h)
        m = int(m)
        s = int(s)
        msg = msg.strip()
        chn = chn.strip()

        user = update.message.chat.username
        adminds = []

        ## Getting admins username
        for i in bot.get_chat_administrators(chat_id=chn):
            adminds.append(i.user.username)
        
        if(user in adminds):
            t = threading.Thread(target=timer, args=(s, m, h, msg, chn,))
            threads.append(t)
            t.start()
        else:
            update.message.reply_text("You are not the admin of this chat")

def start(update, context):
    global toggeled

    toggeled = True
    update.message.reply_text(
"""
Well, this bot will countdown until a specified interval for a channel or group.

Specify a exact interval to countdown.

# hour:minute:second:your message:@ChannelID

For example for one hour and 4 minute and 30 second:
1:0:30:to start meeting:@ChannelID
""")
    print(update.message.text)

def rg_chl(update, context):
    pass
    # global chn
    # chn = ""
    # chn = update.message.text.split(" ")[1]
    # update.message.reply_text("channel username registered")

# Start point
if __name__ == "__main__":
    print("Starting.")

    threads = list()
    toggeled = True

    bot = telegram.Bot(token=TOKEN)
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("regester", rg_chl))
    dispatcher.add_handler(MessageHandler(Filters.text, sec))

    updater.start_polling()
    updater.idle()
