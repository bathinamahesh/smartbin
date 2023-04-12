from django.shortcuts import render
import json
import time
import base64
import asyncio
import nest_asyncio
nest_asyncio.apply()
from azure.storage.blob import BlobServiceClient
import datetime #for checking today date with last updated data
from datetime import date

# creating the date object of today's date
t_d = date.today()
month=str(t_d.month)
day=str(t_d.day)
#--------------------------------------------------------------BLOB ACCESSING
connect_str = "DefaultEndpointsProtocol=https;AccountName=binboys0storage;AccountKey=eO82ex6Fxz4vFtw6N6ySWz5CG6/92xVMH5K/3t/H70+NTUQeHzelsXrhiCGX4hMhnWndo7SKUyCD+AStUrk5Mg==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container = "binsdata"
containerClient = blob_service_client.get_container_client(container=container)
#final dictionary for last value getting
outData = {}
streetData = {
        "street1":{9398977650:['d1']},
        "street2":{9381767446:['d2']}
        }
    #------------------------------------
#print("\nListing blobs...")
blob_list = containerClient.list_blobs()
def index(request):
    asyncio.run(readBlobs())
    data=outData
    d1phn=0
    d2phn=0
    try:
        d1percent=list(data['d1'].values())[0]
    except:
        d1percent=0
    try:
        d2percent=list(data['d2'].values())[0]
    except:
        d2percent=0
    ##
    try:
        d1phn=(list(data['d1'].values())[1])
    except:
        d1phn="default"
    try:
        d2phn=(list(data['d2'].values())[1])
    except:
        d2phn="default"
    d3phn="180539"
    ##
    d1=0
    if(int(d1percent)>80):
        d1=4
    elif(int(d1percent)>50):
        d1=3
    elif(int(d1percent)>25):
        d1=2
    else:
        d1=1
    d2=0
    if(int(d2percent)>80):
        d2=4
    elif(int(d2percent)>50):
        d2=3
    elif(int(d2percent)>25):
        d2=2
    else:
        d2=1
    #sprint(d1,"   ",d2)
    return render(request,'index.html',context={"data1":d1,"data2":d2,"data3":4,"percent1":d1percent,"percent2":d2percent,"percent3":95,"datet":str(date.today()),"d1phn":d1phn,"d2phn":d2phn,"d3phn":d3phn})
    #------------------------------------
async def read(deviceId,fill_percent,date):
        for i,j in streetData.items():
            for k,l in j.items():
                if deviceId in l:
                    phno = k
        #print(phno)
        outData[deviceId] = {date:fill_percent,"contact":phno}
        
        ''' only if>80%
        if(fill_percent>80):
            #print(deviceId," = Fill percent: ",fill_percent,"%")
            outData[deviceId] = {date:fill_percent,"contact":phno}
            #print(outData)
        '''
        return
    #-----------------------------------
async def readBlobs():
    blob_list = containerClient.list_blobs()
    for blob in blob_list:
        #-----------------------
        arr = blob.name.split("/")
        #print(int(arr[3]),int(month),int(arr[4]),int(day))
        if(int(arr[3])==int(month) and int(arr[4])==int(day)):
            #print("Mahesh")
            date = arr[4] #date index in blob path name (seen from documentation)
            #-----------------------
            data = str(containerClient.download_blob(blob.name).readall(),'utf-8')
            i = data.strip().split("\n")
            for j in i:
                j = json.loads(j)
                #print(j['deviceId']," = Fill percent: ",j['telemetry']['fill_percent'],"%")
                asyncio.run(read(j['deviceId'],j['telemetry']['fill_percent'],date))

