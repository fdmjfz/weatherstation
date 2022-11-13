import curses
from datetime import datetime
import configuracion as conf
import drawings
from apscheduler.schedulers.background import BackgroundScheduler

timer = 0

def updating():
    global timer
    timer += 1
    with open(f'{timer}.txt', 'w') as f:
        f.write('prueba')
        
scheduler = BackgroundScheduler()
scheduler.add_job(func=updating, trigger='interval', seconds=10)
scheduler.start()

#conf.get_daily_pred()
#conf.get_last_data()

REFRESH_TIME = 1000 * 1 #Milisegundos

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

def main(stdscr):
    countertomorrow = 0
    counterlast = 0
    countertoday = 0
    main_window = curses.newwin(30, 100, 0, 0)
    main_window.bkgd(' ', COLOR_1)
    main_window.timeout(REFRESH_TIME)
    main_window.box()
    
    title = main_window.subwin(9, 63, 1, 20)
    title.addstr(0,2, drawings.TITLE, COLOR_3 | curses.A_BOLD)
    
    last = main_window.subwin(7, 25, 9, 1)
    last.box()
    
    tomorrow = main_window.subwin(9, 35, 20, 64)
    tomorrow.box()
    
    today = main_window.subwin(9, 60, 20, 1)
    today.box()
    

    while True:
        countertomorrow += 1
        counterlast += 1
        countertoday += 1
        main_window.addstr(8,40, 
                           datetime.now().strftime('%Y-%m-%d %H:%M'), 
                           COLOR_3 | curses.A_STANDOUT)
    
        tomorrow.addstr(1,1, str(countertomorrow))
        last.addstr(1,1, str(counterlast))
        today.addstr(1,1,str(countertoday))
        
        
        main_window.refresh()
        last.refresh()
        today.refresh()
        tomorrow.refresh()
        main_window.getch() 



if __name__ == '__main__':
    curses.wrapper(main)
