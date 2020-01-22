#%%
import schedule
import time
import pickle as pkl
from datetime import datetime, timedelta
from yaspin import yaspin
import json

import check_email
import SWA_Checkin
import itineraries

json_inputs = json.load(open(r'Input/Inputs.json','r'))

time_started = datetime.now()
test = False

#%%

def get_emails():
    with yaspin(text='Checking for Emails...', color='blue') as sp:
        sp.write(check_email.main())
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
        with yaspin(text='Checking into {} flights...'.format(len(queue)), color='blue') as sp:
            queue.sort(key=lambda x:x.checkin_datetime)

            SWA_Checkin.flight_checkin(queue)

            for each in removal:
                sp.write("Dropping {}".format(each))
                flight_list.pop(each)
            
            properties['listings'] = flight_list

            pkl.dump(properties, open('properties.p','wb'))

            sp.write('Done Checking in!')




#%%

if __name__ == "__main__":
    try:
        schedule.every(json_inputs['check_queue_interval_secs']).seconds.do(check_queue_and_checkin)
        schedule.every(json_inputs['email_check_interval_secs']).seconds.do(get_emails)

        schedule.run_all()
        while True:
            try:
                schedule.run_pending()
                time.sleep(5)
            except:
                pass
    except:
        pass


#%%
