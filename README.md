# MeteoApp

Project for BME280 temperature/humidity/pressure sensor implementation in a Raspberry Pi with a curses-python console app.  
  
First, it is needed to write in the _configuracion.py_ file the _api key_ (API_KEY), the weather station identifier (IDEMA) and the city code (MUNICIPIO_ID), which can be found here https://opendata.aemet.es/centrodedescargas/inicio.  
Then the app is ready to get real time data from the AEMET's Open Data api and weather forecasting as external source, and the indoor conditions with the BME280 sensor in a lightweight environment and a console-based front-end.  
  
```
git clone https://github.com/fdmjfz/weatherstation.git  
cd weatherstation
pip install -r requirements
pyton app.py
```
