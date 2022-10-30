from fastapi import FastAPI
from app.feat_eng import get_json_data
import requests

app = FastAPI()

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
#        Endpoint : Feature Engineering       #
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

@app.get('/features')
def get_features():
    return get_json_data()


#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
#        Endpoint : API_STATUS      #
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

@app.get('/api_status')
def get_status():

    url = "http://0.0.0.0:8000/features"
    status = requests.get(url= url).status_code

    if status == 200:
        return {"status": "UP"}

