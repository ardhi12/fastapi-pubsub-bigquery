#create a topic
gcloud pubsub topics create api-log

#create a subscription
gcloud pubsub subscriptions create sub-api-log --topic=api-log

#create a dataset to load the data
bq --location=US mk dataset