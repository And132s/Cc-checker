#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CODED BY @XD-ADISINGH
# KINDLY GIVE CREDITS 
# DONT MISUSE
# THANK YOU
import logging
import os
import sys
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import re
from luhn import *
import pymongo

# WORKS LIKE FIRE

'''
This bot is developed by @XD_SHIVAY Lol
it is the first version deployed for public scraping,
now it is an Waste version for my work environment, 
that's why I post it for Open source


---------------Deploy on Heroku

-ENV keys: 
	-TOKEN: 123:ABC
	- MODE: prod
	- CHAT_ID_FORWARD: -1111
	- HEROKU_APP_NAME: (HEROKU APP NAME)
'''


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

client = pymongo.MongoClient(
	
	)# MONGO DB LINK 
db = client.credit_cards

developers = ['5428236702', '5595023466']


addusr = ""
tk = os.getenv("TOKEN")
mode = os.getenv("MODE")

posting_channel = os.getenv("CHAT_ID_FORWARD")

if mode == "dev":
	def run(updater):
		updater.start_polling()
		updater.idle()
elif mode == "prod":
	def run(updater):
		PORT = int(os.environ.get("PORT", "8443"))
		HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
		updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=tk)
		updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/"+ tk)
else:
	sys.exit()


def start(update, run_async):
	update.message.reply_text("ᴛʜɪs ᴄᴄ sᴄʀᴀᴘᴇʀ ʜᴀs ʙᴇᴇɴ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ | ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ @XD_SHIVAY")

def extrct(update, context):
	print('check channel id')
	#global chat_id
	gex = ['-11111111111'] #To exclude groups from scraping
	
	try:
		chat_id = str(telegram.Chat)
		#global chat_id
	except:
	   pass
	   chat_id = str(telegram.Chat)
	   if chat_id == posting_channel:	
		   rawdata = update.message.text
filtron = "[0-9]{16}[|][0-9]{1,2}[|][0-9]{2,4}[|][0-9]{3}"
filtroa = "[0-9]{15}[|][0-9]{1,2}[|][0-9]{2,4}[|][0-9]{4}"
detectavisa = "[0-9]{16}"
detectamex = "[0-9]{15}"
print('I am here')
try:
				try:
					sacanumvisa = re.findall(detectavisa, rawdata)
					carduno = sacanumvisa[0]
					tipocard = str(carduno[0:1])
				except:
					sacanumamex = re.findall(detectamex, rawdata)
					carduno	= sacanumamex[0]
					tipocard = str(carduno[0:1])
				if tipocard == "3":
					x = re.findall(filtroa, rawdata)[0]
				elif tipocard == "4":
					x = re.findall(filtron, rawdata)[0]
				elif tipocard == "5":
					x = re.findall(filtron, rawdata)[0]
				elif tipocard == "6":
					x = re.findall(filtron, rawdata)[0]
				
				check_if_cc = db.credit_card.find_one({'cc_num': x.split("|")[0]})
				try:
					card_exist_indb = str(check_if_cc['cc_num'])
					existe = True
				except:
					existe = False

				check_luhn = verify(x.split("|")[0])

				if existe is False:
					if check_luhn is True:
						
						cc_data = {
							"bin": x.split("|")[0][:6],
							"cc_full": x,
							"cc_num": x.split("|")[0]
						}
						db.credit_card.insert_one(cc_data)
						print('CArd check')
						print(x)
						card_send_formatted = f'''
CC: {x}
(C) @XD_SHIVAY
						'''
						hey = '''I checked cards'''

						context.bot.send_message(
							chat_id=posting_channel,
							text=card_send_formatted,
							parse_mode='HTML'
						)
						context.bot.send_message(
							chat_id=posting_channel,
							text=hey,
							parse_mode='HTML'
						)
except:
				pass
def main():

	updater = Updater(tk, use_context=True)


	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(MessageHandler(Filters.text, extrct,run_async=True))
	run(updater)


if __name__ == '__main__':
	main()
	print('started')
