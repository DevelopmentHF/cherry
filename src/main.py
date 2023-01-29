import curses, time, datetime
from curses import wrapper
from os import system



def main(stdscr):
    # Init. screen to be fresh for use
    stdscr.clear()

    # Init. color pair for future use
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Hides cursor on screen, user will be doing no typing that needs to be seen, only keypresses
    curses.curs_set(0)
    stdscr.refresh()

    # 25 minute timer 
    totalsec = 25 * 60

    # Allows for the while loop to start
    stdscr.nodelay(True)
    try:
        key = stdscr.getkey()
    except:
        key = 'a' 

    # timer control variables
    timerStarted = False
    sessionNum = 1 # after the 4th session, take an extended break
    breakNum = 0 
    isBreak = False


    # define text string constants to be used
    statusbar = "[q] - quit | [s] - start | [p] - pause"
    title = "cherry🍒"

    while key != 'q':
        # Get size of screen for centering purposes
        height, width = stdscr.getmaxyx()

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_session = int((width // 2) - (len("Session x") // 2) - len("Session x") % 2)
        start_x_break = int((width // 2) - (len("Break x") // 2) - len("Break x") % 2)
        start_x_timer = int((width // 2) - (len("0:00:00") // 2) - len("0:00:00") % 2)
        start_y = int((height // 2) - 2)

        # Render status bar
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(height-1, 0, statusbar)
        stdscr.addstr(height-1, len(statusbar), " " * (width - len(statusbar) - 1))
        stdscr.attroff(curses.color_pair(1))

        # Rendering title
        stdscr.addstr(1, start_x_title, title, curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(1))

        # Render details onto screen
        stdscr.attron(curses.A_UNDERLINE)
        if isBreak == False:
            stdscr.addstr(start_y,start_x_session, f"Session {sessionNum}")
        else:
            stdscr.addstr(start_y,start_x_break, f"Break {breakNum}")
        stdscr.attroff(curses.A_UNDERLINE)

        stdscr.addstr(start_y + 3, start_x_timer, str(datetime.timedelta(seconds = totalsec)))
        stdscr.refresh()

        # Check if user has started the countdown
        if key == 's':
            timerStarted = True
        elif key == 'p':
            timerStarted = False
        
        # Begin counting down 
        if timerStarted == True:
            time.sleep(1)
            totalsec -= 1

        # Check whether or not to increment session values
        if totalsec == -1:
            for i in range(4):
                system(f'afplay /System/Library/Sounds/Blow.aiff')
            if isBreak:
                sessionNum += 1
                totalsec = 5 * 60
            else:
                breakNum += 1
                if breakNum % 4 == 0:
                    totalsec = 30 * 60
                else:
                    totalsec = 25 * 60
            isBreak = not isBreak
    
        
        # Checks if a new keypress has occured, if not, set to default value 'a' to keep loop running
        try:
            key = stdscr.getkey()
        except:
            key = 'a'

        stdscr.clear()
        

wrapper(main)