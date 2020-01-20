#%%
import pickle as pkl
import smtplib
import time
import imaplib
import email
import operator
import json

from datetime import datetime

from itineraries import flight_listing

#%%
email_info = json.load(open(r'Input/Inputs.json','r'))

#%%
def main():
	mail = imaplib.IMAP4_SSL(email_info['smtp_server'])
	mail.login(email_info['email_address'],email_info['email_password'])
	mail.select('inbox')

	#%%

	type, data = mail.search(None, 'ALL')
	mail_ids = data[0]
	id_list = mail_ids.split()
	mail_ids = []

	for each in id_list:
		mail_ids.append(int(each))

	#%%

	cur_props = pkl.load(open('properties.p','rb'))

	#%%

	processed_listings = 0

	if cur_props['inboxcount'] != max(mail_ids): #if we have new emails then we'll process them
		print('Processing new emails:')
		for email_id in  range(cur_props['inboxcount'], max(mail_ids)):
			typ, data = mail.fetch(id_list[email_id], '(RFC822)')

			for response in data:
				try:
					if isinstance(response, tuple):
						msg = email.message_from_string(response[1].decode('utf-8'))

						#if it's not from southwest airlines then I don't want it.
						if 'southwestairlines@ifly.southwest.com' in msg['from']:
							this_listing = flight_listing('WN', msg)
							if this_listing.depart_datetime < datetime.now():
								print('{} is in the past, cannot process further.'.format(this_listing.confirmation_number))
							
							#not saving items which aren't in the approved last name list
							elif this_listing.last_name in email_info['approved_last_names']:
								(cur_props['listings'])['WN-' + this_listing.confirmation_number] = this_listing
								print("Processed listing {} from {} to {} on {}".format(\
								this_listing.confirmation_number,\
								this_listing.departure_airport,\
								this_listing.destination_airport,\
								this_listing.depart_datetime
								))
								processed_listings += 1
							else:
								print("{} isn't authorized, add {} to the input file to allow them to list.".format(this_listing.last_name))
								cur_props['unauth_names'] = set(list(cur_props['unauth_names']).append(this_listing.last_name))

				except ValueError:
					print(ValueError)
		print("{} new emails processed.\n".format(max(mail_ids)-cur_props['inboxcount']))
		cur_props['inboxcount'] = max(mail_ids)
	else:
		print('No new emails.')

	pkl.dump(cur_props, open('properties.p','wb'))


#%%


#%%


#%%
