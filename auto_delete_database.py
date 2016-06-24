"""

This piece of code deletes all entries from the database every 48 hours.

"""
import time
from app.models import User
from app import db
import sys
from datetime import datetime,timedelta

def from_hour_to_total_seconds(num_hours):
    seconds_per_minute = 60
    minutes_per_hour = 60
    return seconds_per_minute*minutes_per_hour*num_hours

if __name__ == '__main__':

    #Here we are setting up the duration that we should wait before wiping the database, this is set to 48 hours by default
    duration = str(input("Enter the duration user information should persist (in hours, default is 48):"))
    if duration == '':
        duration = 48
    if not duration.isdigit():
        duration = 48
    else:
        duration = int(duration)

    #yes_no is a check to make sure you actually want to do this and didn't just hit the database by accident
    yes_no = ''
    while True:
        yes_no = str(input("Are you sure you want to delete all users every "+str(duration)+" hours?(y/n)"))
        yes_no = yes_no.strip()
        if yes_no == "y" or yes_no == "n":
            break
        else:
            print("please enter y or n, for yes or no, respectively")

    #Here we actually wipe the database
    if yes_no == 'n':
        sys.exit(0)
        
    while True:
        print("Deleting all user data..")
        two_days_ago = datetime.now() - timedelta(days=2)
        to_delete = db.session.query(User).filter(User.timestamp<two_days_ago).all()
        [db.session.delete(deleteable_element) for deleteable_element in to_delete]
        db.session.commit()
        time.sleep(from_hour_to_total_seconds(duration))
    
