

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
    return True if request_body==request_body else False