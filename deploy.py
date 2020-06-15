import requests
from requests.auth import HTTPBasicAuth
import json

file=open("readme.txt","r")
data=json.load(file)

url="http://localhost:11111/semarchy/api/rest/app-builder/data-locations/"+data["dloc_name"]+"/deploy"
payload={"modelName": data["name"],"modelEditionKey": data["import_branchId"]+"."+data["import_editionId"]}

response=requests.post(url,json=payload,auth=HTTPBasicAuth('semadmin','semadmin'))
if response.status_code==403:
    print("User must have role SEMARCHY_ADMIN")
elif response.status_code==401:
    print("Unauthorized")
elif response.status_code==500:
    print("Internal Error")
elif response.status_code==404:
    print("Not found")
elif response.status_code==204:
    print("No content, Deployed Successfully")
elif response.status_code==303:
    print("Deployed Successfully")
