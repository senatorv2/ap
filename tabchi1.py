#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import util
import sys
import json
import os
import subprocess
import requests
import random
import urllib
import urllib2
import redis
import requests as req
reload(sys)
sys.setdefaultencoding("utf-8")
TOKEN = ''
bot = telebot.TeleBot(TOKEN)
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
db = "https://api.telegram.org/bot{}/getMe?".format(TOKEN)
#AFBOTS
f = "\n \033[01;30m Bot Firstname: {} \033[0m".format(bot.get_me().first_name)
u = "\n \033[01;34m Bot Username: {} \033[0m".format(bot.get_me().username)
i = "\n \033[01;32m Bot ID: {} \033[0m".format(bot.get_me().id)
c = "\n \033[01;31m Bot Is Online Now! \033[0m"
print(f + u + i + c)

@bot.message_handler(commands=['start'])
def start(m):
      id = m.from_user.id
      redis.sadd('seenchipy',id)
      redis.sadd('alls',id)
      bot.send_message(m.chat.id,'سلام',parse_mode='markdown')
	 
@bot.message_handler(commands=['panel'])
def panel(m):
    if m.from_user.id == 65761134 :
     markup = types.InlineKeyboardMarkup()
     c = types.InlineKeyboardButton("امار",callback_data='amar')
     markup.add(c)
     bot.send_message(m.chat.id, "پنل مدریتی", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['fwdall'])
def fwdall(m):
    if m.from_user.id == 65761134 :
        if m.reply_to_message:
            mid = m.reply_to_message.message_id
            ids = redis.smembers('alls')
            for id in ids :
                try:
                    bot.forward_message(id,m.chat.id,mid)
                except:
                    redis.srem('alls',id)	
		
@bot.message_handler(commands=['bc'])
def clac(m):
    if m.from_user.id == 65761134 :
        text = m.text.replace("/bc ","")
        rd = redis.smembers('alls')
        for id in rd:
            try:
                bot.send_message(id, "{}".format(text), parse_mode="Markdown")
            except:
                redis.srem('alls', id)
		
@bot.message_handler(content_types=['new_chat_member'])
def new_member(m):
     id = m.chat.id
     redis.sadd('chatpys',id)
     redis.sadd('alls',id)
	  
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
 if call.message: 
     if call.data == "amar":
       markup = types.InlineKeyboardMarkup()
       c = types.InlineKeyboardButton("بروز رسانی",callback_data='amar')
       markup.add(c)
       usrs = str(redis.scard('seenchipy'))
       cha = str(redis.scard('chatpys'))
       tex = 'تعداد کاربران : {}\nتعداد گروه: {}'.format(usrs,cha)
       bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = tex, reply_markup=markup, parse_mode='Markdown')

bot.polling(True)
#By: @soheildkta