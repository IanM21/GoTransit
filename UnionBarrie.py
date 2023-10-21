import requests as r
from texttable import Texttable
import inquirer
from inquirer.themes import GreenPassion
import csv
import json
import os
import datetime

def un_ba():
    # Get the current date
    depart_date_today = datetime.datetime.now() 
    depart_date_today = depart_date_today.strftime("%Y-%m-%d") # Format the date to YYYY-MM-DD

    # Get tomorrow's date
    depart_date_tmr = datetime.datetime.now() + datetime.timedelta(days=1)
    depart_date_tmr = depart_date_tmr.strftime("%Y-%m-%d") # Format the date to YYYY-MM-DD

    # Get the day after tomorrow's date
    depart_date_tmr2 = datetime.datetime.now() + datetime.timedelta(days=2)
    depart_date_tmr2 = depart_date_tmr2.strftime("%Y-%m-%d") # Format the date to YYYY-MM-DD

    print("Enter Depart Date\n")
    print("\t1. Today ({})".format(depart_date_today))
    print("\t2. Tomorrow ({})".format(depart_date_tmr))
    print("\t3. Day After Tomorrow ({})".format(depart_date_tmr2))
    
    depart_date = input("\n")
    depart_date = int(depart_date)

    if depart_date == 1:
        depart_date = depart_date_today
    elif depart_date == 2:
        depart_date = depart_date_tmr
    elif depart_date == 3:
        depart_date = depart_date_tmr2

    url = 'https://api.gotransit.com/v2/schedules/en/timetable?fromStop=UN&toStop=BA&serviceCode=65&direction=N&date={}'.format(depart_date)
    response = r.get(url)
    data = response.json()

    trips = data['trips']
    timetable = []

    for trip in trips:
        trip_type = trip['transitType']
        if trip_type == 1:
            # Correctly use datetime.datetime to parse and format the time
            depart_time = datetime.datetime.strptime(trip['departureTimeDisplay'], "%H:%M").strftime("%I:%M %p")
            arrive_time = datetime.datetime.strptime(trip['arrivalTimeDisplay'], "%H:%M").strftime("%I:%M %p")
            transfer = trip['transfers']
            duration = trip['duration']
            trip_number = trip['lines'][0]['tripNumber']
            timetable.append([depart_time, arrive_time, transfer, duration, trip_number])


    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    table = Texttable()
    headers = ['Departure Time', 'Arrival Time', 'Transfer(s)', 'Duration', 'Trip #']
    table.header(headers)

    for row in timetable:
        table.add_row(row)

    table.set_deco(Texttable.HEADER)
    print(table.draw())
    print("===============================================================")
    print('\nUnion to Barrie\t' + depart_date + '\n')

if __name__ == "__main__":
    un_ba()
