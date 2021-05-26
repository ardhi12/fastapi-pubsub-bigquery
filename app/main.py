from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from google.cloud import pubsub_v1
import uvicorn, json
app = FastAPI()

class Log(BaseModel):
	user_activities: List[dict] = []

# configuration Publisher
project_id = "ardhi-data-engineer"
topic_id = "api-log"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

@app.post("/api-log/v1/")
async def log(body: Log):
    # push to pubsub cluster
    dict_user_act = {"user_activities": body.user_activities}
    dict_user_act = json.dumps(dict_user_act)
    print(dict_user_act, type(dict_user_act))    
    future = publisher.publish(topic_path, dict_user_act.encode("utf-8"))    
    return print(future.result())            
    

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8787, debug=True)