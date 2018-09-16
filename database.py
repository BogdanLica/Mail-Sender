import pymongo
from mongoengine import *
import hashlib


class Dababase:
    my_database = None
    tmp_document = None
    
    def __init__(self):
        self.my_database = self.getClient()['mail']

    def getClient(self):
        return pymongo.MongoClient('mongo',27017)
    
    def craft_document(self,email,hash_file,recipient):
        
        id_user = hashlib.sha256(email.encode('utf-8')).hexdigest()

        self.my_database['mail'].update_many(
                                            {'id_user' : id_user},
                                            {'$set':{'email' : email}},
                                            True

        )
        self.update_hashes(hash_file,id_user)
        self.update_recipients(recipient,id_user)
        


    def update_hashes(self,new_hash,id_user):
        self.my_database['mail'].update_many(
                                        {'id_user' : id_user},
                                        {'$push' : {'hash_files' : new_hash}},
                                        True
        )


    def update_recipients(self,new_recipient,id_user):
        self.my_database['mail'].update_many(
                                        {'id_user' : id_user},
                                        {'$push' : {'recipients' : new_recipient}},
                                        True
        )

    #def getTables():
    #    return db['users']


    def query(self):
        for document in self.my_database['mail'].find():
            print(document)





class Page(Document):
    id_user=StringField(required=True)
    email = EmailField(required=True)
    hash_files = ListField(StringField())
    recipients = ListField(EmailField(required=True))






'''
    meta = {
        'id_user':'md5_hash_of_email',
        'email': 'myemail',
        'recipients' : [
            'me',
            'and me'
        ],
        'hash_files' : [
            'SD3113',
            'DAHJ23',
            'FDSK8F'
        ]
    }
    '''