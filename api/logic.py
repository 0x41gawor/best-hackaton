import threading
from database import db
from datetime import datetime


# code from http://stackoverflow.com/a/14035296/4592067
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def db_setup():
    db.setup()
    db.insert_csv()
    db.create_home()

# Return current: hour, day_type, month, temperature and %clouds
def get_input_values():
    def get_day_type(home_id):
        day_nr = datetime.today().weekday()

        if db.get_is_holiday(home_id) == True:
            return 'wakacje'
        if day_nr > 4:
            return 'wolne'
        else:
            return 'robocze'
    hour = str(datetime.now().hour) + ":00"
    day_type = get_day_type(0)
    month = datetime.now().month
    return hour, day_type, month
    
def run():
    # INPUT DATA
    print('INPUT DATA')
    # Get input values(hour, day_type, month)
    print(get_input_values())



    