import json
import requests
from requests.auth import HTTPBasicAuth

file=open("readme.txt",'r')
data=json.load(file)
filename=data["name"]+"["+data["import_branchId"]+"."+data["import_editionId"]+"].xml"
print(filename)

#Close at Test Server
model_close_url_test="http://localhost:11111/semarchy/api/rest/app-builder/models/"+data["name"]+"/editions/"+data['import_branchId']+"."+data['import_editionId']+"/close"
payload_test={"description":"Closed Successfully"}
close_response_test=requests.post(model_close_url_test,json=payload_test,auth=HTTPBasicAuth('semadmin','semadmin'))
if close_response_test.status_code==200:
    print("Closed at test server")

#Close at Dev Server
model_close_url_dev="http://localhost:8088/semarchy/api/rest/app-builder/models/"+data["name"]+"/editions/"+data['import_branchId']+"."+data['import_editionId']+"/close"
payload_dev={"description":"Closed Successfully"}
close_response_dev=requests.post(model_close_url_dev,json=payload_dev,auth=HTTPBasicAuth('semadmin','semadmin'))
if close_response_dev.status_code==200:
    print("Closed at dev server")

if close_response_dev.status_code==200 and close_response_test.status_code==200:
    #Export the closed model
    export_url="http://localhost:11111/semarchy/api/rest/app-builder/models/"+data["name"]+"/editions/"+data['import_branchId']+"."+data['import_editionId']+"/content"
    export_response=requests.get(export_url,auth=HTTPBasicAuth('semadmin','semadmin'))
    if export_response.status_code==403:
        print("EXPORT User must have role SEMARCHY_ADMIN")
    elif export_response.status_code==401:
        print("EXPORT Unauthorized")
    elif export_response.status_code==500:
        print("EXPORT Internal Error")
    elif export_response.status_code==404:
        print("EXPORT Not found")
    elif export_response.status_code==200:
        #Update readme.txt
        data['import_editionId']=str(int(data['import_editionId'])+1)
        data['export_editionId']=str(int(data['export_editionId'])+1)
        file=open("readme.txt",'w')
        file.write(json.dumps(data))
        file.close
        #import the closed model to the Production Server
        import_url="http://localhost:9999/semarchy/api/rest/app-builder/model-imports"
        headers = {'Content-type': 'application/octet-stream'}
        payload=export_response.text
        import_response=requests.post(import_url,data=payload,auth=HTTPBasicAuth('semadmin','semadmin'),headers=headers)
        if import_response.status_code==403:
            print("User must have role SEMARCHY_ADMIN")
        elif import_response.status_code==401:
            print("Unauthorized")
        elif import_response.status_code==500:
            print("Internal Error")
        elif import_response.status_code==404:
            print("Not found")
        elif import_response.status_code==400:
            print("Bad request")
        elif import_response.status_code==200:
            print("Imported successfully")
            file=open("readme.txt","r")
            data=json.load(file)
            deploy_url="http://localhost:9999/semarchy/api/rest/app-builder/data-locations/"+data["dloc_name"]+"/deploy"
            #print("Deploy_url",deploy_url)
            deploy_payload={"modelName": data["name"],"modelEditionKey": data["import_branchId"]+"."+str(int(data["import_editionId"])-1)}
            #print("Deploy_payload",deploy_payload)
            deploy_response=requests.post(deploy_url,json=deploy_payload,auth=HTTPBasicAuth('semadmin','semadmin'))
            if deploy_response.status_code==403:
                print("User must have role SEMARCHY_ADMIN")
            elif deploy_response.status_code==401:
                print("Unauthorized")
            elif deploy_response.status_code==500:
                print("Internal Error")
            elif deploy_response.status_code==404:
                print("Not found")
            elif deploy_response.status_code==204:
                print("No content, Deployed Successfully")
            elif deploy_response.status_code==303:
                print("Deployed Successfully")
    elif export_response.status_code==400:
        print("EXPORT Bad request")
    else:
        print("EXPORT Unable to export")
else:
    print("Unable to close model")
