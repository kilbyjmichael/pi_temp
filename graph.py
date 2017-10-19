import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib import style
style.use(['seaborn-poster'])

conn = sqlite3.connect(r"temp.db")
c = conn.cursor()

def graph_all_data():
    c.execute('SELECT time, temp FROM office')
    data = c.fetchall()

    dates = []
    temps = []
    
    for row in data: # 2017-10-19 05:42:40.277908
        parsed = datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S.%f")
        dates.append(parsed)
        temps.append(row[1])

    plt.plot_date(dates,temps,'',label='temp')
    ax = plt.gca()
    ax.grid(True)
    plt.show()

def graph_data(choose_date):
    c.execute('SELECT time, temp FROM office')
    data = c.fetchall()

    dates = []
    temps = []

    dayg = datetime.strptime(choose_date, "%Y-%m-%d")
    
    for row in data: # 2017-10-19 05:42:40.277908
        parsed = datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S.%f")
        if parsed.date() == dayg.date():
            dates.append(parsed)
            temps.append(row[1])

    plt.plot_date(dates,temps,'',label='temp')
    ax = plt.gca()
    ax.grid(True)
    plt.show()

#graph_data("2017-10-16")
graph_all_data()
c.close()
