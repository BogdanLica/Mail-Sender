import smtplib
import re
import socket
import os.path
import smtpservers_scraper
import database
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from os.path import basename
import threading


import handle_files



def smtp_connect(domain,port):
    smtpObj = smtplib.SMTP(domain,port,3)
    smtpObj.starttls()

    return smtpObj

def reconnect(email,passwd,domain,port):
    smtpObj = smtp_connect(domain,port)
    smtpObj.login(email,passwd)

    return smtpObj


'''
Put the servers from a file to a list
'''
def get_servers():
    list=[]
    with open("servers.txt","r+") as file:
        for item in file:
            list.append(item.rstrip())

    return list

'''
Valid email based on regex
'''
def valid_email(email):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email)


def extract_domain(email):
    return re.search(r"@(\w+).",email).group(1)

'''
Check if the domain is comment with one of the servers
'''
def valid_servers(list_servers,domain):
    myList=set()
    for server in list_servers:
        if domain in server:
            myList.add(server)
    return myList

def get_server_and_port(domain,email,passwd):
    servers = get_servers()
    servers_to_check = valid_servers(servers,domain)
    

    ports=[25,465,587,2525,2526]

    settings={}
    

    for server_to_check in servers_to_check:
        print("[*] Server '%s' is being checked" %server_to_check)
        for port in ports:
            try:
                smtpObj = smtp_connect(server_to_check,port)
                try:
                    if smtpObj.login(email,passwd) is not None:
                        print("Success on server '%s'" %server_to_check)
                        
                        settings['server'] = server_to_check
                        settings['port'] = port
                        return settings
                except smtplib.SMTPAuthenticationError :
                    break
            except:
                print("[*][*]Trying a different port")

    return None

def fetch_servers():
    if not os.path.exists('servers.txt'):
        print("[*] Fetching servers...")
        smtpservers_scraper.main()
    else:
        print("[*] SMTP Servers fetched")




def save_to_db(email_user,hash_file,recipient):
    MyDB = database.Dababase()

    MyDB.craft_document(email_user,hash_file,recipient)


    MyDB.query()

def check_attachment(file_path):
    my_check = handle_files.VirusTotal()
    result = my_check.scan_file(file_path)


    if result:
        print('[*] Sorry, I cannot attach the file as it is considered malicious...')
    else:
        return handle_files.File_attached(file_path).find()
    
'''
Main loop
'''
def main():
    email=""
    settings={}
    while True :

        email=input("E-mail: ")
        if valid_email(email):

            password=getpass.getpass("Pass: ")


            domain = extract_domain(email)
            print("The domain is %s" %domain)

            settings = get_server_and_port(domain,email,password)
           # server = match_domain_with_servers(domain,email,password)

            if settings is not None:
                recipient = input("Recipient: ")
                subject = input("Subject: ")
                message = input("Message: ")
                print('[*] Sending email...')

                msg = MIMEMultipart()
                msg['From']=email
                msg['To']=recipient
                msg['Subject']=subject

                msg.attach(MIMEText(message))

                attachment_ask=input("Do you want to add an attachment?(Y/N) ")

                if attachment_ask == 'Y':
                    file_path = input('File: ')
                    hash_file = handle_files.File_attached(file_path).sha256sum()
                    
                    full_path = check_attachment(file_path)
                    
                    if full_path is not  None:
                        with open(full_path, "rb") as file:
                             part = MIMEApplication(
                             file.read(),
                             Name=basename(full_path)
                            )
                        part['Content-Disposition'] = "attachment; filename= %s" % file_path
                        
                        msg.attach(part)


                
                
                    
                server = reconnect(email,password,settings['server'],settings['port'])
                server.send_message(msg)

                #server.sendmail(email,recipient,'Subject: %s\r\n%s' %(subject,message))
                server.quit()
                print('[*] Done')

                save_to_db(email,hash_file,recipient)

                break
     
            
            
        else:
            print("E-mail is invalid\n")
            email=input("E-mail: ")



'''
Start the main function
'''
if __name__ == '__main__':
    fetch_servers()
    main()