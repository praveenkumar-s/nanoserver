# nanoserver

    Nanoserver is a service that can accept a API documentation as input and host the mock version of the same. This can be useful to deploy adhoc services over the cloud, when the actual service that we want is not available or not ready yet


# Steps to Add your service to Nano Server: 

    POST: https://<nano-server-url>/service/add

    body:

     ```       {
        "descripton":"this is service for Sharebox service emulation",
        "paths":[
            {
                "path":"/sharebox/api/files",
                "method":"GET",
                "pairs":[
                            {
                                "request":{
                                            "params":{"token":["757d24dc-bd14-4962-920f-efe65ee331af"]},
                                            "headers":{}
                                            },
                                "response":{
                                            "headers":{"Content-Type ":"application/json"},
                                            "body":"[\"hello world\"]",
                                            "status_code":200                                            
                                }

                            }
                        ]
 
            },
            {
                "path":"/",
                "method":"GET",
                "pairs":[
                            {
                                "request":{
                                            "params":{"token":["757d24dc-bd14-4962-920f-efe65ee331af",""]},
                                            "headers":{}
                                            },
                                "response":{
                                            "headers":{"Content-Type ":"application/json"},
                                            "body":"[\"Welcome to sharebox API\"]",
                                            "status_code":200                                            
                                }

                            } 
                        ]

            }
        ]
    }       ```

# response: 
    a uuid will be retuned. This id must be used as `Nano-Server-Key` in further requests to get response for your mock server. 
    Eg: 
    https://<your-server-url>/sharebox/api/files will fetch responses as mentioned in the previously uploaded document

# To get data about the available service documentation for a given nano server id : 
    https://<your-server-url>/service/docs
    header: `Nano-Server-Key`: <key>