# Stream Processing of Database User Activity
## Use Case
A system can usually capture all database user activity data. However, as data engineers, we cannot retrieve the data from the database directly because it could potentially destabilize the database in the production environment. instead, the backend team sends user activity data via an API. So we will create an API that is ready to receive this data by implementing stream processing
## Tech Stack
* FastAPI : Create API for receive user activity data
* Google Pub/Sub : Data stream
* Google BigQuery : Data Warehouse


