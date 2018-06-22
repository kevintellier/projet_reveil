import requests
from gtts import gTTS
from playsound import playsound
import time

"""main_api = "https://dataratp2.opendatasoft.com/api/records/1.0/search/?dataset="
dataset_temps_reel = "horaires-temps-reel"
dataset_positions = "positions-geographiques-des-stations-du-reseau-ratp"
stop_name = "NOISEAU-AMBOILE"

url = main_api + dataset_positions + "&refine.stop_name=" + stop_name
print("Requesting "+ url)
json_data = requests.get(url).json()
stop_id=json_data['records'][0]['fields']['stop_id']
print(stop_id)

url = main_api + dataset_temps_reel
reponse = requests.request("POST",)"""
HOME_ADRESS_lat = 48.787820
HOME_ADRESS_long = 2.532749
WORK_ADRESS_lat = 48.787820
WORK_ADRESS_long = 2.532749
TEMPS_PREPARATION = 3600*1.5
API_MAPS_KEY = "AIzaSyDE5NJFi9_se8qtlF1uyVSXxnTXPueKeQI"
API_WEATHER_KEY = "ff204a7f66eafb607b541f9a2ccb9032"

def get_travel_time():
	url_base="https://maps.googleapis.com/maps/api/directions/json"
	origin = str(HOME_ADRESS_long)+","+str(HOME_ADRESS_lat)
	destination = str(WORK_ADRESS_long)+","+str(WORK_ADRESS_lat)
	origin = "93 rue d'Aguesseau, 94490"
	destination = "ESIEE Paris"
	language = "fr-FR"
	mode="driving"
	departure_time = time.time() + TEMPS_PREPARATION
	url = url_base + "?origin="+origin+"&destination="+destination+"&language="+language+"&mode="+mode+"&departure_time=now"+"&key="+API_MAPS_KEY
	json_data = requests.get(url).json()
	duration_in_traffic = json_data["routes"][0]["legs"][0]["duration_in_traffic"]["text"]
	duration_in_traffic_formated = int(duration_in_traffic[0]+duration_in_traffic[1])*60
	arrival_datetime = time.strftime('%Hh%M', time.localtime(departure_time + duration_in_traffic_formated))
	departure_datetime = time.strftime('%Hh%M', time.localtime(departure_time))
	sentence = "Le temps de trajet pour vous rendre sur votre lieu de travail est estimé à " + duration_in_traffic + ", vous arriverez à " + arrival_datetime + " en partant à " + departure_datetime 
	tts = gTTS(sentence,lang="fr")
	tts.save('tts_travel.mp3')
	playsound('tts_travel.mp3')
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
		tts = gTTS(sentence,lang="fr")
		tts.save('tts.mp3')
		playsound('tts.mp3')
		print(sentence)
	else:
		sentence = "Le prochain bus est " + time_tables[1] + " min"
		tts = gTTS(sentence,lang="fr")
		tts.save('tts.mp3')
		playsound('tts.mp3')
		print(sentence)

def get_current_weather():
	weather_api_key = "ff204a7f66eafb607b541f9a2ccb9032"
	zip_code = "75000"
	url_base="http://samples.openweathermap.org/data/2.5/"
	url=url_base+"weather?zip="+ zip_code +",fr&appid="+weather_api_key+"&lang=fr"
	url="http://api.openweathermap.org/data/2.5/weather?zip=75000,fr&lang=fr"+"&appid"+API_WEATHER_KEY
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
	tts = gTTS(sentence,lang="fr")
	tts.save('tts_weather.mp3')
	playsound('tts_weather.mp3')
	print(sentence)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

get_travel_time()
#get_current_weather()
#get_bus_schedules()



