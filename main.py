import smtplib
import re
import socket
import os.path
import smtpservers_scraper
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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

def match_domain_with_servers(domain,email,passwd):
    servers = get_servers()
    servers_to_check = valid_servers(servers,domain)
    

    ports=[25,465,587,2525,2526]

    

    for server_to_check in servers_to_check:
        print("[*] Server '%s' is being checked" %server_to_check)
        for port in ports:
            try:
                smtpObj = smtplib.SMTP(server_to_check,port,None,3)

                smtpObj.starttls()
                try:
                    if smtpObj.login(email,passwd) is not None:
                        print("Success on server '%s'" %server_to_check)
                        return smtpObj
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



'''
Main loop
'''
def main():
    email=""
    password=""
    while True :

        email=input("E-mail: ")
        if valid_email(email):

            password=input("Pass: ")


            domain = extract_domain(email)
            print("The domain is %s" %domain)


            server = match_domain_with_servers(domain,email,password)

            if server is not None:
                recipient = input("Recipient: ")
                subject = input("Subject: ")
                message = input("Message: ")
                print('[*] Sending email...')

                msg = MIMEMultipart()
                msg['From']=email
                msg['To']=recipient
                msg['Subject']=subject

                msg.attach(MIMEText(message))
                server.send_message(msg)


                #server.sendmail(email,recipient,'Subject: %s\r\n%s' %(subject,message))
                server.quit()
                print('[*] Done')
                break
            #print(server)




            
            
        else:
            print("E-mail is invalid\n")
            email=input("E-mail: ")



'''
Start the main function
'''
if __name__ == '__main__':
    fetch_servers()
    main()