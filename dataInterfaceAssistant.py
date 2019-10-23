# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 13:59:20 2019

@author: 60888
"""

import requests
import numpy as np
import json #codecs
from pandas.io.json import json_normalize
import pandas as pd

class dataInterfaceClass:
    #For cloud production run
    endpoint = "http://grundfossmartcity.com:8080/"    
    getExtension = "api/tablestore/data"
    postExtension = "api/tablestore/post"
    
    def sanityCheck(self):
        statusInfoOk = 200
        return statusInfoOk

    def getDataToWorkWith(self, timeRange): 
        request = requests.get(self.endpoint+self.getExtension+"?start="+str(timeRange[0])+"&stop="+str(timeRange[1])) 
        #print(self.endpoint+self.getExtension+"?start="+str(timeRange[0])+"&stop="+str(timeRange[1]))
        #print(request.status_code, request.reason) 
        return request.text, request.status_code, request.reason
        
    def postProcessedDataBack(self, data):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        request = requests.post(self.endpoint+self.postExtension, json=data, headers=headers) # json.dumps(  , headers=headers
        #print(request.status_code, request.reason)
        return request.status_code, request.reason
        
    def jsonToDataframe(self, data, resultAttribute):
        keyList = []
        jsonData = json.loads(data)

        for key in jsonData[0]:
            keyList.append(key)

        dataFrame = pd.DataFrame(columns=keyList)
        for element in range(len(jsonData)):
            newRow = []
            for key in keyList:
                try:
                    newRow.append(float(jsonData[element][key]))
                except ValueError:
                    newRow.append(jsonData[element][key])
            if any("overflow" in stringItem for stringItem in keyList): # Temp hack for missing value
                pass
            else:
                dataFrame['overflow'] = -1.0
                newRow.append(-1.0)
            #print(newRow)
            dataFrame.loc[element,:] = newRow
        #print(dataFrame)
        return dataFrame
        
    def dataframeToJson(self, data):
        # Correct current data types
        data['water_level'] = data['water_level'].astype(str)
        data['flow_rate'] = data['flow_rate'].astype(str)
        data['comm_error'] = data['comm_error'].astype(str)
        data['main_status'] = data['main_status'].astype(str)
        data['warn_code'] = data['warn_code'].astype(str)
        data['pump_fault'] = data['pump_fault'].astype(str)
        data['alarm_code'] = data['alarm_code'].astype(str)
        data['opr_mode'] = data['opr_mode'].astype(str)
        data['pump_mode'] = data['pump_mode'].astype(str)
        data['unix_time'] = data['unix_time'].astype(int)
        data['overflow'] = data['overflow'].astype(float)
        jsonObject = data.to_json(orient='records')[1:-1].replace('},{', '} {')
        return jsonObject