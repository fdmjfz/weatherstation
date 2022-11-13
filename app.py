import curses
import os
from datetime import datetime
import configuracion as conf
from configuracion import data_update
from bme280pi import Sensor
from apscheduler.schedulers.background import BackgroundScheduler
import drawings

#Descargar datos si no hay
if not os.listdir('data'):
    data_update()

#Programado de la actualización/descarga de los datos de AEMET
scheduler = BackgroundScheduler()
scheduler.add_job(func=data_update, trigger='interval', minutes=60)
scheduler.start()


REFRESH_TIME = 1000 * 60 * 1#Milisegundos

#Inicialización de curses y creación de paletas de color
stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.init_pair(1,curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
COLOR_1 = curses.color_pair(1)
COLOR_2 = curses.color_pair(2)
COLOR_3 = curses.color_pair(3)
YELLOW = curses.color_pair(4)
curses.curs_set(0)

#Inicialización del sensor
sensor = Sensor()

def main(stdscr):
    main_window = curses.newwin(30, 100, 0, 0)
    main_window.bkgd(' ', COLOR_1)
    main_window.timeout(REFRESH_TIME)
    main_window.box()
    
    title = main_window.subwin(9, 63, 1, 20)
    title.addstr(0,2, drawings.TITLE, COLOR_3 | curses.A_BOLD)
    
    last = main_window.subwin(7, 25, 9, 1)
    last.box()

    bme280 = main_window.subwin(5,17,9,26)
    bme280.box()
    
    tomorrow = main_window.subwin(9, 35, 20, 64)
    tomorrow.box()
    
    today = main_window.subwin(9, 60, 20, 1)
    today.box()
    

    while True:
        main_window.addstr(8,40, 
                           datetime.now().strftime('%Y-%m-%d %H:%M'), 
                           COLOR_3 | curses.A_STANDOUT)
        
#Importación de datos
        today_data = {i:conf.daily_to_dict(period=i, today=True) for i in conf.PERIODS}
        tomorrow_data = conf.daily_to_dict(period='00-24', today=False)
        last_data = conf.last_to_dict()
#Lectura de datos del BME280
        temperature = round(sensor.get_temperature(), 1)
        humidity = round(sensor.get_humidity(), 1)
        pressure = round(sensor.get_pressure(), 1)
        
#Panel con los últimos registros de la estación cercana
        last.addstr(0,1, last_data['fint'])
        last.addstr(1,1, "Temp: ", COLOR_2 | curses.A_BOLD)
        last.addstr(1,12, str(last_data['ta']) + " ºC", COLOR_3 | curses.A_BOLD)
        last.addstr(2,1, "Hum: ", COLOR_2 | curses.A_BOLD)
        last.addstr(2,12, str(last_data['hr']) + " %", COLOR_3 | curses.A_BOLD)
        last.addstr(3,1, "Pres Nmar: ", COLOR_2 | curses.A_BOLD)
        last.addstr(3,12, str(last_data['pres_nmar']) + " hPa", COLOR_3 | curses.A_BOLD)
        last.addstr(4,1, "Precip: ", COLOR_2 | curses.A_BOLD)
        last.addstr(4, 12, str(last_data['prec']) + " L/m2", COLOR_3 | curses.A_BOLD)
        last.addstr(5,1, "Racha Max: ", COLOR_2 | curses.A_BOLD)
        last.addstr(5,12, str(last_data['vmax']) + " km/h", COLOR_3 | curses.A_BOLD)

#Panel BME280
        bme280.addstr(0,1, "BME 280")
        bme280.addstr(1,1, "Temp: ", COLOR_2 | curses.A_BOLD)
        bme280.addstr(1,6, str(temperature) + " ºC", COLOR_3 | curses.A_BOLD)
        bme280.addstr(2,1, "Hum: ", COLOR_2 | curses.A_BOLD)
        bme280.addstr(2,6, str(humidity) + " %", COLOR_3 | curses.A_BOLD)
        bme280.addstr(3,1, "Pres: ", COLOR_2 | curses.A_BOLD)
        bme280.addstr(3,6, str(pressure) + " hPa", COLOR_3 | curses.A_BOLD)

#Panel con la previsión de mañana        
        tomorrow.addstr(0,1,"Mañana,")
        tomorrow.addstr(0,8, tomorrow_data['fecha'])
        tomorrow.addstr(1,1, "T. Max/Min: ", COLOR_2 | curses.A_BOLD)
        tomorrow.addstr(1,19, 
                        str(tomorrow_data['temperatura']['maxima']) + 
                        " / " + 
                        str(tomorrow_data['temperatura']['minima']) +
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        tomorrow.addstr(2,1, "S. Term. Max/Min: ", COLOR_2 | curses.A_BOLD)
        tomorrow.addstr(2,19, 
                        str(tomorrow_data['sensTermica']['maxima']) + 
                        " / " + 
                        str(tomorrow_data['sensTermica']['minima']) +
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        tomorrow.addstr(3,1, "P. Precip.: ", COLOR_2 | curses.A_BOLD)
        tomorrow.addstr(3,19, 
                        str(tomorrow_data['probPrecipitacion']['value']) +
                        " %",
                        COLOR_3 | curses.A_BOLD)
        tomorrow.addstr(4,1, "Viento: ", COLOR_2 | curses.A_BOLD)
        tomorrow.addstr(4,19,
                        str(tomorrow_data['viento']['velocidad']) +
                        " km/h",
                        COLOR_3 | curses.A_BOLD)
        tomorrow.addstr(5,1, "Dir. Viento: ", COLOR_2 | curses.A_BOLD)
        tomorrow.addstr(5,19,
                        str(tomorrow_data['viento']['direccion']),
                        COLOR_3 | curses.A_BOLD)
        tomorrow.addstr(6,1, "UV Max: ", COLOR_2 | curses.A_BOLD)
        tomorrow.addstr(6,19,
                        str(tomorrow_data['uvMax']),
                        COLOR_3 | curses.A_BOLD)
        tomorrow.addstr(7,1,
                        tomorrow_data['estadoCielo']['descripcion'],
                        COLOR_3 | curses.A_BOLD)

#Panel con la previsión de hoy
        today.addstr(0,1, "Hoy, ")
        today.addstr(0, 5, today_data['00-06']['fecha'])
        today.addstr(2,1, "T. Max/Min: ", COLOR_2 | curses.A_BOLD)
        today.addstr(3,1, "S. Term. Max/Min: ", COLOR_2 | curses.A_BOLD)
        today.addstr(4,1, "P. Precip.: ", COLOR_2 | curses.A_BOLD)
        today.addstr(5,1, "Viento: ", COLOR_2 | curses.A_BOLD)
        today.addstr(6,1, "Dir. Viento: ", COLOR_2 | curses.A_BOLD)
        today.addstr(7,1, "UV Max: ", COLOR_2 | curses.A_BOLD)
        
        today.addstr(1,19, "00-06", curses.A_UNDERLINE)
        today.addstr(2,19, 
                        str(today_data['00-06']['temperatura']['value']) + 
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(3,19, 
                        str(today_data['00-06']['sensTermica']['value']) + 
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(4,19, 
                        str(today_data['00-06']['probPrecipitacion']['value']) +
                        " %",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(5,19,
                        str(today_data['00-06']['viento']['velocidad']) +
                        " km/h",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(6,19,
                        str(today_data['00-06']['viento']['direccion']),
                        COLOR_3 | curses.A_BOLD)
        today.addstr(7,19,
                        str(today_data['00-06']['uvMax']),
                        COLOR_3 | curses.A_BOLD)
        
        today.addstr(1,29, "06-12", curses.A_UNDERLINE)
        today.addstr(2,29, 
                        str(today_data['06-12']['temperatura']['value']) + 
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(3,29, 
                        str(today_data['06-12']['sensTermica']['value']) +
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(4,29, 
                        str(today_data['06-12']['probPrecipitacion']['value']) +
                        " %",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(5,29,
                        str(today_data['06-12']['viento']['velocidad']) +
                        " km/h",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(6,29,
                        str(today_data['06-12']['viento']['direccion']),
                        COLOR_3 | curses.A_BOLD)
        today.addstr(7,29,
                        str(today_data['06-12']['uvMax']),
                        COLOR_3 | curses.A_BOLD)
        
        today.addstr(1,40, "12-18", curses.A_UNDERLINE)
        today.addstr(2,40, 
                        str(today_data['12-18']['temperatura']['value']) + 
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(3,40, 
                        str(today_data['12-18']['sensTermica']['value']) +
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(4,40, 
                        str(today_data['12-18']['probPrecipitacion']['value']) +
                        " %",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(5,40,
                        str(today_data['12-18']['viento']['velocidad']) +
                        " km/h",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(6,40,
                        str(today_data['12-18']['viento']['direccion']),
                        COLOR_3 | curses.A_BOLD)
        today.addstr(7,40,
                        str(today_data['12-18']['uvMax']),
                        COLOR_3 | curses.A_BOLD)
        
        today.addstr(1,51, "18-24", curses.A_UNDERLINE)
        today.addstr(2,51, 
                        str(today_data['18-24']['temperatura']['value']) + 
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(3,51, 
                        str(today_data['18-24']['sensTermica']['value']) +
                        " ºC",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(4,51, 
                        str(today_data['18-24']['probPrecipitacion']['value']) +
                        " %",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(5,51,
                        str(today_data['18-24']['viento']['velocidad']) +
                        " km/h",
                        COLOR_3 | curses.A_BOLD)
        today.addstr(6,51,
                        str(today_data['18-24']['viento']['direccion']),
                        COLOR_3 | curses.A_BOLD)
        today.addstr(7,51,
                        str(today_data['18-24']['uvMax']),
                        COLOR_3 | curses.A_BOLD)
  
        
#Actualización de paneles
        main_window.refresh()
        last.refresh()
        today.refresh()
        tomorrow.refresh()
        main_window.getch() 



if __name__ == '__main__':
    curses.wrapper(main)
