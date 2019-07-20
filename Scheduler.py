#%%
import schedule
import time
import pickle as pkl
from datetime import datetime, timedelta

import check_email
import SWA_Checkin
import itineraries

#%%

def get_emails():
    print('Getting new emails...')
    check_email.main()
    print('Back to sleep...\n')

def check_queue_and_checkin():
    print("Checking if it's almost time to checkin...")
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
            print("\nDropping {}".format(each))
            flight_list.pop(each)
        
        properties['listings'] = flight_list

        pkl.dump(properties, open('properties.p','wb'))

        print('\nDone Checking in!')
        print('Back to sleep...')




#%%

if __name__ == "__main__":
    schedule.every(30).seconds.do(get_emails)
    schedule.every(10).seconds.do(check_queue_and_checkin)

    while True:
        schedule.run_pending()
        time.sleep(5)


#%%
