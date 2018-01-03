import sys
import telegram
from flask import Flask,request
from fsm import stockMachine

import twstock

import time


app=Flask(__name__)
bot=telegram.Bot(token='491933444:AAHULAo8FE3crybP3YBAw0mmpEnGs1sA-lc')
machine = stockMachine(
					   states=[
							   'modeSelection',
							   'stock',
							   'currency'
							   'makeOrder'
							   ],
					   transitions=[
									{
									'trigger': 'stockTermsTriggered',
									'source': 'modeSelection',
									'dest': 'stock',
									
									},
									{
									'trigger': 'currencyTermsTriggered',
									'source': 'modeSelection',
									'dest': 'currency',
									},
									{
									'trigger': 'currencyTermsTriggered',
									'source': 'stock',
									'dest': 'currency'
									},
									{
									'trigger': 'stockTermsTriggered',
									'source': 'currency',
									'dest': 'stock'
									},
									{
									'trigger': 'buy',
									'source': 'stock',
									'dest': 'order'
									},
									{
									'trigger': 'cancel',
									'source': 'order',
									'dest': 'stock'
									},
									{
									'trigger': 'orderConfirmed',
									'source': 'order',
									'dest': 'modeSelection'
									}
									],
					   initial='modeSelection',
					   auto_transitions=False,
					   show_conditions=True,
					   )

helpPhrases=('how to','help','how to use','instruction','who are you')
modePhrases=('stock','currency','fx','foreign exchange')
stockPhrases=('stock','stock market','stock',' price','price','open','high','low','volume')
stockTechPhrases=('price','open','high','low','volume')
stockTechInfo=(1,0,0,0,0)
currencyPhrases=('currency','fx','foreign exchange')
currencyTechPhrases=('currency')
buyPhrases=('buy','get')



def setWebhook():
	status=bot.set_webhook('https://5c0dfd60.ngrok.io/hook')
	if not status:
		print('Webhook setup failed')
		sys.exit(1)



@app.route('/hook',methods=['POST'])
def webhookResponse():
	if request.method=="POST":
		update=telegram.Update.de_json(request.get_json(force=True),bot)
		text=update.message.text

		

		text=stateDecision(text)
		
		
		update.message.reply_text(text)
	
	
	return 'ok'


def stateDecision(txt):
	global wordComposition
	global mode
	global stockTechInfo
	global currentStock,name,price
	wordComposition=txt.split()
	
	determineUnknownWords()
	
	respond='ok'
	
	if txt=='initialization':
		mode=1
		respond='Please tell me what you want to know. (ex: stock, currency...)'
		return respond
	
	if mode==1 :
		if findInString(txt,stockPhrases) :
			if findInString(txt,stockTechPhrases) :
				mode=4
				stockTechInfo=list(stockTechInfo)
				for a in range(0,len(stockTechPhrases)-1):
					if txt.find(stockTechPhrases[a]) == -1:
						stockTechInfo[a]=0
					else:
						stockTechInfo[a]=1
				stockTechInfo=tuple(stockTechInfo)
				if len(unknownWords)==0:
					respond='Which stock you want to know? (ex: 2330, 2311, 1504...)'
				else:
					respond=checkStock(unknownWords[0],stockTechInfo)
					currentStock=unknownWords[0]
				mode=2
			else:
				mode=2
				respond='Which stock you want to know? (ex: 2330, 2311, 1504...)'
				#ask which market
		
		elif findInString(txt,currencyPhrases) :
			if findInString(txt,currencyTechPhrases) :
				mode=5
				respond='Currency is currently unavailable.'
				mode=1
			else:
				mode=3
				respond='Currency is currently unavailable.'
				mode=1
	
		else:
			respond='Please tell me what you want to know. (ex: stock, currency...)'
				
				
	elif mode==2 :
		if findInString(txt,currencyPhrases):
			mode=5
			respond='Currency is currently out of service.'
			mode=1
		elif findInString(txt,buyPhrases):
			respond="Buy %s %s at price %s for how many shares?" % (currentStock,name,price)
			mode=6
		
		elif findInString(txt,stockTechPhrases):
			stockTechInfo=list(stockTechInfo)
			for a in range(0,len(stockTechPhrases)-1):
				if txt.find(stockTechPhrases[a]) == -1:
					stockTechInfo[a]=0
				else:
					stockTechInfo[a]=1
			stockTechInfo=tuple(stockTechInfo)
			if len(unknownWords)==0:
				respond='Which stock you want to know? (ex: 2330, 2311, 1504...)'
			else:
				respond=checkStock(unknownWords[0],stockTechInfo)
				currentStock=unknownWords[0]
			mode=2
		else:
			stockTechInfo=(1,1,1,1,1)
			if len(unknownWords)==0:
				respond='Which stock you want to know? (ex: 2330, 2311, 1504...)'
			else:
				respond=checkStock(unknownWords[0],stockTechInfo)
				currentStock=unknownWords[0]
			mode=2

	elif mode==5 :
		if findInString(txt,stockPhrases):
			mode=2
		else:
			findInString(txt,currencyTechPhrases)
			respond='Currency is currently unavailable.'
			mode=1

	elif mode==6:
		if findInString(txt,('cancel','quit','give up','no','negative','cancelling')):
			respond='Order CANCELED'
			mode=1
		else:
			respond="Order Confirmed: Buy in %s %s for %s shares at %s per share. Total cost is $%.2f" % (currentStock,name,unknownWords[0],price,float(float(unknownWords[0])*float(price)))
			mode=1

	

	
	
	
	return respond

def determineUnknownWords():
	global unknownWords
	unknownWords=[]
	for a in wordComposition:
		if (a in lexicalDatabase) == False:
			unknownWords.append(a)

	return 'ok'

def findInString(str,target):
	yesOrNo=False
	for a in target:
		if str.find(a) != -1:
			yesOrNo=True
					
	return yesOrNo


def checkStock(stockNumber,stockInfo):
	stock=twstock.realtime.get(stockNumber)
	global name,price
	name=stock['info']['name']
	price=stock['realtime']['latest_trade_price']
	respond="%s %s" % (name,stockNumber)
	
	if stockInfo[0]:
		respond="%s, the latest price is %s" % (respond,price)
	if stockInfo[1]:
		open=stock['realtime']['open']
		respond="%s, open is %s" % (respond,open)

	if stockInfo[2]:
		high=stock['realtime']['high']
		respond="%s, highest is %s" % (respond,high)

	if stockInfo[3]:
		low=stock['realtime']['low']
		respond="%s, lowest is %s" % (respond,low)

	if stockInfo[4]:
		volume=stock['realtime']['accumulate_trade_volume']
		respond="%s, volume is %s" % (respond,volume)

	respond="%s." %respond

	return respond


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
	byte_io = BytesIO()
	machine.graph.draw(byte_io, prog='dot', format='png')
	byte_io.seek(0)
	return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')



if __name__ == "__main__":
	global lexicalDatabase
	lexicalDatabase=[]
	global wordComposition
	wordComposition=[]
	global unknownWords
	unknownWords=[]
	global mode
	mode=1
	
	with open("Lexical Database/web2","r") as ins:
		lexicalDatabase=ins.readlines()
	lexicalDatabase=[x.strip() for x in lexicalDatabase]


	setWebhook()
	app.run()
