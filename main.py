#!/usr/bin/python3

from ast import arg
import threading
import time
from humanfriendly import format_timespan as left
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

print('starting.')

# just get a token from telegram and put it here
token = ""



# chn = None
toggeled = True
# interval = 1

def timer(second=0, minute=0, hour=0, end_msg:str='', chn=str) -> None:
    
    interval = second + (minute*60) + (hour*3600)  
    
    # tmp = updater.message.reply_text(f'{left(interval)} {end_msg}', chat_id=chn)
    bot = telegram.Bot(token=token)
    tmp = bot.send_message(chat_id=chn, text=f'{left(interval)} {end_msg}')
    
    while(interval>0):
        
        print(f'{left(interval)} left')
        time.sleep(30)
        interval -= 30
        if(interval > 0):
            tmp.edit_text(f'{left(interval)} {end_msg}')
        else:
            tmp.edit_text(f'0 seconds {end_msg}')

    

threads = list()

def sec(update, context):
    global toggeled
    if(toggeled):
        x = update.message.text
        h, m, s, msg, chn = x.split(':')
        # timer(int(s), int(m), int(h), end_msg=msg, updater=update, chn=chn)
        
        h = int(h)
        m = int(m)
        s = int(s)
        
        t = threading.Thread(target=timer, args=(s, m, h, msg, chn,))
        threads.append(t)
        t.start()


def start(update, context):
    global toggeled
    toggeled = True
    update.message.reply_text(
"""
well, this bot will countdown to a specified time for you. just send the time.

at first you should register your channel, then add this bot to your channel.

specify a exact interval to countdown.
1st column is hour, 2st is minute, 3th column is second, 4th column is for message and the last column is for the channel you want to send the countdown to.;

# hour:minute:second:your message
for example for one hour and 4 minute and 30 second:

1:0:30:to start meeting:@ChannelName
""")
    print(update.message.text)


def rg_chl(update, context):
    pass
    # global chn
    # chn = ''
    # chn = update.message.text.split(' ')[1]
    # update.message.reply_text("channel username registered")



updater = Updater(token)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("regester", rg_chl))
dispatcher.add_handler(MessageHandler(Filters.text, sec))

updater.start_polling()

updater.idle()

