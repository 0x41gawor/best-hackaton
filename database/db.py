import sqlite3
import csv
import datetime


def setup():

    create_table('home',
                 'id integer primary key, '
                 'max_heating_pow integer, '
                 'water_warmer_pow integerm '
                 'hot_water_capacity integer, '
                 'rooms_heat_pow text, '
                 'battery_capacity integer, '
                 'battery_max_pow_drain integer, '
                 'max_charging_pow integer, '
                 'max_return_pow integer')

    create_table('admin',
                 'id integer primary key, '
                 'login text, '
                 'password text, '
                 'is_super integer, '
                 'foreign key(id) references home(home_id)')

    create_table('avg_heat_power',
                 'id integer primary key, '
                 'min_temp integer, '
                 'max_temp integer, '
                 'conts_temp_power real, '
                 'inc_temp_power real, '
                 'temp_drop_time real, '
                 'foreign key(id) references home(home_id)')

    create_table('expected_temp',
                 'id integer primary key, '
                 'day_type text, '
                 'start_hour text, '
                 'end_hour text, '
                 'temperature integer, '
                 'foreign key(id) references home(home_id)')

    create_table('fotov_efficiency',
                 'id integer primary key, '
                 'months text, '
                 'hours text, '
                 'clear_sky text, '
                 'power text, '
                 'foreign key(id) references home(home_id)')

    create_table('other_dev_pow_drain',
                 'id integer primary key, '
                 'day_type text, '
                 'hours text, '
                 'power text, '
                 'foreign key(id) references home(home_id)')

    create_table('electricity_prices',
                 'id integer primary key, '
                 'months text, '
                 'day_type text, '
                 'hours text, '
                 'drain_price real, '
                 'return_price real, '
                 'foreign key(id) references home(home_id)')


def create_table(name, fields):
    connection = sqlite3.connect('database.db')
    c = connection.cursor()

    c.execute(f"""CREATE TABLE IF NOT EXISTS {name} (
                    {fields}
                    )""")

    connection.commit()
    connection.close()


def insert(table, arguments):
    connection = sqlite3.connect('database.db')
    c = connection.cursor()

    s = ''

    for argument in arguments:
        if type(argument) is str:
            s += "'" + argument + "', "
        else:
            s += str(argument) + ', '
    s = s[:-2]

    c.execute(f"INSERT into {table} VALUES ({s})")

    connection.commit()
    connection.close()


def insert_csv():
    files = ['../csv_payload/expected_temp.csv',
             '../csv_payload/electricity_prices.csv',
             '../csv_payload/fotov_efficiency.csv',
             '../csv_payload/other_dev_pow_drain.csv',
             '../csv_payload/avg_heat_power.csv'
             ]
    tables = ['expected_temp', 'electricity_prices', 'fotov_efficiency', 'other_dev_pow_drain', 'avg_heat_power']
    for i, file in enumerate(files):
        with open(file, newline='') as f:
            reader = csv.reader(f, delimiter=";")
            data = list(reader)[1::]
        for j, entry in enumerate(data):
            entry.insert(0, j)
            insert(tables[i], entry)


def create_home():
    connection = sqlite3.connect('database.db')
    c = connection.cursor()

    s = '10, 6, 150, "1kW, 1kW, 1,5kW, 1,5kW, 2kW, 2kW, 3kW", 7, 2, 1, 5'

    c.execute(f"INSERT into home VALUES ({s})")

    connection.commit()
    connection.close()


def get_expected_temp(day, time):

    connection = sqlite3.connect('database.db')
    c = connection.cursor()

    c.execute(f'SELECT * FROM expected_temp WHERE day_type="{day}"')
    results = c.fetchall()
    connection.commit()
    connection.close()

    for result in results:
        if int(result[2][0:2]) <= int(time[0:2]) <= int(result[3][0:2]):
            return result[4]


def get_other_dev_pow_drain(day, time):
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute(f'SELECT * FROM other_dev_pow_drain WHERE day_type="{day}"')
    results = c.fetchall()
    connection.commit()
    connection.close()
    for result in results:
        if int(result[2][0:2]) <= int(time[0:2]) <= int(result[2][6:8]):
            return result[3]


def get_avg_heat_power(temp):
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute(f'SELECT * FROM avg_heat_power where min_temp<="{temp}" and max_temp>="{temp}"')
    results = c.fetchone()
    connection.commit()
    connection.close()

    return results


def get_electricity_prices(month, day, time):

    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute(f'SELECT * FROM electricity_prices WHERE day_type="{day}"')
    results = c.fetchall()
    connection.commit()
    connection.close()
    for result in results:
        if int(result[3][0:2]) <= int(time[0:2]) <= int(result[3][6:8]):

            ranges = (result[1].split())
            for range in ranges:
                if int(range[0:2]) <= month <= int(range[3:5]):
                    return result[4], result[5]


def get_fotov_efficiency(month, hour, clouds):

    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute(f'SELECT * FROM fotov_efficiency')
    results = c.fetchall()
    connection.commit()
    connection.close()

    res = []
    for result in results:
        months = result[1].replace(',', '').split()
        months = list(map(int, months))
        # warunek miesiąca
        if month in months:
            # godziny przechodzące przez północ
            if int(result[2][0:2]) > int(result[2][6:8]):
                if int(result[2][0:2]) <= int(hour[0:2]) or int(result[2][6:8]) >= int(hour[0:2]):
                    res.append(result)
            # godziny "zwykłe"
            else:
                if int(result[2][0:2]) <= int(hour[0:2]) <= int(result[2][6:8]):
                    res.append(result)
    for result in res:
        if result[3] == '90-100' and clouds >= 90:
            return result[4]
        elif result[3] == '60-90' and 60 <= clouds < 90:
            return result[4]
        elif result[3] == '<60' and clouds < 60:
            return result[4]


if __name__ == '__main__':
    pass
    # setup()
    # insert_csv()
    # create_home()
    # print(get_expected_temp('robocze', '06:00'))
    # print(get_other_dev_pow_drain('robocze', '16:30'))
    # print(get_avg_heat_power(12))
    # print(get_electricity_prices(12, 'robocze', '12:00'))
    # print(get_fotov_efficiency(12, '15:00', 90))
