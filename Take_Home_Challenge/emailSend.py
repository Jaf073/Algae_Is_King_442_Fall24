from email.message import EmailMessage
import ssl
import smtplib
from splitInfo_02 import splitInfo

emailSender = 'plzdontbegone@gmail.com' # put your own here while testing

senderPass = 'zztdejhesnxyhxsu'  # NOTE: You want to use something called an "app password" for this field, it's something that you can set up with gmails ONLY if you have two factor authentication enabled
# obviously don't leave this filled in when you push to git

emailVictim = '' # put somebody you don't like here while testing

Dic1, Dic2, Dic3, Dic4, Dic5 = splitInfo('finished')

with open('email_template.txt', 'r') as file:
          email_template = file.read()

def replaceEmails(name_dic, dic_num):
    filledOutEmails = []
    for name, emailVictim in name_dic.items():
        email = EmailMessage()
        email['From'] = emailSender
        email['To'] = emailVictim
        email['Subject'] = 'This is a test email subject'

        contents = email_template

        if dic_num == 1 or dic_num == 2:
            contents = contents.replace('[college]', 'College of Engineering and Science')

        if dic_num == 3:
            contents = contents.replace('[college]', 'College of Applied and Natural Sciences')

        if dic_num == 4:
            contents = contents.replace('[college]', 'College of Education and Human Sciences')

        if dic_num == 5:
            contents = contents.replace('[college]', 'College of Liberal Arts')
            

        #contents = email_template
        contents = contents.replace('[target]', name)
        contents = contents.replace('fakeemail@email.com', emailSender)
        contents = contents.replace('[your worst nightmare]', emailSender)

        email.set_content(contents)

        #with open('IESB.jpeg', 'rb') as img:
            #email.add_attachment(img.read(), maintype='image', subtype='jpeg', filename='IESB.jpeg')

        filledOutEmails.append(email)

    return filledOutEmails

preppedEmails = []
preppedEmails.extend(replaceEmails(Dic1, 1))
preppedEmails.extend(replaceEmails(Dic2, 2))
preppedEmails.extend(replaceEmails(Dic3, 3))
preppedEmails.extend(replaceEmails(Dic3, 4))
preppedEmails.extend(replaceEmails(Dic3, 5))

context = ssl.create_default_context()

for email in preppedEmails:
    emailVictim = email['To']

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(emailSender, senderPass)
    
        # uncommenting the following command will send the email out
        # DO NOT UNCOMMENT THIS DURING LARGE SCALE TESTING
        #emailVictim = '' # if you want to do your own. put a 'break' after the next line
        smtp.sendmail(emailSender, emailVictim, email.as_string())
