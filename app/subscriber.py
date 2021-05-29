from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import os
import json
from google.cloud import bigquery

# configuration Publisher
project_id = "ardhi-data-engineer"
sub_id = "sub-api-log"
dataset_id = "dataset"

timeout = 30
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "yourKey.json"

sub = pubsub_v1.SubscriberClient()

subscription_path = sub.subscription_path(project_id, sub_id)

messages = []

def callback(message):
    raw_msg = message.data
    decode_msg = raw_msg.decode("utf-8")
    json_msg = json.loads(decode_msg)
    print(f"Received {json_msg}.")    
    message.ack()
    #str_data = str(message.data).replace("\\n", "").replace("\\t", "").replace("\\","").replace("b\'b\'", "").replace("'", "") 
    #json_data = json.loads(str_data)
    #print(json_data)
    user_activities = [obj for obj in json_msg['user_activities']]
    
    client = bigquery.Client()
    for activity in user_activities:
        table_id = activity['table']
        table_id1 = f'{project_id}.{dataset_id}.{table_id}'
        operation = activity['operation']
        col_names = activity['col_names']        
        col_types = activity['col_types']
        col_values = activity['col_values']        

        #something to do on insert operation here
        if operation == "insert":
            #check bq dataset, if table not exist, we need to create table and define schema
            tables = [tables.table_id for tables in client.list_tables(dataset_id)]
            if table_id not in tables:
                #create schema for new table
                schema = []
                for col_idx in range(len(col_names)):
                    field = bigquery.SchemaField(col_names[col_idx], col_types[col_idx])
                    schema.append(field)
                    
                table = bigquery.Table(table_id1, schema=schema)
                table = client.create_table(table) #make an API request.
            
            #we're done to create table. 
            add = ', '.join([f'ADD COLUMN IF NOT EXISTS {col[0]} {col[1] if col[1] != "integer" else "numeric"}' for col in zip(col_names, col_types)])
            sql = f'ALTER TABLE {table_id1} {add}'    
            client.query(sql)

            #insert data to the table. 
            rows_to_insert = {}
            for idx in range(len(col_names)):
                rows_to_insert[col_names[idx]] = col_values[idx]
            
            client.insert_rows_json(table_id1, [rows_to_insert])

        elif operation == "delete":
            row_to_delete = []
            #create query statement
            for idx in range(len(col_names)):
                row_to_delete.append(f"""{col_names[idx]} = {col_values[idx] if col_types[idx] == 'integer' else f"'{col_values[idx]}'"}""")
            sql = f"DELETE {table_id1} WHERE {' and '.join(row_to_delete)}"
            print(sql) 
            client.query(sql)

streaming_pull_future = sub.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with sub:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()