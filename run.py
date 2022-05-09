from operator import indexOf
import requests
import json
import csv

org_id= '4100b0a1f9f' #update your org id
access_token='Bearer e05c2dfsdfsd323ds'. #update access token

env= { #update env names and env id as per it.
    "dev": "d4e2a5f6-bfbd26c45", 
    "test": "4fca05ca-e599-4f",
    "pre-prod": "04dbbed3-968f5030",
    "prod": "695b02c5"
}

for key in env:
    url = "https://anypoint.mulesoft.com/cloudhub/api/v2/applications"

    payload={}
    headers = {
    'Authorization': access_token,
    'X-ANYPNT-ORG-ID': org_id,
    'X-ANYPNT-ENV-ID': env[key],
    'Cookie': 'XSRF-TOKEN=pllZ94Ou-fVF3Invs71fV_iQbGvjfBWyxcNw; _csrf=qIRYYRVngWKlL1QEitO_rMb9; mulesoft.sess=eyJpZCI6ImxZVGxzcnN3ckxFd0ZQWlRLSUdHS21aZFprNHlFOWk0IiwibWZhX3VzZXJfaWQiOiIyNGUzODk5ZS0xY2FiLTRiM2ItYjI3NS01MDY5OTg4ODcwMzUifQ==; mulesoft.sess.sig=DpMrPraA8nkA75eYOLynKfkW8wg; mulesoft.vaas.sess=eyJpZCI6ImxZVGxzcnN3ckxFd0ZQWlRLSUdHS21aZFprNHlFOWk0IiwibWZhX3VzZXJfaWQiOiIyNGUzODk5ZS0xY2FiLTRiM2ItYjI3NS01MDY5OTg4ODcwMzUifQ=='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.json())
    apis = response.json()

    # Serializing json 
    json_object = json.dumps(apis, indent = 4)
    
    # Writing to sample.json
   #  with open(env[key]+"sample.json", "w") as outfile:
    #    outfile.write(json_object) """

    apiDict={}
    apiDetails=[]
    #you can select more properties as well as per your requoirement
    for api in apis:
        apiDict={}
        apiDict['apiName']=api['domain']
        apiDict['apiBuildVersion']=api['properties']['appVersion']
        apiDict['apiConfigVersion']=api['properties']['configVersion']
        apiDict['muleRuntimeVersion']=api['muleVersion']['version']
        apiDict['apiDeployedEnv']=api['properties']['env']
        apiDict['apiStatus']=api['status']
        apiDict['apiWorkerSize']=api['workers']['type']['weight']
        apiDict['apiNoOfWorkers']=api['workers']['amount']
        apiDict['apiTotalWorkers']= apiDict['apiWorkerSize'] * apiDict['apiNoOfWorkers']
        apiDict['apiBuildFile']=api['fileName']
        apiDetails.append(apiDict)
    
    """ json_object = json.dumps(apiDetails, indent = 4)
    with open(env[key]+"runtimeapi.json", "w") as outfile:
        outfile.write(json_object) """

    data_file = open(key+'_RuntimeApi.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)

    count = 0
    for data in apiDetails:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    data_file.close()
