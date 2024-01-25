# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 00:41:58 2024

@author: suraj
"""
import pandas as pd
from datetime import datetime, timedelta

def analyze_employee_data(file_path):
    # Loading data from Excel file
    df = pd.read_excel(file_path)

    # Converting 'Time' and 'Time Out' columns to datetime objects
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time Out'] = pd.to_datetime(df['Time Out'])

    #creating Dictionary to store employee data along with position
    employees = {}

    # Iterating over rows in the dataframe
    for index, row in df.iterrows():
        employee_name = row['Employee Name']
        position = row['Position ID']
        start_time = row['Time']
        end_time = row['Time Out']

        # Adding data to the dictionary
        if (employee_name, position) not in employees:
            employees[(employee_name, position)] = {'shifts': [(start_time, end_time)], 'worked_consec_days': False, 'less_than_10_hours': False, 'more_than_14_hours': False}
        else:
            employees[(employee_name, position)]['shifts'].append((start_time, end_time))

    # Analyzing employee data
    for (employee_name, position), data in employees.items():
        shifts = data['shifts']

        # Checking for consecutive days worked
        if not data['worked_consec_days']:
            for i in range(len(shifts) - 1):
                if (shifts[i+1][0] - shifts[i][1]).days == 1:
                    print(f"{employee_name} ({position}) has worked for 7 consecutive days.")
                    employees[(employee_name, position)]['worked_consec_days'] = True
                    break  # Break the inner loop once condition is met

        # Checking for less than 10 hours between shifts but greater than 1 hour
        if not data['less_than_10_hours']:
            for i in range(len(shifts) - 1):
                time_between_shifts = shifts[i+1][0] - shifts[i][1]
                if 1 < time_between_shifts.total_seconds() // 3600 < 10:
                    print(f"{employee_name} ({position}) has less than 10 hours between shifts but greater than 1 hour.")
                    employees[(employee_name, position)]['less_than_10_hours'] = True
                    break  # Break the inner loop once condition is met

        # Checking for more than 14 hours in a single shift
        if not data['more_than_14_hours']:
            for i in range(len(shifts) - 1):
                if (shifts[i+1][1] - shifts[i][0]).total_seconds() // 3600 > 14:
                    print(f"{employee_name} ({position}) has worked for more than 14 hours in a single shift.")
                    employees[(employee_name, position)]['more_than_14_hours'] = True
                    break  # Break the inner loop once condition is met

if __name__ == "__main__":
    file_path = "Assignment_Timecard.xlsx"
    analyze_employee_data(file_path)


# storing outputs in output.txt
with open("output.txt", "w") as output_file:
    
    import sys
    original_stdout = sys.stdout
    sys.stdout = output_file

    
    analyze_employee_data(file_path)

    
    sys.stdout = original_stdout
