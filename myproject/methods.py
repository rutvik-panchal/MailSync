import smtplib,imaplib, email, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders




def checkAuth(email_user,email_password):
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)
        server.close()
        return 1
    except:
        return 0


def sendMail(email_user,email_password,email_send,subject,body):

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    msg.attach(MIMEText(body,'plain'))
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()

def getMail(user_mailid, password):

    imap_url = 'imap.gmail.com'
    #Where you want your attachments to be saved (ensure this directory exists)
    attachment_dir = 'your_attachment_dir'
    # sets up the auth

    user = user_mailid
    password = password

    def auth(user,password,imap_url):
        con = imaplib.IMAP4_SSL(imap_url)
        con.login(user,password)
        return con
    # extracts the body from the email
    def get_body(msg):
        if msg.is_multipart():
            return get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None,True)
    # allows you to download attachments
    def get_attachments(msg):
        for part in msg.walk():
            if part.get_content_maintype()=='multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(attachment_dir, fileName)
                with open(filePath,'wb') as f:
                    f.write(part.get_payload(decode=True))
    #search for a particular email
    def search(key,value,con):
        result, data  = con.search(None,key,'"{}"'.format(value))
        return data
    #extracts emails from byte array
    def get_emails(result_bytes):
        msgs = []
        for num in result_bytes[0].split():
            typ, data = con.fetch(num, '(RFC822)')
            msgs.append(data)
        return msgs

    con = auth(user,password,imap_url)
    con.select('INBOX')
    sender = [15]
    bodyarray = [15]
    result, data1 = con.search(None, "ALL")
    counter = 0
    for num in data1[0].split() :
        counter += 1
    for i in range (-1,-15,-1) :

        result, data = con.fetch(data1[0].split()[i],'(RFC822)')
        raw = email.message_from_bytes(data[0][1])
        sender.append(raw['FROM'])
        abcd = get_body(raw)
        bodyarray.append(abcd)


    #get_attachments(raw)
    info=[sender,bodyarray]
    return info

def getSent(user,password):

    imap_url = 'imap.gmail.com'
    #Where you want your attachments to be saved (ensure this directory exists)
    attachment_dir = 'your_attachment_dir'
    # sets up the auth

    user = user_mailid
    password = password

    def auth(user,password,imap_url):
        con = imaplib.IMAP4_SSL(imap_url)
        con.login(user,password)
        return con
    # extracts the body from the email
    def get_body(msg):
        if msg.is_multipart():
            return get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None,True)
    # allows you to download attachments
    def get_attachments(msg):
        for part in msg.walk():
            if part.get_content_maintype()=='multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(attachment_dir, fileName)
                with open(filePath,'wb') as f:
                    f.write(part.get_payload(decode=True))
    #search for a particular email
    def search(key,value,con):
        result, data  = con.search(None,key,'"{}"'.format(value))
        return data
    #extracts emails from byte array
    def get_emails(result_bytes):
        msgs = []
        for num in result_bytes[0].split():
            typ, data = con.fetch(num, '(RFC822)')
            msgs.append(data)
        return msgs

    con = auth(user,password,imap_url)
    con.select('SENT')
    sender = [15]
    bodyarray = [15]
    result, data1 = con.search(None, "ALL")
    counter = 0
    for num in data1[0].split() :

        result, data = con.fetch(data1[0].split()[i],'(RFC822)')
        raw = email.message_from_bytes(data[0][1])
        sender.append(raw['FROM'])
        abcd = get_body(raw)
        bodyarray.append(abcd)


    #get_attachments(raw)
    info=[sender,bodyarray]
    return info
