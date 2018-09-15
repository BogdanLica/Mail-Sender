from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re


'''
Make an HTTP request to the url specified
and if the response is HTML/XML, return the content
otherwise return None
'''
def content_url(URL):
    '''
    The closing makes sure that any network connections used are freed
    '''
    try:
        with closing(get(URL,stream=True)) as response:
            if good_response(response):
                return response.content
            else:
                return None

    except RequestException as e:
        log_error("Error during requests to {0} : {1}").format(URL,str(e))
        return None

'''
Based on the HTTP Status code, return True/False
'''
def good_response(response):
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200 and content_type is not None and content_type.find("html") > -1)


def log_error(err):
    print(err)


'''
Look for tables in the HTML
Based on the regex, extract the text which is between "." like smtp.google.com
Regex: \w+\.\w+\.\w+
'''
def get_servers(html):
    print("[*] Extracting the list...")
    list = set()
    for i,tag in enumerate(html.select('td')):
        if(check_valid_server(tag.text)):
            list.add(tag.text)
        
    return list

def check_valid_server(line):
    return re.match("\w+\.\w+\.\w+",line)

'''
Write the list obtained to a file on the system
'''
def write_list_to_file(list_servers):
    file_content = set()
    with open('servers.txt','w+') as file:
            for line in file:
                file_content.add(line)
            union_sets = list_servers | file_content ## file_content.update(list_servers)
            for item in union_sets:  
                file.write("%s\n" %item)

def main():

    sources=["https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html",
    "https://domar.com/smtp_pop3_server",
    "http://www.e-eeasy.com/SMTPServerList.aspx"
    ]
    for URL in sources:
        print("[*] Sending the request to %s" %URL)
        html_received = content_url(URL)
        print("[*] Valid content received, making it parsable...")
        html_parsable = BeautifulSoup(html_received,'html.parser')
        print("[*] Writing the list to a file...")
        write_list_to_file(get_servers(html_parsable))
        print("[*] Done")
    
if __name__ == '__main__':
    main()
