"""

This piece of code deletes all entries from the database every 48 hours.

"""
import time
from app.models import User
from app import db
import sys

def from_second_to_hour(num_hours):
    seconds_per_minute = 60
    minutes_per_hour = 60
    return seconds_per_minute*minutes_per_hour*num_hours

if __name__ == '__main__':

    #Here we are setting up the duration that we should wait before wiping the database, this is set to 48 hours by default
    duration = str(raw_input("Enter the duration user information should persist (in hours, default is 48):"))
    if duration == '':
        duration = 48
    if not duration.isdigit():
        duration = 48
    else:
        duration = int(duration)

    #yes_no is a check to make sure you actually want to do this and didn't just hit the database by accident
    yes_no = ''
    while yes_no != "y" or yes_no != "n":
        yes_no = str(raw_input("Are you sure you want to delete all users every "+str(duration)+" hours?(y/n)"))
        if yes_no != "y" or yes_no != "n":
            print("please enter y or n, for yes or no, respectively")

    #Here we actually wipe the database
    while True:
        print("Deleting all user data..")
        db.session.query(User).delete()
        db.session.commit()
        time.sleep(from_second_to_hour(duration))
    
