import requests as r
import inquirer
from inquirer.themes import GreenPassion
import csv
import json
import os
import datetime
from texttable import Texttable

def custom_mode():
    def get_stations():
        stations = []

        with open('./GTFS/stops.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile, fieldnames=['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url', 'location_type', 'parent_station', 'wheelchair_boarding', 'stop_code'])
        
            # Iterate over each row in the CSV file
            for row in csvreader:
                # Check if the stop_id is not an integer
                if not row['stop_id'].isdigit():
                    # Extract the desired information and format it
                    stop_info = f"{row['stop_name']}: {row['stop_id']}"
                    # Append the formatted information to the result_list
                    stations.append(stop_info)

        return stations

    def get_schedule():
        stations = get_stations()

        depart_station = inquirer.prompt([
            inquirer.List('depart_station',
                        message="Select Departure Station",
                        choices=stations,
                    ),
        ], theme=GreenPassion())['depart_station']
        depart_code = depart_station.split(": ")[1] # Split the string to get the stop_id
        

        arrive_station = inquirer.prompt([
            inquirer.List('arrive_station',
                        message="Select Arrival Station",
                        choices=stations,
                    ),
        ], theme=GreenPassion())['arrive_station']
        arrive_code = arrive_station.split(": ")[1] # Split the string to get the stop_id

        
        depart_date = datetime.datetime.now() # Get the current date
        depart_date = depart_date.strftime("%Y-%m-%d") # Format the date to YYYY-MM-DD

        travel_direction = input("Enter 1 for Northbound, 0 for Southbound: ") # Ask for travel direction
        if travel_direction == "1":
            travel_direction = "N"
        elif travel_direction == "0":
            travel_direction = "S"

        service_code = input("Enter Service Code: ") # Ask for service code
        print('Scheduled Trains: \n')

        find_trips(depart_code, arrive_code, depart_date, travel_direction, service_code)

    def find_trips(depart_code, arrive_code, depart_date, travel_direction, service_code):
        url = 'https://api.gotransit.com/v2/schedules/en/timetable?fromStop={}&toStop={}&serviceCode={}&direction={}&date={}'.format(depart_code, arrive_code, service_code, travel_direction, depart_date)
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


        # clear console before printing the table
        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        # Create a table object
        table = Texttable()
        # Set the table header + add information to the table
        headers = ['Departure Time', 'Arrival Time', 'Transfer(s)', 'Duration', 'Trip #']
        table.header(headers)

        for row in timetable:
            table.add_row(row)
        
        trip_string = depart_code + ' to ' + arrive_code

        # Print the table
        table.set_deco(Texttable.HEADER)
        print(table.draw())
        print("===============================================================")
        print('\n', trip_string, '\n')
    get_schedule()