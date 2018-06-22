import requests

main_api = "https://dataratp2.opendatasoft.com/api/records/1.0/search/?dataset="
dataset_positions = "positions-geographiques-des-stations-du-reseau-ratp"
stop_name = "NOISEAU-AMBOILE"

url = main_api + dataset_positions + "&refine.stop_name=" + stop_name
print("Requesting: "+ url)
json_data = requests.get(url).json()
stop_id=json_data['records'][0]['fields']['stop_id']
print(stop_id)