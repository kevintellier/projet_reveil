import requests
from gtts import gTTS
from playsound import playsound
import time
import os

NAME="Monsieur"
HOME_ADRESS="93 rue d'Aguesseau, 94490"
WORK_ADRESS = "ESIEE Paris"
LANG="fr"
TEMPS_PREPARATION = 3000
API_MAPS_KEY = "AIzaSyDE5NJFi9_se8qtlF1uyVSXxnTXPueKeQI"
API_WEATHER_KEY = "ff204a7f66eafb607b541f9a2ccb9032"
API_NEWS_KEY = "0f64ca5a2eb44c84bb311eb4ebdd4d62"
TRANSPORTATION_MODE = "driving"

def get_travel_time():
	url_base="https://maps.googleapis.com/maps/api/directions/json"
	origin = HOME_ADRESS
	destination = WORK_ADRESS
	language = LANG
	mode = TRANSPORTATION_MODE
	departure_time = time.time() + TEMPS_PREPARATION
	url = url_base + "?origin="+origin+"&destination="+destination+"&language="+language+"&mode="+mode+"&departure_time=now"+"&key="+API_MAPS_KEY
	json_data = requests.get(url).json()
	duration_in_traffic = json_data["routes"][0]["legs"][0]["duration_in_traffic"]["text"]
	duration_in_traffic_formated = int(duration_in_traffic[0]+duration_in_traffic[1])*60
	arrival_datetime = time.strftime('%Hh%M', time.localtime(departure_time + duration_in_traffic_formated))
	departure_datetime = time.strftime('%Hh%M', time.localtime(departure_time))
	sentence = "Le temps de trajet pour vous rendre sur votre lieu de travail est estimé à " + duration_in_traffic + ", vous arriverez à " + arrival_datetime + " en partant à " + departure_datetime 
	tts = gTTS(sentence,lang=LANG)
	tts.save('tts_travel.mp3')
	playsound('tts_travel.mp3')
	os.system("del tts_travel.mp3")
	print(sentence)

def get_bus_schedules():
	url_base="https://api-ratp.pierre-grimaud.fr/v3/schedules/bus/308/NOISEAU-AMBOILE/A"
	url=url_base
	json_data = requests.get(url).json()
	data_table= json_data["result"]["schedules"]
	time_tables = [0 for _ in range(len(data_table))]
	for i in range(len(data_table)):
		message = data_table[i]["message"]
		time_tables[i] = message
	if RepresentsInt(time_tables[1][0]):
		sentence = "Le prochain bus est dans " + time_tables[1]
		tts = gTTS(sentence,lang=LANG)
		tts.save('tts.mp3')
		playsound('tts.mp3')
		print(sentence)
	else:
		sentence = "Le prochain bus est " + time_tables[1] + " min"
		tts = gTTS(sentence,lang=LANG)
		tts.save('tts.mp3')
		playsound('tts.mp3')
		os.system("del tts_travel.mp3")
		print(sentence)

def get_current_weather():
	weather_api_key = "ff204a7f66eafb607b541f9a2ccb9032"
	zip_code = "75000"
	url_base="http://samples.openweathermap.org/data/2.5/"
	url=url_base+"weather?zip="+ zip_code +",fr&appid="+weather_api_key+"&lang=fr"
	url="http://api.openweathermap.org/data/2.5/weather?zip=75000,fr&lang=fr"+"&appid="+API_WEATHER_KEY
	json_data = requests.get(url).json()
	weather_descr = json_data["weather"][0]["description"]
	main = json_data["weather"][0]["main"]
	temp = json_data["main"]["temp"]-273.15
	weather_switch = {
		"Clear": "Le temps est dégagé",
		"Clouds": "le ciel est couvert",
		"Atmosphere": "Il y a du brouillard",
		"Snow": "Il y a de la neige",
		"Rain": "Le temps est pluvieux",
		"Drizzle": "Il y a de la bruine",
		"Thunderstrom": "Il y a de l'orage"
	}
	sentence = "Il fait " + str(round(temp)) + " degrés et "+weather_switch[main]
	tts = gTTS(sentence,lang=LANG)
	tts.save('tts_weather.mp3')
	playsound('tts_weather.mp3')
	os.system("del tts_travel.mp3")
	print(sentence)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_news():
	tts = gTTS("Voici les gros titres du jour : ",lang=LANG)
	tts.save('tts_news.mp3')
	playsound('tts_news.mp3')
	os.system("del tts_news.mp3")
	url_base="https://newsapi.org/v2/top-headlines?country=fr&apiKey="+API_NEWS_KEY
	url=url_base
	json_data = requests.get(url).json()
	news_data_title_list = [0 for _ in range(2)]
	news_data_desc_list = [0 for _ in range(2)]
	for i in range(2):
		news_data_title_list[i] = json_data["articles"][i]["title"]
		news_data_desc_list[i] = json_data["articles"][i]["description"]
		if (news_data_title_list[i] and news_data_desc_list[i]) != None:
			tts = gTTS(str(news_data_title_list[i]+news_data_desc_list[i]),lang=LANG)
			tts.save('tts_news'+str(i)+'.mp3')
			playsound('tts_news'+str(i)+'.mp3')
			os.system("del tts_news"+str(i)+".mp3")

def play_music():
	playsound('ringtone/1.mp3')

def message():
	sentence = "Bonjour Monsieur, il est " + time.strftime('%Hh%M') + ", nous somme le " + time.strftime("%d") + " aujourd'hui" 
	tts = gTTS(sentence,lang=LANG)
	tts.save('tts_message.mp3')
	playsound('tts_message.mp3')
	os.system("del tts_message.mp3")
	print(sentence)

play_music()
message()
get_news()
get_current_weather()
if TRANSPORTATION_MODE == "driving":
	get_travel_time()
elif TRANSPORTATION_MODE == "bus":
	get_bus_schedules()