"""Elasticsearch database utils.

References
-----------
https://www.elastic.co/guide/en/elasticsearch/reference/7.14/index.html
https://opendistro.github.io/for-elasticsearch-docs/docs/elasticsearch/aggregations/
https://github.com/oliver006/elasticsearch-gmail

Query DSL:
https://github.com/elastic/elasticsearch-dsl-py

Text analysis and full-text search
https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html

"""
import sys
from typing import Dict, List

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import elasticsearch_dsl
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
import pandas as pd


EMAIL_INDEX = "email"
QUERY_LIMIT = 1000
SIMILARITY_BATCH_SIZE = 10


def bulk_load_docs():
    # Connect to ES instance
    es = Elasticsearch(
        hosts=["http://localhost:9200"], timeout=60, retry_on_timeout=True
    )

    dataset = []
    # Elasticsearch bulk buffer
    buffer = []
    rows = 0

    for x, text in enumerate(dataset):
        # Article record
        article = {"_id": x, "_index": "articles", "title": text}

        # Buffer article
        buffer.append(article)

        # Increment number of articles processed
        rows += 1

        # Bulk load every 1000 records
        if rows % 1000 == 0:
            helpers.bulk(es, buffer)
            buffer = []

            print("Inserted {} articles".format(rows), end="\r")

    if buffer:
        helpers.bulk(es, buffer)


def get_all(client, index, start: int = 0, stop: int = sys.maxsize):
    s = Search(using=client, index=index)
    s = s[start:stop]
    resp = s.execute()
    print(f"Hits: {resp.hits.total.value}")
    return resp


def get_by_id(id_: str, client: Elasticsearch):
    resp = client.get(index=EMAIL_INDEX, id=id_)
    return resp


def search_query_string(
    query_str: str,
    fields: List,
    client: Elasticsearch,
    start: int = 0,
    stop: int = QUERY_LIMIT,
) -> List[elasticsearch_dsl.response.hit.Hit]:
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html
    # https://www.elastic.co/guide/en/elasticsearch//reference/current/query-dsl-multi-match-query.html
    query = MultiMatch(query=query_str, fields=fields, type="best_fields")
    s = Search(using=client, index=EMAIL_INDEX)
    s = s.query(query)
    s = s[start:stop]  # pagination/limit
    hits = s.execute()
    return hits


def dsl_hit_to_dict(hit: List[elasticsearch_dsl.response.hit.Hit]) -> Dict:
    """Convert Elasticsearc-DSL Hit objects to normal ES result dicts."""
    return {
        "_id": hit.meta.id,
        "_index": hit.meta.index,
        "_type": "_doc",  # not sure if this exists
        "_score": hit.meta.score,
        "_source": hit.to_dict(),
    }


def results_to_df(results: List[Dict], fields: List[str] = None):
    rows = []
    for result in results:
        doc = {
            "_id": result["_id"],
            "_score": min(result["_score"], 18) / 18,
        }
        doc.update(
            {
                k: v
                for k, v in result["_source"].items()
                if fields is None or k in fields
            }
        )
        rows.append(doc)
    df = pd.DataFrame(rows)
    return df


def example_search():
    client = Elasticsearch()
    response = client.search(
        index="gmail",
        body={
            "query": {
                "bool": {
                    "must": [{"match": {"title": "python"}}],
                    "must_not": [{"match": {"description": "beta"}}],
                    "filter": [{"term": {"category": "search"}}],
                }
            },
            "aggs": {
                "per_tag": {
                    "terms": {"field": "tags"},
                    "aggs": {"max_lines": {"max": {"field": "lines"}}},
                }
            },
        },
    )

    for hit in response["hits"]["hits"]:
        print(hit["_score"], hit["_source"]["title"])

    for tag in response["aggregations"]["per_tag"]["buckets"]:
        print(tag["key"], tag["max_lines"]["value"])
