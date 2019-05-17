
from flask import Flask
from flask import request
import json
import support_functions as sf
import objectifier
import json
from jsonschema import validate
import uuid
import requests
from flask import jsonify
import os

app = Flask(__name__)

databank= sf.get_databank(mode= sf.nullifier(os.environ,'ENDURANCE'))

def eval_body(body):
    if(body[0]=='$'):
        return eval(body.lstrip('$'))
    else:
        return body 

@app.route('/', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>/<p2>', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>/<p2>/<p3>', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>/<p2>/<p3>/<p4>', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>/<p2>/<p3>/<p4>/<p5>', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<p7>', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<p7>/<p8>', methods=['POST','GET','PUT','DELETE'])
@app.route('/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<p7>/<p8>/<p9>', methods=['POST','GET','PUT','DELETE'])

def thread_ripper(p1=None , p2 = None , p3 = None , p4 = None , p5 = None , p6 = None , p7 = None , p8 = None , p9 = None):
    path_elements=[]
    path_elements.append(p1)
    path_elements.append(p2)
    path_elements.append(p3)
    path_elements.append(p4)
    path_elements.append(p5)
    path_elements.append(p6)
    path_elements.append(p7)
    path_elements.append(p8)
    path_elements.append(p9)
    

    service_object=None
    try:
        nano_server_key= sf.nullifier(request.headers,'Nano-Server-Key')
        if(nano_server_key==None):
            nano_server_key=request.values['Nano-Server-Key']
        if( nano_server_key in databank.keys()):
            service_object=databank[nano_server_key]
        else:
            return "Requested Service is not available",404
    except:
        return "bad request: header : nano-server-key is mandatory",400
    
    #match maker
    HEADERS=request.headers  # can be accessed from response body for eval
    ARGS= request.values # can be accessed from response body for eval
    REQUEST= request # can be accessed form response body for eval

    for items in service_object['paths']:
        if(request.path.rstrip('/') == items['path'].rstrip('/') and request.method == items['method']):
            for pairs in items['pairs']:
                
                # validate headers
                if(not sf.dictcompare(request.headers , pairs['request']['headers'])):
                    break                    

                # validate body
                if('body' in pairs['request']):
                    if(not sf.compare_body(request.body , pairs['request']['body'])):
                        break

                # validate query params
                if(not sf.dictcompare(request.values , pairs['request']['params'])):
                    break        

                response_obj=pairs['response']
                response_obj['body']= eval_body(response_obj['body'])
                if(isinstance(response_obj['body'], dict)):
                    return jsonify(response_obj['body'])
                return response_obj['body'], response_obj['status_code'],response_obj['headers']
    
    return 'nothing',404


@app.route('/service/add',  methods=['POST'])
def service_add():
    
    incoming_data=request.json
    try:
        validate(incoming_data, json.load(open('incoming_data_schema.json')))
        if(request.headers['Authorization']!=os.environ['Authorization']):
            return 'Invalid key',404
    except:
        return "bad request", 400

    id= uuid.uuid1()
    databank[str(id)]=incoming_data  

    if(sf.put_databank(sf.nullifier(os.environ,'ENDURANCE'), databank)):
        return str(id),200
    else:
        return 'error',500


@app.route('/service/docs', methods=['GET'])
def get_documentation():
    nano_server_key= sf.nullifier(request.headers,'Nano-Server-Key')
    
    try:
        if(nano_server_key==None):
            nano_server_key=request.values['Nano-Server-Key']
        if( nano_server_key in databank.keys()):
            service_object=databank[nano_server_key]
            return jsonify(service_object)
        else:
            return "Requested Service is not available",404
    except:
        return "bad request: header : nano-server-key is mandatory",400




if __name__ == '__main__':
    app.run(debug=False , host='0.0.0.0', port=environ.get("PORT", 5000), threaded=True)
