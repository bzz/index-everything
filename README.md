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




TODO:
-----
 - continue fetching from the last repo in file
 - change interafce to match GNU parallel
 - crete 4 access tockens


Using GNU parallel
--------------
curl -u personal-access-token:x-auth-basic \
 https://api.github.com/repositories?since=17200500

./github-pull-agent.py personal-access-token start end

cat segments.txt | \
 parallel -j+0 --eta './github-pull-agent.py {}'


Segmants.txt
-------------------
# of lines = # parallel jobs
token | [start | end)
  --- |   ---  | ---
personal-access-token1 0 4500000
personal-access-token2 4500000 9000000
personal-access-token3 9000000 13500000
personal-access-token4 13500000 18000000



Commandline 
=====

Sample of JSON repository, one in the raw
```curl -u ....:x-auth-basic https://api.github.com/repositories?since=17200500 | jq -c .[]  | wc -l```

```jq -c .[] raw-github-repos.txt > github-repos.txt```

Index:
```jq -c .id github-repos.txt | xargs curl -XPUT 'http://dooku.nflabs.com:9200/github/repository' -d```


