
# Show indices
curl -X GET 'http://localhost:9200/_cat/indices?pretty'

# Show schemas (mappings)
curl -X GET 'http://localhost:9200/gmail/_mapping?pretty'
# curl -X GET 'http://localhost:9200/articles/_mapping?pretty'

# Delete index
# curl -X DELETE 'http://localhost:9200/gmail'

# Search index
# https://www.elastic.co/guide/en/elasticsearch/reference/7.14//search-your-data.html
curl -X GET 'http://localhost:9200/gmail/email/_search?pretty' -H 'Content-Type: application/json' -d '
{
    "query": {
        "bool": {
            "filter": [{
                "range" : {
                    "date_ts" : { 
                        "gte": "1226501681000" 
                    }
                }
            }]
        }
    }
}'

# Show first 5 rows
# Paginate option: https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#search-after
curl -X GET 'http://localhost:9200/email/_search?pretty&size=5' -H 'Content-Type: application/json' -d '
{
    "query" : {
        "match_all" : {}
    }
}'

# # Count
# curl -XGET 'http://localhost:9200/gmail/_count?pretty' -H 'Content-Type: application/json' -d '
# {
#   "query": {
#     "term": {
#       "from": {
#         "value": "bda@mnsspb.ru",
#         "boost": 1.0
#       }
#     }
#   }
# }'

# # Aggregate count of emails over each unique 'from' address
# curl -XGET 'http://localhost:9200/gmail/_search?pretty' -H 'Content-Type: application/json' -d '
# {
#   "aggs": {
#     "my-agg-name": {
#       "terms": {
#         "field": "from.keyword"
#       }
#     }
#   }
# }'

# # Return `count of docs containing field 'from'
# # https://opendistro.github.io/for-elasticsearch-docs/docs/elasticsearch/aggregations/
# # If you’re only interested in the aggregation result and not in the results of the query, set size to 0.
# # curl -X POST "http://localhost:9200/gmail/_search?size=0&pretty" -H 'Content-Type: application/json' -d'
# # {
# #     "aggs" : {
# #         "types_count" : { "value_count" : { "field" : "from.keyword" } }
# #     }
# # }'

