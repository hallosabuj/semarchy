import requests
from requests.auth import HTTPBasicAuth
import json

file=open("readme.txt",'r')
data=json.load(file)
filename=data["name"]+"["+data["export_branchId"]+"."+data["export_editionId"]+"].xml"
print(filename)
if data['export_editionId']==data['import_editionId']:
    url="http://localhost:11111/semarchy/api/rest/app-builder/models/"+data["name"]+"/editions/"+data['import_branchId']+"."+data['import_editionId']+"/content"
    model_data=open(filename,"r").read()
    response=requests.post(url,data=model_data,auth=HTTPBasicAuth('semadmin','semadmin'))
    if response.status_code==403:
        print("User must have role SEMARCHY_ADMIN")
    elif response.status_code==401:
        print("Unauthorized")
    elif response.status_code==500:
        print("Internal Error")
    elif response.status_code==404:
        print("Not found")
    elif response.status_code==204:
        print("No Content, Imported Successfully")
    elif response.status_code==400:
        print("Bad request")
    else:
        print(response.status_code)
    print("When both editionId are same")
else:
    model_close_url="http://localhost:11111/semarchy/api/rest/app-builder/models/"+data["name"]+"/editions/"+data['import_branchId']+"."+data['import_editionId']+"/close"
    payload={"description":"Closed Successfully"}
    close_response=requests.post(model_close_url,json=payload,auth=HTTPBasicAuth('semadmin','semadmin'))
    if close_response.status_code==403:
        print("User must have role SEMARCHY_ADMIN")
    elif close_response.status_code==401:
        print("Unauthorized")
    elif close_response.status_code==500:
        print("Internal Error")
    elif close_response.status_code==404:
        print("Not found")
    elif close_response.status_code==400:
        print("Bad request")
    elif close_response.status_code==200:
        print("Closed Successfully",close_response.status_code)
        #Now importing the model
        data['import_editionId']=data['export_editionId']
        file=open("readme.txt",'w')
        file.write(json.dumps(data))
        file.close
        url="http://localhost:11111/semarchy/api/rest/app-builder/models/"+data["name"]+"/editions/"+data['import_branchId']+"."+data['import_editionId']+"/content"
        model_data=open(filename,"r").read()
        response=requests.post(url,data=model_data,auth=HTTPBasicAuth('semadmin','semadmin'))
        if response.status_code==403:
            print("User must have role SEMARCHY_ADMIN")
        elif response.status_code==401:
            print("Unauthorized")
        elif response.status_code==500:
            print("Internal Error")
        elif response.status_code==404:
            print("Not found")
        elif response.status_code==204:
            print("No Content, Imported Successfully")
        elif response.status_code==400:
            print("Bad request")
        else:
            print(response.status_code)
    else:
        print("Unknown",close_response.status_code)
