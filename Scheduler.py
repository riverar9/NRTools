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
    check_email.main()
    if test:
        print("Running for: {} seconds".format(str((datetime.now()-time_started).total_seconds())))

def check_queue_and_checkin():
    properties =  pkl.load(open('properties.p','rb'))
    flight_list = properties['listings']

    queue = []
    removal = []

    for each in flight_list:
        if (flight_list[each].checkin_datetime - datetime.now()).total_seconds() <= 60:
            queue.append(flight_list[each])
            removal.append(each)
    
    if len(queue) > 0:
        print("\nProcessing Coming due Itineraries:\n")
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
    try:
        schedule.every(1).seconds.do(check_queue_and_checkin)
        schedule.every(5).seconds.do(get_emails)

        schedule.run_all()
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except:
                pass
    except:
        pass


#%%
