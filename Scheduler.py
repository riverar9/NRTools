#%%
import schedule
import time
import pickle as pkl
from datetime import datetime, timedelta

import check_email
import SWA_Checkin
import itineraries

time_started = datetime.now()
test = True

#%%

def get_emails():
    print('\nChecking for new emails...')
    check_email.main()
    if test:
        print("Running for: {} minutes".format(str((datetime.now()-time_started).total_seconds()/60)))

def check_queue_and_checkin():
    print("\nChecking if it's almost time to checkin...\n")
    properties =  pkl.load(open('properties.p','rb'))
    flight_list = properties['listings']

    queue = []
    removal = []

    for each in flight_list:
        if (flight_list[each].checkin_datetime - datetime.now()).total_seconds() <= 60:
            queue.append(flight_list[each])
            removal.append(each)
    
    if len(queue) > 0:
        queue.sort(key=lambda x:x.checkin_datetime)

        SWA_Checkin.flight_checkin(queue)

        for each in removal:
            print("Dropping {}".format(each))
            flight_list.pop(each)
        
        properties['listings'] = flight_list

        pkl.dump(properties, open('properties.p','wb'))

        print('\nDone Checking in!')




#%%

if __name__ == "__main__":
    schedule.run_all()
    try:
        schedule.every(10).seconds.do(check_queue_and_checkin)
        schedule.every(30).seconds.do(get_emails)

        while True:
            schedule.run_pending()
            time.sleep(5)
    except:
        pass


#%%
