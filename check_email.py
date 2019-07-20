#%%
import pickle as pkl
import smtplib
import time
import imaplib
import email
import operator
from itineraries import flight_listing

#%%
def main():
	mail_address	= "autononrev@gmail.com"
	maill_pwd   	= "Rivera1994"
	smtp_server		= "imap.gmail.com"

	#%%

	mail = imaplib.IMAP4_SSL(smtp_server)
	mail.login(mail_address,maill_pwd)
	mail.select('inbox')

	print('\nSuccessfully connected to {} inbox!'.format(mail_address))

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

	if cur_props['inboxcount'] != max(mail_ids): #if we have new emails then we'll process them
		for email_id in  range(cur_props['inboxcount'], max(mail_ids)):
			typ, data = mail.fetch(id_list[email_id], '(RFC822)')

			for response in data:
				if isinstance(response, tuple):
					msg = email.message_from_string(response[1].decode('utf-8'))

					if 'southwestairlines@ifly.southwest.com' in msg['from']:
						this_listing = flight_listing('WN', msg)
						(cur_props['listings'])['WN-' + this_listing.confirmation_number] = this_listing
					print("Processed listing {} from {} to {} on {}".format(\
						this_listing.confirmation_number,\
						this_listing.departure_airport,\
						this_listing.destination_airport,\
						this_listing.depart_datetime
						))

	print("\n{} items added for checkin.\n".format(max(mail_ids)-cur_props['inboxcount']))
	cur_props['inboxcount'] = max(mail_ids)

	pkl.dump(cur_props, open('properties.p','wb'))
