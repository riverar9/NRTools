#%%
import pickle as pkl
import smtplib
import time
import imaplib
import email

#%%

def get_full_name(ebody, config, anchor):
	if config == 'WN':
		result = ebody[ebody.find('TICKET #'):]
		result = result[result.find(anchor):]
		result = result[:result.find('<')]
		return result[:result.find('\n')-1].split('&nbsp;')

def get_PNR(esubject, airline):
	if airline == 'WN':
		return esubject[esubject.find("(")+1:esubject.find(")")]

def get_depart_info(ebody, config):
	if config == 'WN':
		info = ebody[ebody.find('DEPARTS'):]
		info = info[info.find('\r\nong>')+6:]
		airport_time = info[:info.find('<')]
		
		AM_PM = info[info.find(airport_time) + len(airport_time):]
		AM_PM = AM_PM[AM_PM.find('span>')+len('span>'):AM_PM.find('\r\n')]

		d_date = ebody.replace('\r\n','')
		d_date = d_date[d_date.find('date')+6:d_date.find('date')+22]
		d_date = d_date.rstrip().replace('=','').replace(' ','')

		result = airport_time.split(' ')
		result[1] = result[1] + ' ' + AM_PM

		result.append(d_date)
		
		return result

#%%

mail_address	= "autononrev@gmail.com"
maill_pwd   	= "Rivera1994"
smtp_server		= "imap.gmail.com"

#%%

mail = imaplib.IMAP4_SSL(smtp_server)
mail.login(mail_address,maill_pwd)
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

if cur_props['inboxcount'] != max(mail_ids): #if we have new emails then we'll process them
	for email_id in  range(cur_props['inboxcount'], max(mail_ids)):
		print('\n\nItinerary:')
		typ, data = mail.fetch(id_list[email_id], '(RFC822)')

		for response in data:
			if isinstance(response, tuple):
				msg = email.message_from_string(response[1].decode('utf-8'))

				if 'southwestairlines@ifly.southwest.com' in msg['from']:
					airline = 'WN'
					
					em_sub = msg['subject']
					em_sub_fn = em_sub[:em_sub.find("'s ")]

					PNR = get_PNR(em_sub, airline)
					full_name = get_full_name(msg.get_payload(), airline ,em_sub_fn)
					depart_info = get_depart_info(msg.get_payload(), airline)

					print(full_name)
					print(PNR)
					print(depart_info)



	#pkl.dump(, open('properties.p','wb'))

#%%

# first_email_id = int(id_list[0])
# latest_email_id = int(id_list[-1])


# for i in range(latest_email_id,first_email_id, -1):
	# typ, data = mail.fetch(i, '(RFC822)' )

	# for response_part in data:
		# if isinstance(response_part, tuple):
			# msg = email.message_from_string(response_part[1])
			# email_subject = msg['subject']
			# email_from = msg['from']
			# print 'From : ' + email_from + '\n'
			# print 'Subject : ' + email_subject + '\n'


#%%
