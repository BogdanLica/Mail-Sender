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
    list = []
    for i,tag in enumerate(html.select('td')):
        if(check_valid_server(tag.text)):
            list.append(tag.text)
        
    return list

def check_valid_server(line):
    return re.match("\w+\.\w+\.\w+",line)

'''
Write the list obtained to a file on the system
'''
def write_list_to_file(list_servers):
    with open('servers.txt','w') as file:
        for item in list_servers:
            file.write("%s\n" %item)



def main():
    URL= "https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html"
    print("[*] Sending the request to %s" %URL)
    html_received = content_url(URL)
    print("[*] Valid content received, making it parsable...")
    html_parsable = BeautifulSoup(html_received,'html.parser')
    print("[*] Writing the list to a file...")
    write_list_to_file(get_servers(html_parsable))
    print("[*] Done")
    
if __name__ == '__main__':
    main()
