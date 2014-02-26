Elasticsearch everything!

Kafka to bring data in,
Then index by elasticsearch

I.e Github:
 1. Python agent:       pull data from GithubAPI
 2. (Scala?) indexer:   read data from FS, push to ES REST API
 -----------
 this could be replaced with Kafka, pulling the data in, pushing out to ES API
 
 3. Elasticserch 1.0:   index (without keeping th Doc in memroy!)
 4. (Py|Scala) Kibana:  explore the index


Github
=====

Sample of JSON repository, one in the raw
```curl https://api.github.com/repositories?since=17200500 | jq -c .[]  | wc -l```
