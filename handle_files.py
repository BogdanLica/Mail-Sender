'''
Virus total creds:
user:
bozub@hurify1.com
password:
password
'''



'''
Take the hash of the file and search for it
If no match then submit the file and see the response

'''

import os
import hashlib
import requests
import json
import time
class File_attached(object):
    def __init__(self,file,folder):
        self.name = file
        self.query_folder = folder

    def find(self):
        for root,dirs,files in os.walk(self.query_folder):
            if self.name in files:
                return os.path.join(root,self.name)



    def sha256sum(self):
        filename = self.find()
        with open(filename, 'rb') as f:
            tmp = hashlib.sha256()
            while True:
                data = f.read(8192)
                if not data:
                    break
                tmp.update(data)
            return tmp.hexdigest()



class VirusTotal(object):

    def __init__(self):
        self.api_key="926ce5e57bcd578480e56183cdb6f013e2d17af4f72f7418f2914919cca70c5d"
        #self.base_url="https://www.virustotal.com/vtapi/v2/"
        self.scan_url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        self.report_url = 'https://www.virustotal.com/vtapi/v2/file/report'
        self.check_hash = 'https://www.virustotal.com/vtapi/v2/file/rescan'
        self.HTTP_OK=200
        self.HTTP_RATE_EXCEEDED=204
        self.HTTP_BAD_REQUEST=400
        self.HTTP_FORBIDDEN=403
        self.response_code_successful = 1
        self.response_code_queued_for_analysis = -2
        self.response_code_not_in_db = 0
        self.response_code_unexpected_error = -1
        self.scan_finished = True

    def api_key_exists(self):
        return self.api_key is not None


    '''
    Check it too many requests were done, if so then wait
    '''

    def scan_file(self,file_path,folder_path):
        tmp = File_attached(file=file_path,folder=folder_path)
        hash = tmp.sha256sum()

        response_code = ''
        json_response = ''

        while response_code != self.response_code_successful:

            json_response = self.get_report(hash)
            response_code = json_response['response_code']


            if response_code == self.response_code_not_in_db :
                self.unrecognised_file(tmp.find())
                response_code = -10
            elif response_code == self.response_code_queued_for_analysis:
                print('[*] File queued for analysis...') 
            elif response_code == self.response_code_unexpected_error:
                print('[*]There was an error scanning your file...') 

    
        #print("The response code is %s" % (response_code))

        return self.is_malicious(json_response)



    

    def is_malicious(self,json_document):
        return self.analyze_report(json_document)

    def analyze_report(self,json_document):
        print('[*] Analysing the results...')

        positives = json_document['positives']
        total = json_document['total']
        if positives > total / 4:
            return True
        else:
            return False


        ## take hash and query it
        ## if no result then call unrecognaised_file

    def unrecognised_file(self,file_path):
        print('[*] Sending the file for a scan...')
        params = {'apikey': self.api_key}
        file = {'file': (file_path,open(file_path,'rb'))}
        response = requests.post(self.scan_url,files = file,params=params)
        print('[*] File sent...')
        return response.json()


    def get_report(self,sha256hash):
        params = {'apikey':self.api_key,
                   'resource':sha256hash}


        header = {
            'Accept-Encoding':'gzip, deflate',
            'User-Agent': 'gzip, My python script to test files'
        }


        response = requests.get(self.report_url,params=params, headers=header)

        while response.status_code != self.HTTP_OK:
            if response.status_code == self.HTTP_RATE_EXCEEDED:
                #wait()
                print("[*] Too many API calls...")
                print("[*] Sleeping for 60 seconds...")

                time.sleep(60)
                
            elif response.status_code == self.HTTP_FORBIDDEN or response.status_code == self.HTTP_BAD_REQUEST:
                print("[*] There was an error trying to scan the file")
            response = requests.get(self.report_url,params=params, headers=header)
        return response.json()