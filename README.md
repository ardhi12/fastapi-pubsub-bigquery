# Stream Processing of Database User Activity
## Use Case
A system can usually capture all database user activity data. However, as data engineers, we cannot retrieve the data from the database directly because it could potentially destabilize the database in the production environment. instead, the backend team sends user activity data via an API. So we will create an API that is ready to receive this data by implementing stream processing

## Flow
![alt text](https://github.com/ardhi12/fastapi-pubsub-bigquery/blob/master/img/flow.jpeg?raw=true)

## Tech Stack
* FastAPI : Create API for receive user activity data
* Google Pub/Sub : Data stream
* Google BigQuery : Data Warehouse

## Prerequisite
* Make sure you have python 3.6 or above installed on your machine
* Enabled Cloud Pub/Sub API [[Read docs](https://cloud.google.com/pubsub/docs/quickstart-console)]
* Create service account as an owner, download key with JSON format and put the key in `app` folder [[Read docs](https://cloud.google.com/iam/docs/creating-managing-service-accounts)]
* Activate Cloud SDK on your local device [[Read docs](https://cloud.google.com/sdk/docs/quickstart)]
* Install postman to your browser [[Read docs](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=id)]
* Clone this repository
`git clone https://github.com/ardhi12/fastapi-pubsub-bigquery.git`
* Install the prerequisite library from requirements.txt 
`pip3 install -r requirements.txt`

## Run
* Run `bash pubsub.sh` to create pubsub topic, subscription, and create BigQuery dataset
* Run `python3 main.py` to start API service
* Run `python3 subscriber.py` to start stream process
* Make a POST request with an endpoint `http://127.0.0.1:8787/api-log/v1/`
example raw body request (JSON format):
```
{"user_activities": [
    {
      "operation": "insert",
      "table": "user_activities_table",
      "col_names": ["user_id", "event_type_id", "detail", "occured_at"],
      "col_types": ["integer", "integer", "string", "datetime"],
      "col_values": [1, 2, "logged in", "2021-03-30 06:12:44"] 
    },
    {
      "operation": "insert",
      "table": "user_activities_table",
      "col_names": ["user_id", "event_type_id", "detail", "occured_at"],
      "col_types": ["integer", "integer", "string", "datetime"],
      "col_values": [2, 5, "Delete item with id 7", "2021-05-24 10:15:04"] 
    }]
}
```

## Notes
* Key operation, table, col_names, col_types, col_values is a must
* Col_types which is allowed are: string, bytes, integer, float, numeric, bignumeric, boolean, timestamp, date, time, datetime, geography, record
* Operation which is allowed are insert and delete
* Delete operations can be used after waiting up to 90 minutes [[Read issue](https://stackoverflow.com/questions/43085896/update-or-delete-tables-with-streaming-buffer-in-bigquery)]