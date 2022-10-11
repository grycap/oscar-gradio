import gradio as gr
import base64
import requests
from minio import Minio
import os
import zipfile
import json 


class gradiooscar:
    def __init__(self, endpoint, user, password,ssl):
        self.endpoint=endpoint
        self.user=user
        self.password=password
        self.ssl=ssl
        x=self.basicRequest("/system/config")
        if x.status_code == 200:
            self.login=True
            response=json.loads(x.text)
            client=response["minio_provider"]
            self.minio = Minio(
                    client["endpoint"].split("//")[1],
                    access_key=client["access_key"],
                    secret_key=client["secret_key"],
                    secure=client["verify"],
                )
        else:
            self.login=False

    def getLogin(self):
        return self.login

    def basicRequest(self,path):
        url=self.endpoint+path
        as_bytes=bytes(self.user+":"+self.password,"utf-8")
        userAndPass = base64.b64encode(as_bytes).decode("utf-8")
        headers = {"Authorization": "Basic "+ userAndPass}
        x = requests.get(url, headers=headers , verify=self.ssl)
        return x


    def get_token(self,servicename):
        x=self.basicRequest("/system/services")
        result=json.loads(x.text)
        for service in result:
            if service["name"] == servicename:
                return service["token"]
        return None 


    def callAsync(self,data,input_bucket,output_bucket,resultfile):
        bucketname=input_bucket.split("/")[0]
        bucketfolder=input_bucket.replace(bucketname+"/","")
        bucketname_output=output_bucket.split("/")[0]
        bucketfolder_output=output_bucket.replace(bucketname+"/","")
        if(os.path.exists(data)):
            self.minio_putfile(bucketname,bucketfolder,data)
        else:
            f = open(resultfile, "w") 
            f.write(data)
            f.close()
            self.minio_putfile(bucketname,bucketfolder,resultfile)
            os.remove(resultfile)
        self.minio_waitAndDownload(bucketname_output,bucketfolder_output,resultfile)

    def callAsyncUuid(self,data,input_bucket,output_bucket,resultfile):
        bucketname=input_bucket.split("/")[0]
        bucketfolder=input_bucket.replace(bucketname+"/","")
        bucketname_output=output_bucket.split("/")[0]
        bucketfolder_output=output_bucket.replace(bucketname+"/","")
        if(os.path.exists(data)):
            self.minio_putfile(bucketname,bucketfolder,data)
        else:
            f = open(resultfile, "w") 
            f.write(data)
            f.close()
            self.minio_putfile(bucketname,bucketfolder,resultfile)
            os.remove(resultfile)
        self.minio_waitAndDownloadUuid(bucketname_output,bucketfolder_output,resultfile)


    def minio_putfile(self,bucketname,bucketfolder,file):
        self.minio.fput_object(
            bucketname, bucketfolder+"/"+file.split("/")[-1], file,
        )

    def minio_waitAndDownload(self,bucketname,bucketfolder,resultfile):
        with self.minio.listen_bucket_notification(
            bucketname,
            prefix=bucketfolder,
            events=["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
        ) as events:
            for event in events:
                info=event
                break
        object=info["Records"][0]["s3"]["object"]["key"]
        self.minio.fget_object(bucketname, object, resultfile)

    def minio_waitAndDownloadUuid(self,bucketname,bucketfolder,resultfile):
        with self.minio.listen_bucket_notification(
            bucketname,
            prefix=bucketfolder,
            events=["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
        ) as events:
            for event in events:
                if(resultfile in event["Records"][0]["s3"]["object"]["key"]):
                    info=event
                    break
        object=info["Records"][0]["s3"]["object"]["key"]
        self.minio.fget_object(bucketname, object, resultfile)
        return  resultfile

        
    def minio_waitAndDownloadSome(self,bucketname,bucketfolder,times,folder):
        index=0
        pathreturn=[]
        with self.minio.listen_bucket_notification(
            bucketname,
            prefix=bucketfolder,
            events=["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
        ) as events:
            for event in events:
                info=event
                index+=1
                object=info["Records"][0]["s3"]["object"]["key"]
                self.minio.fget_object(bucketname, object, folder+object.split("/")[-1])
                pathreturn.append(folder+object.split("/")[-1])
                if(index == times):
                    break
        return pathreturn

    def callSync(self,servicename,data,resultfile=None):
        if(os.path.exists(data)):
            f=open(data,"rb")
            file_bytes=f.read()
            f.close()
            file=base64.b64encode(file_bytes)
        else:
            file=data
        response=self.bearerRequest(servicename,file)
        if (response.status_code == 200):
            result=base64.b64decode(response.text)
            if(resultfile != None):
                f=open(resultfile,"wb")
                f.write(result)
                f.close()
                return resultfile
            else:
                return result
        return response

    def bearerRequest(self,servicename,data):
        token=self.get_token(servicename)
        url=self.endpoint+"/run/"+servicename
        headers = {"Authorization": "Bearer "+str(token)}
        x = requests.post(url, headers=headers, data = data, verify=self.ssl)
        return x


#gro=GradioOSCAR("https://determined-liskov7.im.grycap.net","oscar","oscar2022",True)
#print(gro.get_token("txt-to-img-async"))
#print(gro.callAsync("main.py","a/b/c"))

#image="/media/slangarita/3FD820DA090ABEBD/TFM/Chest X-Ray/COVID19.png"
#Pasando imagen recibiendo txt
#gro.callAsync(image,"chestray/input","chestray/output","resultados.txt")
#input="/media/slangarita/3FD820DA090ABEBD/TFM/Breast Cancer Prediction Dataset/docker/input.json"
"""input2='{"mean_radius": [10.42], \
      "mean_texture": [10.28], \
      "mean_primeter": [186.9], \
      "mean_area": [2501.0],\
     "mean_smoothness": [0.100]} \
'"""
#Pasando fichero recibiendo archivo
#gro.callAsync(input,"bcp/input","bcp/output/grap","resultados1.zip")
#Pasando string recibiendo archivo
#gro.callAsync(input2,"bcp/input","bcp/output/grap","resultados2.zip")
#image2="/media/slangarita/3FD820DA090ABEBD/EGIConference/prueba/plant-classification-sync/input/image3.jpg"

#Pasando imagen recibiendo texto
#plantresult=gro.callSync("plant-classification-sync",image2)
#print(plantresult)
#Pasando texto, recibiendo archivo
#code1=gro.callSync("breast-cancer-prediction-graphic",input,"resultados3.zip")
#print(code1)
#code2=gro.callSync("breast-cancer-prediction-graphic",input2,"resultados4.zip")
#print(code2)
