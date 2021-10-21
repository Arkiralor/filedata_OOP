'''
Main executable Python Script.
'''

from posix import ST_WRITE
import requests as re
import json as js
import os
import datetime as dt
import base64 as bs

from requests import cookies

BASE_PATH = 'files/'

class FileReturn():
    
    #I REAAALLLY hope I don't have to comment this:
    def __init__(self, base_path):
        self.BASE_PATH = base_path


    #Method to read the UNIX timestamp when the files were last updated:
    def timestamp_read(self):
        with open('last_access.txt', 'rt') as ts:
            timestamp = float(ts.read())

        return timestamp


    #Method to write a UNIX timestamp to a .txt file:
    def timestamp_write(self):
        time_stamp = dt.datetime.now().timestamp()
        time_stamp = str(time_stamp)

        with open('last_access.txt', 'wt') as ts:
            ts.write(time_stamp)


    #Method to encode the file contents in Base64 format:
    def file_encode(self, input_string):
        encoded_string = bs.b64encode(input_string)
        return encoded_string

    
    #Method to scrape the contents of the file:
    def file_reader(self, filename):
        BASE_PATH = "files/"
        with open(BASE_PATH + filename, 'rb') as file:
            file_bdata = file.read()
            encoded_data = self.file_encode(file_bdata)
        return encoded_data

    
    #Method to construct & return the {file: filedata} dictionaries:
    def file_handler(self, BASE_PATH):
        
        #Empty dictionary to store output:
        payload = {"results":[]}
        #List out all the files in the given path:
        files = os.listdir(BASE_PATH)
        try:
            for file in files:
                #If the file was last modified after the last file list was updated and hence,
                #the timestamp was taken:
                if os.path.getmtime(BASE_PATH+file)  > self.timestamp_read():
                    filedata = self.file_reader(file)
                    payload['results'].append({"file_name":file, "content_base64":filedata})
            
            #Return the list of dictionaries -> filename: filedata:
            return payload
        except Exception as e:
            return {'Error':f'Code #{e}. Could not retrive file data.'}
        
    
    #Method to call all the functions:
    def main(self):
    
        file_tuples = self.file_handler(self.BASE_PATH)
        print(file_tuples)
        
        payload_login = {"username":"my_username", "password":"my_password"}
        login_url = " https://7988-103-219-61-230.ngrok.io/login"
        response = re.post(login_url, json=payload_login)
        token = response.cookies.get_dict()['csrf_access_token']

        cookies = response.cookies

        headers = {
        'accept': '*/*',
        'X-CSRF-TOKEN': token,
        'Content-Type': 'application/json',
        }

        params = (
            ('project_id', 'files'),
            ('force_project_creation', 'false')
        )

        send_url = 'https://7988-103-219-61-230.ngrok.io/allure-docker-service/send-results'

        sent_response = re.post(
                            send_url, 
                            headers=headers, 
                            params=params, 
                            json=file_tuples,
                            cookies=cookies
                        )
        print(sent_response.content)
        
        #Update the timestamp if request was successful:
        if sent_response.status_code==200:
            self.timestamp_write()
        
        #Print the request response:
        print(sent_response)


if __name__ == "__main__":
    filer = FileReturn(BASE_PATH)
    filer.main()