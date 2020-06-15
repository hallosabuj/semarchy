import requests
import sys
from requests.auth import HTTPBasicAuth
import json

if len(sys.argv)==1:
    branchId="0"
    editionId="0"
else:
    branchId=sys.argv[1]
    editionId=sys.argv[2]
file=open("readme.txt","r")
filename=json.load(file)['name']
#here we have to provide tha name and branchId and editionId
url="http://localhost:8088/semarchy/api/rest/app-builder/models/"+filename+"/editions/"+branchId+"."+editionId+"/content"
response=requests.get(url,auth=HTTPBasicAuth('semadmin','semadmin'))
if response.status_code==403:
    print("User must have role SEMARCHY_ADMIN")
elif response.status_code==401:
    print("Unauthorized")
elif response.status_code==500:
    print("Internal Error")
elif response.status_code==404:
    print("Not found")
elif response.status_code==200:
    filename=filename+"["+branchId+"."+editionId+"].xml"
    #Opening a file with the specified filename and storing data
    file=open(filename,"w")
    file.write(response.text)
    file.close()
    #Updating export branchId and editionId
    file=open("readme.txt",'r')
    data=json.load(file)
    data["export_branchId"]=branchId
    data["export_editionId"]=editionId
    file=open("readme.txt",'w')
    file.write(json.dumps(data))
    file.close

elif response.status_code==400:
    print("Bad request")
