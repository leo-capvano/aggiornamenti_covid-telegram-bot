#this bot is used to recieve data/updates about COVID in Italy. 
#It can retrieve data about contagions, sick people, deceased and many more ... 
#It has been used the Telepot API
import sys
import telepot
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from datetime import datetime

#function that format the data in a specific way: Year-Month-Day-Hour-Minute-Second
def convert_data(data):
    return datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")


#this function sends to the chat the data of all the italian regions
def tutte_le_regioni_command(chat_id):
	#request data from the online repo of the Civil Protection
    r = requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json")
    if r.status_code == requests.codes.ok:
            r = r.json()
            msg_resp = ""
            #format the retrieved data and send back to the chat
            for i in range(21):
                msg_resp += "*"+r[-i]["denominazione_regione"]+"*:\n\n"\
                    +"Nuovi positivi ---> "+str(r[-i]["nuovi_positivi"])+"\n"\
                    +"Totale positivi ---> "+str(r[-i]["totale_positivi"])+"\n"\
                    +"Deceduti ---> "+str(r[-i]["deceduti"])+"\n"\
                    +"Dimessi Guariti ---> "+str(r[-i]["dimessi_guariti"])+"\n"\
                    +"Tamponi ---> "+str(r[-i]["tamponi"])+"\n"\
                    +"Ricoverati con sintomi ---> "+str(r[-i]["ricoverati_con_sintomi"])+"\n"\
                    +"In isolamento ---> "+str(r[-i]["isolamento_domiciliare"])+"\n\n\n"
            bot.sendMessage(chat_id, msg_resp, parse_mode="Markdown")
            bot.sendMessage(chat_id, "DATI AGGIORNATI IN DATA:\n"+str(convert_data(r[len(r)-1]["data"])))
            bot.sendMessage(chat_id, "Questi dati sono recuperati dal *Sito del Dipartimento della Protezione Civile*", parse_mode="Markdown")


#this function let the user choose an italian region to recover COVID updates.
#it creates one bottom for each italian region, and the user has to press them to make the chioce.
def scegli_regione_command(chat_id):
	#create buttons and send to the user chat
	#Each button will send the result to the on_callback_query function defined below
    choose_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Abruzzo",callback_data='abruzzo')],[InlineKeyboardButton(text="Veneto",callback_data='veneto')],
        [InlineKeyboardButton(text="Valle D'Aosta",callback_data='valle d\'aosta')],
        [InlineKeyboardButton(text="Umbria",callback_data='Umbria')],
        [InlineKeyboardButton(text="Toscana",callback_data='toscana')],
        [InlineKeyboardButton(text="Sicilia",callback_data='sicilia')],
        [InlineKeyboardButton(text="Sardegna",callback_data='sardegna')],
        [InlineKeyboardButton(text="Puglia",callback_data='puglia')],
        [InlineKeyboardButton(text="Piemonte",callback_data='piemonte')],
        [InlineKeyboardButton(text="Trentino",callback_data='Trentino')],
        [InlineKeyboardButton(text="Alto Adige",callback_data='Alto Adige')],
        [InlineKeyboardButton(text="Molise",callback_data='Molise')],
        [InlineKeyboardButton(text="Lombardia",callback_data='Lombardia')],
        [InlineKeyboardButton(text="Marche",callback_data='Marche')],
        [InlineKeyboardButton(text="Liguria",callback_data='Liguria')],
        [InlineKeyboardButton(text="Lazio",callback_data='Lazio')],
        [InlineKeyboardButton(text="Friuli Venezia Giulia",callback_data='Friuli Venezia Giulia')],
        [InlineKeyboardButton(text="Emilia-Romagna",callback_data='Emilia-Romagna')],
        [InlineKeyboardButton(text="Campania",callback_data='Campania')],
        [InlineKeyboardButton(text="Calabria",callback_data='Calabria')],
        [InlineKeyboardButton(text="Basilicata",callback_data='Basilicata')]
        ])
    bot.sendMessage(chat_id, "Scegli la regione",reply_markup=choose_keyboard)

#This function recieves the "choice" of the user when he presses the button to choose a specific region. 
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    #Recover all the data from the online repo
    r = requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json")
    if r.status_code == requests.codes.ok:
            r = r.json()
            for i in range(21):
            	#loop through the retrieved data region by region and perform "action X" when the actual region = region choosed with the button
            	#action X: send back to the user's chat the data of the selected region 
                if r[-i]["denominazione_regione"].lower() == query_data.lower():
                    msg_resp = "*"+r[-i]["denominazione_regione"]+"*:\n\n"\
                    +"Nuovi positivi ---> "+str(r[-i]["nuovi_positivi"])+"\n"\
                    +"Totale positivi ---> "+str(r[-i]["totale_positivi"])+"\n"\
                    +"Deceduti ---> "+str(r[-i]["deceduti"])+"\n"\
                    +"Dimessi Guariti ---> "+str(r[-i]["dimessi_guariti"])+"\n"\
                    +"Tamponi ---> "+str(r[-i]["tamponi"])+"\n"\
                    +"Ricoverati con sintomi ---> "+str(r[-i]["ricoverati_con_sintomi"])+"\n"\
                    +"In isolamento ---> "+str(r[-i]["isolamento_domiciliare"])+"\n\n\n"
                    bot.sendMessage(from_id, msg_resp)
                    bot.sendMessage(from_id, "DATI AGGIORNATI IN DATA:\n"+str(convert_data(r[-i]["data"])))
                    bot.sendMessage(from_id, "Questi dati sono recuperati dal *Sito del Dipartimento della Protezione Civile*", parse_mode="Markdown")


#function that handles the chat messages recieved by the bot. 
#It's called on every recieved message
def msg_handler(msg):
	#recover some infos about the recieved message
    content_type, chat_type, chat_id = telepot.glance(msg)

    #perform action based on the recieved message (command).
    #Messages different by the official commands (shown in the commands list) will be ignored (this can be easly changed)
    command = msg["text"]
    if command == "/tutte_le_regioni":
    	tutte_le_regioni_command(chat_id)
    if command == "/scegli_regione":
        scegli_regione_command(chat_id)
    if command == "/start":
        bot.sendMessage(chat_id, "Ciao!\nQuesto bot ti permette di controllare gli aggiornamenti \
        	giornalieri del COVID-19.\nI dati sono recuperati dal sito della Protezione Civile.\n\n\
        	I comandi sono:\n/tutte_le_regioni - controlla dati COVID di tette le regioni italiane\n/scegli_regione - controlla dati COVID scegliendo una regione")
    

#registering the bot
bot = telepot.Bot("1258623971:AAGwqZDtRGRTKWjSs7CMmgebOMteV_ZIXvI")
#defining a message loop that will process all the messages.
#In particular we are specifying that the "chat" messages (from keyboard) will be processed by the mgs_handler function
#and the "callback_query" messages (from predefined buttons) will be processed by on_callback_query function 
MessageLoop(bot, {"chat":msg_handler,
                    "callback_query":on_callback_query}).run_as_thread()
print("Listening...")

#keeping the bot alive
while 1:
	time.sleep(10)

