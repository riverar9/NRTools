from datetime import datetime
from datetime import timedelta
import requests
import json
from time import gmtime, strftime

class flight_listing:
    def __init__(self, carrier, message):
        if carrier == 'WN':
            # 1A This section goes through the subject to get the confirmation number
            t_subject = message['subject'].replace(' (Love) ',' ').replace(' (Hobby) ','')
            self.confirmation_number = t_subject[t_subject.find("(")+1:t_subject.find(")")]

            # 2A This section goes through the subject to get the passenger's first name
            self.first_name = message['subject'][:message['subject'].find("'s ")]

            # 3A This section uses the body to determine the passenger's last name
            t_full_name = message.get_payload()[message.get_payload().find('TICKET #'):]
            t_full_name = t_full_name[t_full_name.find(self.first_name):]
            t_full_name = t_full_name[:t_full_name.find('<')]
            self.last_name = (t_full_name[:t_full_name.find('\n')-1].split('&nbsp;'))[1]

            # 4A This section uses the body to determine the departure airport
            t_info = message.get_payload()[message.get_payload().find('DEPARTS'):]
            t_info = t_info[t_info.find('\r\nong>')+6:]
            t_airport_time = t_info[:t_info.find('<')]
            t_depart_info = t_airport_time.split(' ')
            self.departure_airport = t_depart_info[0]

            # 4B This section uses the body and the results from 4A to determine the departure datetime
            t_AM_PM = t_info[t_info.find(t_airport_time) + len(t_airport_time):]
            t_AM_PM = t_AM_PM[t_AM_PM.find('span>')+len('span>'):t_AM_PM.find('\r\n')]
            t_depart_time = t_depart_info[1] + ' ' + t_AM_PM
            
            t_depart_date = message.get_payload().replace('\r\n',' ')\
                .replace('Monday','FunDay!')\
                .replace('Tuesday','FunDay!')\
                .replace('Wednesday','FunDay!')\
                .replace('Thursday','FunDay!')\
                .replace('Friday','FunDay!')\
                .replace('Saturday','FunDay!')\
                .replace('Sunday','FunDay!')
            t_depart_date = t_depart_date[t_depart_date.find('FunDay!')+9:t_depart_date.find('FunDay!')+19]
            self.depart_datetime = datetime.strptime(t_depart_date + ' ' + t_depart_time, '%m/%d/%Y %I:%M %p')

            # 5A This section uses the body to determine the destination
            t_destination = message.get_payload()[message.get_payload().find('ARRIVES'):]
            self.destination_airport = t_destination[t_destination.find('\r\nng>')+len('\r\nng>'):t_destination.find('\r\nng>')+len('\r\nng>')+3]

            # 6A This section uses an online resource to figure out when to begin the checkin process
            t_airport_api_link = "https://airports-api.s3-us-west-2.amazonaws.com/iata/{}.json".format(self.departure_airport.lower())
            t_airport_api_data = requests.get(t_airport_api_link)
            t_dep_time = datetime.datetime.now(pytz.timezone(json.loads(t_airport_api_data.text)['timezone']))
            t_cpu_time = datetime.datetime.now()
            t_min_diff = (t_dep_time.hour - t_cpu_time.hour)*60 + (t_dep_time.minute - t_cpu_time.minute)
            self.checkin_datetime = self.depart_datetime - timedelta(minutes=t_min_diff)

