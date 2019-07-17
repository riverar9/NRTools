#%%
import pickle as pkl
import smtplib
import time
import imaplib
import email

#%%

def get_full_name(embody, airline):
	if airline == 'SWA':
		Full_Name = email_html[email_html.find('TICKET #'):]
		Full_Name = Full_Name[Full_Name.find(cur_props['Name_Locator'])+len(cur_props['Name_Locator']):]
		Full_Name = Full_Name[Full_Name.find('>'):]
		Full_Name = Full_Name[:Full_Name.find('<')]
		Full_Name = Full_Name.replace('>','').replace("\r\n",'').rstrip().lstrip().split('&nbsp;')
		return Full_Name

#%%

mail_address  = "autononrev@gmail.com"
maill_pwd    = "Rivera1994"
smtp_server = "imap.gmail.com"

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
	mail_ids.append(bytes(each))

#%%

cur_props = pkl.load(open('properties.p','rb'))

#%%

if cur_props['inboxcount'] != max(mail_ids): #if we have new emails then we'll process them
	for email_ids in  range(cur_props['inboxcount'], max(mail_ids)):
		typ, data = mail.fetch(1, '(RFC822)')
		msg = email.message_from_string(email[1].decode('utf-8'))

		if msg['from'] == '"Southwest Airlines" <southwestairlines@ifly.southwest.com>':

			email_subject = msg['subject']
			
			PNR = email_subject[email_subject.find("(")+1:email_subject.find(")")]
			
			f_name, l_name = get_full_name(msg.get_payload(), 'SWA')
			



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
