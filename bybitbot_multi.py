import bybit
import datetime
from datetime import datetime
import decimal
import time, requests, json
import telebot
from telebot import types
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import tweepy
import pymysql.connections
bot = telebot.TeleBot("1279865343:AAFnt3irzahq6qABMITEf8tAgRJz1Y2EMAQ")
client = bybit.bybit(test=False, api_key="kJpsWCHrHqo2CkkrRz", api_secret="zfAADNVJYm1gOzQEBiMdU4PW0vWPQ6SkDPn2")
btcprice = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]


def start():

    respx1 = requests.get('https://hexeba.com/vbotout.php')
    dataxx = respx1.json()
    bin15 = dataxx[0]['bin15']
    deci15 = dataxx[0]['deci15']
    
 #   #print(dataxx[0]['state'])
    entry = dataxx[0]['entry']
    state = dataxx[0]['state']
  #  state = "open"
    position = dataxx[0]['position']
   # if((state=="open")and(position=="long")):
    if((state=="open")and(position=="long")):
        Trade.openlong(bin15,deci15,entry,state,position)        
    if((state=="open")and(position=="short")):
        Trade.openshort(bin15,deci15,entry,state,position)


    respxx2 = requests.get('https://hexeba.com/hbot/lastuserout.php')
    dataxxz = respxx2.json()
    entryz = dataxxz[0]['entry']
    statez = dataxxz[0]['state']
    positionz = dataxxz[0]['position']
    if((state=="closed")):
        closeposition(bin15,deci15,entryz,statez,positionz)
 #   if(state=="closed"):
 #       nil()


def user_data():
    admincode = "1iloveJesus"
    resp1 = requests.get('https://hexeba.com/hbot/users.php?admincode='+str(admincode))
    datax = resp1.json()

    respx1 = requests.get('https://hexeba.com/hbot/lastuserout.php')
    dataxx = respx1.json()
    last = int(dataxx[0]['last'])+1

    time.sleep(2)
    p = len(datax)
    
    if(last == p):
        last = 0
        for j in range(last, p):
            fullname = datax[j]['fullname']
            email = datax[j]['email']
            paid = datax[j]['paid']
            exchange = datax[j]['exchange']
            apikey1 = datax[j]['apikey1']
            apikey2 = datax[j]['apikey2']
            statez = datax[j]['state']
            total = datax[j]['total']
            balance = datax[j]['balance']
            chatid = datax[j]['chatid']
            control = datax[j]['control']
            startbal = datax[j]['startbal']

            last = j



class Trade:

    def __init__(self,fullname,email,paid,exchange,apikey1,apikey2,statez,total,balance,chatid,control,startbal):
        self.fullname = fullname
        self.email = email
        self.paid = paid
        self.exchange = exchange
        self.apikey1 = apikey1
        self.apikey2 = apikey2
        self.statez = statez
        self.total = total
        self.balance = balance
        self.chatid = chatid
        self.control = control
        self.startbal = startbal

    def openlong(self,bin15,deci15,entry,state,position):

        respx1 = requests.get('https://hexeba.com/hbot/lastuserout.php')
        dataxx = respx1.json()
    #   #print(dataxx[0]['last'])
        last = int(dataxx[0]['last'])+1
        lastsuccess = dataxx[0]['success']
        lastcid = dataxx[0]['chatid']
        exchange = dataxx[0]['exchange']
        if(lastsuccess == "no"):
            messagey = "THERE WAS AN ERROR OPENING TRADE FOR YOUR "+exchange.upper()+" ACCOUNT\nIF THIS MESSAGE PERSISTS PLEASE CONTACT @victor_hexeba FOR SUPPORT"
        #   bot.send_message(str(lastcid), messagey)

        

        bin15 = bin15
        deci15 = deci15
        entry = entry
        state = state
        position = position
                    
        success = "no"
        date = datetime.now()
        b = requests.post("https://hexeba.com/hbot/lastuser.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(chatid)+'&exchange='+exchange+'&entry='+str(entry)+'&position='+position)
        #print(b.text)



        if((self.paid=="yes")and(self.exchange=="Bybit")and(self.control=="on")):




    #     if(exchange=="Bybit"):
            #print("IN")

            #print("IN USER "+fullname.upper())
            client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
            btcprice = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
            positionsx = client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]['side']
            
            #print("IN2")
            
            if(positionsx == "None"):
                
                client.Positions.Positions_saveLeverage(symbol="BTCUSD", leverage="15").result()
                
                walletbalance = client.Wallet.Wallet_getBalance(coin="BTC").result()[0]['result']['BTC']['available_balance']# get wallet balance
                
                #print("IN4")
                currentwallbal = float(walletbalance) * float(btcprice)

                leverage = 15
                
                val = float(leverage) * float(btcprice)
                contractsize = int(float(walletbalance) * (10 /  100) * val)
                entry = btcprice
                total = int(total) + 1
                date = datetime.now()
                
                client.Order.Order_new(side='Buy',symbol="BTCUSD",order_type="Market",qty=contractsize,time_in_force="GoodTillCancel").result()
                if((startbal == "")or(int(startbal)==0)):
                    b = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(currentwallbal)+'&chatid='+str(self.chatid))
    #               
                else:
                    b = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    

        #        messaget = str("***TESTING YOUR BOT FOR TRADE ACTIVITIES***\n\nPLEASE IF BALANCE IS NOT ACCURATE THEN CONVERT USDT TO BTC AS THE BOT WORKS WITH BYBIT INVERSE PERP\n\n*********LONG SCALP POSITION OPENED FOR "+str(fullname) +"*******\nExchange: Bybit\nSymbol: $BTC\nENTRY PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nStarting Balance: $" + str(startbal) + "\nCurrent Balance: $" + str(balance) + "\nDate: " + date + "\nDM @victor_hexeba for any form of assistance. ")
                
                messagex = str("\n*********LONG SCALP POSITION OPENED FOR "+str(self.fullname.upper()) +"*******\nExchange: Bybit\nSymbol: $BTC\nENTRY PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nStarting Balance: $" + str(startbal) + "\nCurrent Balance: $" + str(self.balance) + "\nDate: " + str(date) + "\nDM @victor_hexeba for any form of assistance. ")
                bot.send_message(str(self.chatid), messagex)
                #print("HXXXXX")
                last = j
                success = "yes"
                b = requests.post("https://hexeba.com/hbot/lastuser.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                #print(b.text)
            if((positionsx=='Buy')or(positionsx=='Sell')):
                bin15 = str(j)
                last = j
                deci15 = "x"
                entryz = entry
                statez = state
                positionz = position
                
                closeposition(bin15,deci15,entryz,statez,positionz)
            #   #print(entry)


    def openshort(self,bin15,deci15,entry,state,position):

        respx1 = requests.get('https://hexeba.com/hbot/lastuserout.php')
        dataxx = respx1.json()
    #   #print(dataxx[0]['last'])
        last = int(dataxx[0]['last'])+1
        lastsuccess = dataxx[0]['success']
        lastcid = dataxx[0]['chatid']
        exchange = dataxx[0]['exchange']
        if(lastsuccess == "no"):
            messagey = "THERE WAS AN ERROR OPENING TRADE FOR YOUR "+self.exchange.upper()+" ACCOUNT\nIF THIS MESSAGE PERSISTS PLEASE CONTACT @victor_hexeba FOR SUPPORT"
        #   bot.send_message(str(lastcid), messagey)

        

        bin15 = bin15
        deci15 = deci15
        entry = entry
        state = state
        position = position
        
        success = "no"
        date = datetime.now()
        b = requests.post("https://hexeba.com/hbot/lastuser.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(chatid)+'&exchange='+exchange+'&entry='+str(entry)+'&position='+position)
        #print(b.text)



        if((self.paid=="yes")and(self.exchange=="Bybit")and(self.control=="on")):




    #     if(exchange=="Bybit"):
            #print("IN")

            #print("IN USER "+fullname.upper())
            client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
            btcprice = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
            positionsx = client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]['result']['side']
            

            if((positionsx)=="None"):
                
                client.Positions.Positions_saveLeverage(symbol="BTCUSD", leverage="14").result()
                
                walletbalance = client.Wallet.Wallet_getBalance(coin="BTC").result()[0]['result']['BTC']['available_balance']  # get wallet balance

                currentwallbal = float(walletbalance) * float(btcprice)
        
                leverage = 15
                val = float(leverage) * float(btcprice)
                contractsize = int(float(walletbalance) * (10 /  100) * val)
                entry = btcprice
                total = int(total) + 1 
                date = datetime.now()
                client.Order.Order_new(side='Sell',symbol="BTCUSD",order_type="Market",qty=contractsize,time_in_force="GoodTillCancel").result()
                if((startbal == "")or(int(startbal)==0)):
                    b = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(currentwallbal)+'&chatid='+str(self.chatid))
        #               
                else:
                    b = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                        

        #        messaget = str("***TESTING YOUR BOT FOR TRADE ACTIVITIES***\n\nPLEASE IF BALANCE IS NOT ACCURATE THEN CONVERT USDT TO BTC AS THE BOT WORKS WITH BYBIT INVERSE PERP\n\n*********LONG SCALP POSITION OPENED FOR "+str(fullname) +"*******\nExchange: Bybit\nSymbol: $BTC\nENTRY PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nStarting Balance: $" + str(startbal) + "\nCurrent Balance: $" + str(balance) + "\nDate: " + date + "\nDM @victor_hexeba for any form of assistance. ")
                
                messagex = str("\n*********SHORT SCALP POSITION OPENED FOR "+str(self.fullname.upper()) +"*******\nExchange: Bybit\nSymbol: $BTC\nENTRY PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nStarting Balance: $" + str(startbal) + "\nCurrent Balance: $" + str(self.balance) + "\nDate: " + str(date) + "\nDM @victor_hexeba for any form of assistance. ")
                bot.send_message(str(self.chatid), messagex)
                #print("HXXXXX")
                last = j
                success = "yes"
                b = requests.post("https://hexeba.com/hbot/lastuser.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                #print(b.text)
            if((positionsx=='Buy')or(positionsx=='Sell')):
                bin15 = str(j)
                last = j
                deci15 = "x"
                entryz = entry
                statez = state
                positionz = position
                closeposition(bin15,deci15,entryz,statez,positionz)



        self.fullname = fullname
        self.email = email
        self.paid = paid
        self.exchange = exchange
        self.apikey1 = apikey1
        self.apikey2 = apikey2
        self.statez = statez
        self.total = total
        self.balance = balance
        self.chatid = chatid
        self.control = control
        self.startbal = startbal


    def closeposition(self,bin15,deci15,entryz,statez,positionz):
        #print("MAINBOT POSITION IS CLOSED")
        bin15 = bin15
        deci15 = deci15
        entry = entryz
        
        state1 = statez
        
        position = positionz
        respx1 = requests.get('https://hexeba.com/vbotout.php')
        dataxx = respx1.json()
        time.sleep(2)
        
    #   #print(dataxx[0]['state'])
        state2 = dataxx[0]['state']
        spy = dataxx[0]['spy']
        spyentry = dataxx[0]['spyentry']
        
        #print(btcprice)
        
        entry = float(entry)
        
        
        pnl = float(btcprice) - entry
        #print("HERE")
        #print(pnl)
        tp = (1/100)*float(btcprice)
        tp2 =  (0.5/100)*float(btcprice)
        sl = (2/100)*float(btcprice)
        sl2 = (0.5/100)*float(btcprice)
        pp = 10/100
        pp2 = 5/100
        pl = 10/100
        pl2 = 5/100
        
        
        if(4>1):
            
            
            respx1 = requests.get('https://hexeba.com/hbot/lastuserout.php')
            dataxx = respx1.json()
        #   #print(dataxx[0]['last'])
            if(str(deci15) == "x"):
                last = int(bin15)
            else:

                last = int(dataxx[0]['last']) + 1
            
            lastsuccess = dataxx[0]['success']
            lastcid = dataxx[0]['chatid']
            lastexchange = dataxx[0]['exchange']
            
            if(lastsuccess == "no"):
                messaget = "THERE WAS AN ERROR CLOSING TRADE FOR YOUR "+lastexchange.upper()+" ACCOUNT\nPLEASE VISIT YOUR EXCHANGE NOW TO CLOSE TRADE MANUALLY \n IF THIS MESSAGE PERSISTS PLEASE CONTACT @victor_hexeba FOR SUPPORT"
        #        bot.send_message(str(lastcid), messaget)


            if((self.paid=='yes')and(self.exchange=="Bybit")and(self.control=="on")):
                
                
                
    #        if(exchange=="Bybit"):
                
                client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                
                
#               lastposition = client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]['result']['side']
#               ##print("HEREYYY")
#              lastentry = client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["entry_price"]
#              if(lastposition == 'Buy'):
#                 position = "long"
    #            if(lastposition == 'Sell'):
    #               position = "short"
                ##print("jhdfjgasdfgafsghaf")
                entry = client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["entry_price"]
                ##print("jhdfjgasdfgafsghaf")

                pnl = float(btcprice) - float(entry)
                ##print("HERE")
                ##print(pnl)
                tp = (1/100)*float(btcprice)
                tp2 =  (0.5/100)*float(btcprice)
                sl = (2/100)*float(btcprice)
                sl2 = (0.5/100)*float(btcprice)
                pp = 10/100
                pp2 = 5/100
                pl = 10/100
                pl2 = 5/100
                
                ##print(str(apikey1))
                ##print(str(email))
                date = datetime.now()
                
                
                last = j
                success = "no"
                state = "closed"
                b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                ##print(b.text)
                #print("HEREYY")
                
                lastposition = client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]['result']['side']
                #print("HEREzzzzzzzzzz")

                #print("IN "+fullname.upper())
                #print("WE ARE IN IN X")
                #LONG TAKE PROFIT 1
                if((lastposition == 'Buy')and(pnl >= tp)):
                    

                    date = datetime.now()
                    last = j
                    success = "no"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



        #        if((position=="long")and(state == "open")):
                    client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                    #print("here1")
                    consize = int(client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["size"])
                    client.Order.Order_new(side='Sell', symbol="BTCUSD", order_type="Market", qty=consize,time_in_force="GoodTillCancel").result()
                    time.sleep(2)
                    walletbalance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['available_balance']  # get wallet balance
            #       walletbalance = "90000"
                    time.sleep(2)
                    #print("here2")
                    endprice2 = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
                    currentwallbal = float(walletbalance) * float(endprice2)
                    #print("here3")
                    state = "closed"
                    date = datetime.now()
                    b = requests.post("https://hexeba.com/hbot/closedata.php?entry="+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&chatid='+str(self.chatid))
                    
                    c = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    
                    messagex = str(
                            "*********TOOK PROFIT FOR BTC LONG POSITION*******\nExchange: Bybit\nENTRY PRICE: $" + str(entry) + "\nEXIT PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nPrevious Balance: $" + str(
                                balance) + "\nNew Balance: $" + str(currentwallbal) + "\nDate: " + str(
                                date) + "\nDM @victor_hexeba for inquiry. ")
                    bot.send_message(self.chatid, messagex)
            #      #print("TESTING")

                    date = datetime.now()
                    last = j
                    state = "closed"
                    success = "yes"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)




                #LONG TAKE PROFIT 2
                if((lastposition=='Buy')and(spy=="short")and(pnl >= tp2)):

                    date = datetime.now()
                    last = j
                    success = "no"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)

    #         if((position=="long")and(state == "open")):
                    client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                #  #print("here1")
                    consize = int(client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["size"])
                    client.Order.Order_new(side='Sell', symbol="BTCUSD", order_type="Market", qty=consize,time_in_force="GoodTillCancel").result()
                    time.sleep(2)
                    walletbalance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['available_balance']  # get wallet balance
            #       walletbalance = "90000"
                    time.sleep(2)
                    #print("here2")
                    endprice2 = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
                    currentwallbal = float(walletbalance) * float(endprice2)
                    #print("here3")
                    state = "closed"
                    date = datetime.now()
                    b = requests.post("https://hexeba.com/hbot/closedata.php?entry="+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&chatid='+str(self.chatid))
                    
                    c = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    

                    messagex = str(
                            "*********TOOK PROFIT FOR BTC LONG POSITION*******\nExchange: Bybit\nENTRY PRICE: $" + str(entry) + "\nEXIT PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nPrevious Balance: $" + str(
                                balance) + "\nNew Balance: $" + str(currentwallbal) + "\nDate: " + str(
                                date) + "\nDM @victor_hexeba for inquiry. ")
                    bot.send_message(chatid, messagex)
                #    #print("TESTING")

                    date = datetime.now()
                    last = j
                    state = "closed"
                    success = "yes"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)


                #STOPLOSS LONG 1
                if((lastposition=='Buy')and(pnl <= -sl)):

                    date = datetime.now()
                    last = j
                    success = "no"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



            #    if((position=="long")and(state == "open")):
                    client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                    #print("here1")
                    consize = int(client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["size"])
                    client.Order.Order_new(side='Sell', symbol="BTCUSD", order_type="Market", qty=consize,time_in_force="GoodTillCancel").result()
                    time.sleep(2)
                    walletbalance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['available_balance']  # get wallet balance
            #       walletbalance = "90000"
                    time.sleep(2)
                    #print("here2")
                    endprice2 = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
                    currentwallbal = float(walletbalance) * float(endprice2)
                    #print("here3")
                    state = "closed"
                    date = datetime.now()
                    b = requests.post("https://hexeba.com/hbot/closedata.php?entry="+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&chatid='+str(self.chatid))
                    
                    c = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    

                    messagex = str(
                            "*********STOPLOSS FOR BTC LONG POSITION*******\nExchange: Bybit\nENTRY PRICE: $" + str(entry) + "\nEXIT PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nPrevious Balance: $" + str(
                                balance) + "\nNew Balance: $" + str(currentwallbal) + "\nDate: " + str(
                                date) + "\nDM @victor_hexeba for inquiry. ")
                    bot.send_message(self.chatid, messagex)
                #    #print("TESTING")

                    date = datetime.now()
                    last = j
                    state = "closed"
                    success = "yes"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



                #STOPLOSS LONG 2
                if((lastposition=='Buy')and(spy=="short")and(pnl <= -sl2)):
                    date = datetime.now()
                    last = j
                    success = "no"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



        #     if((position=="long")and(state == "open")):
                    client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                    #print("here1")
                    consize = int(client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["size"])
                    client.Order.Order_new(side='Sell', symbol="BTCUSD", order_type="Market", qty=consize,time_in_force="GoodTillCancel").result()
                    time.sleep(2)
                    walletbalance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['available_balance']  # get wallet balance
            #       walletbalance = "90000"
                    time.sleep(2)
                    #print("here2")
                    endprice2 = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
                    currentwallbal = float(walletbalance) * float(endprice2)
                    #print("here3")
                    state = "closed"
                    date = datetime.now()
                    b = requests.post("https://hexeba.com/hbot/closedata.php?entry="+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&chatid='+str(self.chatid))
                    
                    c = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    

                    messagex = str(
                            "*********STOPLOSS FOR BTC LONG POSITION*******\nExchange: Bybit\nENTRY PRICE: $" + str(entry) + "\nEXIT PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nPrevious Balance: $" + str(
                                balance) + "\nNew Balance: $" + str(currentwallbal) + "\nDate: " + str(
                                date) + "\nDM @victor_hexeba for inquiry. ")
                    bot.send_message(self.chatid, messagex)
            #     #print("TESTING")

                    date = datetime.now()
                    last = j
                    state = "closed"
                    success = "yes"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(chatid)+'&exchange='+exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)













                #SHORT TAKE PROFIT 1
                if((lastposition=='Sell')and(pnl <= -tp)):

                    date = datetime.now()
                    last = j
                    success = "no"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



        #      if((position=="short")and(state == "open")):
                    client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                    #print("here1")
                    consize = int(client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["size"])
                    client.Order.Order_new(side='Buy', symbol="BTCUSD", order_type="Market", qty=consize,time_in_force="GoodTillCancel").result()
                    time.sleep(2)
                    walletbalance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['available_balance']  # get wallet balance
            #       walletbalance = "90000"
                    time.sleep(2)
                    #print("here2")
                    endprice2 = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
                    currentwallbal = float(walletbalance) * float(endprice2)
                    #print("here3")
                    state = "closed"
                    date = datetime.now()
                    b = requests.post("https://hexeba.com/hbot/closedata.php?entry="+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&chatid='+str(self.chatid))
                    
                    c = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    #print("here44")

                    messagex = str(
                            "*********TOOK PROFIT FOR BTC SHORT POSITION*******\nExchange: Bybit\nENTRY PRICE: $" + str(entry)+"\nEXIT PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nPrevious Balance: $" + str(balance) + "\nNew Balance: $" + str(currentwallbal) + "\nDate: " + str(
                                date) + "\nDM @victor_hexeba for inquiry. ")
                    bot.send_message(str(self.chatid), messagex)
                #    #print("TESTING")

                    date = datetime.now()
                    last = j
                    state = "closed"
                    success = "yes"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)




                #SHORT TAKE PROFIT 2
                if((lastposition=='Sell')and(spy=="long")and(pnl <= -tp2)):

                    date = datetime.now()
                    last = j
                    success = "no"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



    #         if((position=="short")and(state == "open")):
                    client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                    #print("here1")
                    consize = int(client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["size"])
                    client.Order.Order_new(side='Buy', symbol="BTCUSD", order_type="Market", qty=consize,time_in_force="GoodTillCancel").result()
                    time.sleep(2)
                    walletbalance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['available_balance']  # get wallet balance
            #       walletbalance = "90000"
                    time.sleep(2)
                    #print("here2")
                    endprice2 = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
                    currentwallbal = float(walletbalance) * float(endprice2)
            #       #print("here3")
                    state = "closed"
                    date = datetime.now()
                    b = requests.post("https://hexeba.com/hbot/closedata.php?entry="+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&chatid='+str(self.chatid))
                    
                    c = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    

                    messagex = str(
                            "*********TOOK PROFIT FOR BTC SHORT POSITION*******\nExchange: Bybit\nENTRY PRICE: $" + str(entry) + "\nEXIT PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nPrevious Balance: $" + str(
                                balance) + "\nNew Balance: $" + str(currentwallbal) + "\nDate: " + str(
                                date) + "\nDM @victor_hexeba for inquiry. ")
                    bot.send_message(str(self.chatid), messagex)
                #    #print("TESTING")

                    date = datetime.now()
                    last = j
                    state = "closed"
                    success = "yes"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)


                #STOPLOSS SHORT 1
                if((lastposition=='Sell')and(pnl >= sl)):

                    date = datetime.now()
                    last = j
                    success = "no"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



        #        if((position=="short")and(state == "open")):
                    client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                    #print("here1")
                    consize = int(client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["size"])
                    client.Order.Order_new(side='Buy', symbol="BTCUSD", order_type="Market", qty=consize,time_in_force="GoodTillCancel").result()
                    time.sleep(2)
                    walletbalance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['available_balance']  # get wallet balance
            #       walletbalance = "90000"
                    time.sleep(2)
                    #print("here2")
                    endprice2 = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
                    currentwallbal = float(walletbalance) * float(endprice2)
                    #print("here3")
                    state = "closed"
                    date = datetime.now()
                    
                    b = requests.post("https://hexeba.com/hbot/closedata.php?entry="+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&chatid='+str(self.chatid))
                #    #print("fuck")
                    c = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    


                    messagex = str(
                            "*********STOPLOSS FOR BTC SHORT POSITION*******\nExchange: Bybit\nENTRY PRICE: $" + str(entry) + "\nEXIT PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nPrevious Balance: $" + str(
                                balance) + "\nNew Balance: $" + str(currentwallbal) + "\nDate: " + str(
                                date) + "\nDM @victor_hexeba for inquiry. ")
                    bot.send_message(str(self.chatid), messagex)
                #   #print("TESTING")

                    date = datetime.now()
                    last = j
                    state = "closed"
                    success = "yes"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



                #STOPLOSS SHORT 2
                if((lastposition=='Sell')and(spy=="long")and(pnl >= sl2)):


                    date = datetime.now()
                    last = j
                    success = "no"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)



        #        if((position=="short")and(state == "open")):
                    client = bybit.bybit(test=False, api_key=self.apikey1, api_secret=self.apikey2)
                    #print("here1")
                    consize = int(client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]["result"]["size"])
                    client.Order.Order_new(side='Buy', symbol="BTCUSD", order_type="Market", qty=consize,time_in_force="GoodTillCancel").result()
                    time.sleep(2)
                    walletbalance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['available_balance']  # get wallet balance
            #       walletbalance = "90000"
                    time.sleep(2)
                    #print("here2")
                    endprice2 = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
                    currentwallbal = float(walletbalance) * float(endprice2)
                    #print("here3")
                    state = "closed"
                    date = datetime.now()
                    b = requests.post("https://hexeba.com/hbot/closedata.php?entry="+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&chatid='+str(self.chatid))
                    
                    c = requests.post("https://hexeba.com/hbot/tradedata.php?bin15="+str(bin15)+'&deci15='+str(deci15)+'&entry='+str(entry)+'&state='+str(state)+'&position='+str(position)+'&total='+str(total)+'&balance='+str(currentwallbal)+'&date='+str(date)+'&startbal='+str(startbal)+'&chatid='+str(self.chatid))
                    

                    messagex = str(
                            "*********STOPLOSS FOR BTC SHORT POSITION*******\nExchange: Bybit\nENTRY PRICE: $" + str(entry) + "\nEXIT PRICE: $" + str(btcprice) + "\nLeverage: 15X" + "\nPrevious Balance: $" + str(
                                balance) + "\nNew Balance: $" + str(currentwallbal) + "\nDate: " + str(
                                date) + "\nDM @victor_hexeba for inquiry. ")
                    bot.send_message(str(self.chatid), messagex)
            #      #print("TESTING")

                    date = datetime.now()
                    last = j
                    state = "closed"
                    success = "yes"
                    b = requests.post("https://hexeba.com/hbot/closetrade.php?last="+str(last)+'&success='+success+'&date='+str(date)+'&state='+state+'&chatid='+str(self.chatid)+'&exchange='+self.exchange+'&entry='+str(entry)+'&position='+position)
                    #print(b.text)




