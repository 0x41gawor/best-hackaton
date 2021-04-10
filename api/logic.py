import threading
from database import db
from datetime import datetime

from weather_client import get_weather

current_in_temp = 20

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
    # We need to save some test api calls
    # temp, clouds = get_weather('Warsaw', 0)
    temp, clouds = 15.37, 15
    clouds = 100 - clouds
    return hour, day_type, month, temp, clouds

    
    
def run():
    # INPUT DATA
    print('INPUT DATA')
    hour, day_type, month, current_out_temp, clouds = get_input_values()
    solar_power = db.get_fotov_efficiency(month, hour, clouds)
    energy_prices = db.get_electricity_prices(month, day_type, hour)
    avg_dev_pow_drain = db.get_other_dev_pow_drain(day_type, hour)
    expected_temp = db.get_expected_temp(day_type, hour)
    maintain_in_temp_pow, increase_temp_pow, temp_drop_time,  = db.get_avg_heat_power(current_out_temp)
    print(f"current temp: {current_in_temp}, expected_temp: {expected_temp}")
    # ALGORITHM
     print('ALGORITHM')


    