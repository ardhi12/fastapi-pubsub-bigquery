from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from google.cloud import pubsub_v1
import uvicorn
import json
import os

app = FastAPI()

class Log(BaseModel):
	user_activities: List[dict] = []

# configuration Publisher
project_id = "ardhi-data-engineer"
topic_id = "api-log"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "yourKey.json"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

@app.post("/api-log/v1/")
async def log(body: Log):
    # push to pubsub cluster
    dict_user_act = {"user_activities": body.user_activities}
    dict_user_act = json.dumps(dict_user_act)        
    try:
        publisher.publish(topic_path, dict_user_act.encode("utf-8"))
        response_value={
            "error" : False,
            "message" : "Data has been received and published to the pubsub topic"            
            }
        status_code=200
    except Exception as e :
        print(e)
        response_value={
            "error" : True,
            "message" : str(e)
            }
        status_code=400
    return JSONResponse(
        status_code=status_code,
        content=response_value)        

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8787, debug=True)