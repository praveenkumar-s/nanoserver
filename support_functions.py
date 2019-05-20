import requests
import os
import json

# compare and return true if all the elements in obj1 are available under obj2
def dictcompare(request_headers,server_headers):
    if(len(server_headers)==0):
        return True
    else:
        for key in server_headers.keys():
            if(key in request_headers):
                if(request_headers[key] == server_headers[key] or request_headers[key] in server_headers[key]):
                    pass
                else:
                    return False
            else:
                return False
    return True
            
def prepare_response(headers=None, body=None, status_code =None):
    
    return body, status_code , headers



def compare_body( request_body , server_body):
    if(isinstance(server_body, dict) or  isinstance(server_body, list)): # if the server object's body is a dict or a list , do a direct comparison
        return True if request_body==server_body else False
    elif(str(server_body).count('%')==2):     # if wild card operator is available, do a wildcard
        return True if str(server_body).strip('%') in request_body else False
    else:  # for all other cases do a direct search 
        return True if request_body==server_body else False



def nullifier(dict, key):
    try:
        return dict[key]
    except:
        return None


def get_databank(mode):
    if(mode=='true'):
        rs=requests.get('https://qube-endurance.herokuapp.com/api/data_store/saas', headers={"x-api-key":os.environ["ENDURANCE_KEY"]})
        print("Storage Mode: Cloud")
        return rs.json() if rs.status_code==200 else json.load(open('services.json'))
    else:
        print("Storage Mode: Local")
        return json.load(open('services.json'))

def put_databank(mode, data):
    if(mode=='true'):
        rs=requests.post('https://qube-endurance.herokuapp.com/api/data_store/saas', headers={"x-api-key":os.environ["ENDURANCE_KEY"]}, json=data)
        return True if rs.status_code==201 else False
    else:
        with open('services.json', 'w') as outfile:
            json.dump(data, outfile)
        return True

    