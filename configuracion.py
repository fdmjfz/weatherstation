import json
import requests
import pandas as pd

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmcmFuZmlsZ3VlaXJhZkBnbWFpbC5jb20iLCJqdGkiOiJiZGNjMmUyNC0zNGQ3LTQxMTItOTM5ZS0zMGNkYmU4N2QxOWEiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY0NjMyODU5NiwidXNlcklkIjoiYmRjYzJlMjQtMzRkNy00MTEyLTkzOWUtMzBjZGJlODdkMTlhIiwicm9sZSI6IiJ9.yjWAb-R3rlG_BLILfmdxViIKuT-S5anAIViuYQYKNKo"
IDEMA = "1495"
MUNICIPIO_ID = "36057"

URL_DAILY = f'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{MUNICIPIO_ID}'
URL_LAST = f'https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{IDEMA}'

PERIODS = [
    '00-06', '06-12', '12-18',
    '18-24'
    ]


def get_daily_pred():
    params = {'api_key': API_KEY}

    response = requests.get(url = URL_DAILY, params = params)
    response = requests.get(url = response.json()['datos'])
    response = response.json()

    with open('data/daily_pred.json', 'w') as fileout:
        json.dump(response, fileout)
        
        
def get_last_data():
    params = {"api_key": API_KEY}
    
    response = requests.get(url = URL_LAST, params = params)
    response = requests.get(url = response.json()['datos'])
    response = response.json()[-1]    
    date = response['fint']
    date = pd.to_datetime(date)
    response['fint'] = date.strftime('%a,%d %H Hrs.')    
    
    with open('data/last_data.json', 'w') as fileout:
        json.dump(response, fileout)
    

def last_to_dict():
    with open('data/last_data.json', 'r') as filein:
        last_data = json.load(filein)
        
    return last_data
    

def daily_to_dict(period = '00-24', today = False):
    if today:
        dia_idx = 0
    else:
        dia_idx = 1
    
    with open('data/daily_pred.json', 'r') as filein:
        data = json.load(filein)
        
    output_dict = {}
    
    dia = pd.Timestamp('now').normalize()
    dia = dia + pd.Timedelta('8H')
    
    data_subset = data[0]['prediccion']['dia'][dia_idx]
    
    data_subset.keys()
    data_subset['humedadRelativa']
    
    
    for probPrecipitacion in data_subset['probPrecipitacion']:
        if probPrecipitacion['periodo'] == period:
            output_dict['probPrecipitacion'] = probPrecipitacion
            
    for estadoCielo in data_subset['estadoCielo']:
        if estadoCielo['periodo'] == period:
            output_dict['estadoCielo'] = estadoCielo
            
    for viento in data_subset['viento']:
        if viento['periodo'] == period:
            output_dict['viento'] = viento
    
    for rachaMax in data_subset['rachaMax']:
        if rachaMax['periodo'] == period:
            output_dict['rachaMax'] = rachaMax
            
            
    if today:
        for temperatura in data_subset['temperatura']['dato']:
            if temperatura['hora'] == int(period[3:5]):
                output_dict['temperatura'] = temperatura
                
                
        for sensTermica in data_subset['sensTermica']['dato']:
            if sensTermica['hora'] == int(period[3:5]):
                output_dict['sensTermica'] = sensTermica

        for humedadRelativa in data_subset['humedadRelativa']['dato']:
            if humedadRelativa['hora'] == int(period[3:5]):
                output_dict['humedadRelativa'] = humedadRelativa
        
        
        output_dict['uvMax'] = data_subset['uvMax']
    
    else:
        output_dict['temperatura'] = {
            'maxima': data_subset['temperatura']['maxima'],
            'minima': data_subset['temperatura']['minima']
            }
        
        output_dict['sensTermica'] = {
            'maxima': data_subset['sensTermica']['maxima'],
            'minima': data_subset['sensTermica']['minima']
            }
        
        output_dict['humedadRelativa'] = {
            'maxima': data_subset['humedadRelativa']['maxima'],
            'minima': data_subset['humedadRelativa']['minima']
            }
        
        output_dict['uvMax'] = data_subset['uvMax']
    
    
    
    fecha = pd.to_datetime(data_subset['fecha'])
    output_dict['fecha'] = fecha.strftime('%Y-%m-%d')
    output_dict
    
    return output_dict

def data_update():
    get_daily_pred()
    get_last_data()