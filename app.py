
from flask import Flask
from flask import request
import json
import support_functions as sf
import objectifier
import json
from jsonschema import validate
import uuid
app = Flask(__name__)

databank= json.load(open('services.json'))

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

def method_name(p1=None , p2 = None , p3 = None , p4 = None , p5 = None , p6 = None , p7 = None , p8 = None , p9 = None):
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
    print request.headers#del

    service_object=None
    try:
        if( request.headers['Nano-Server-Key'] in databank.keys()):
            service_object=databank[request.headers['Nano-Server-Key']]
        else:
            return "Requested Service is not available",404
    except:
        return "bad request: header : nano-server-key is mandatory",400
    
    #match maker

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
                return response_obj['body'], response_obj['status_code'],response_obj['headers']
    
    return 'nothing',404


@app.route('/service/add',  methods=['POST'])
def service_add():
    incoming_data=request.json
    try:
        validate(incoming_data, json.load(open('incoming_data_schema.json')))
    except:
        return "bad request", 400

    id= uuid.uuid1()
    databank[str(id)]=incoming_data  #pending migration to endurance

    with open('services.json', 'w') as outfile:
        json.dump(databank, outfile)
    return str(id),200


@app.route('/service/docs', methods=['GET'])
def get_documentation():
    try:
        if( request.headers['Nano-Server-Key'] in databank.keys()):
            service_object=databank[request.headers['Nano-Server-Key']]
            return service_object , 200
        else:
            return "Requested Service is not available",404
    except:
        return "bad request: header : nano-server-key is mandatory",400

if __name__ == '__main__':
    app.run()
