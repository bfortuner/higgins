from typing import Dict, List, Tuple

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import elasticsearch_dsl
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
import pandas as pd
from txtai.embeddings import Embeddings
from txtai.pipeline.extractor import Extractor
from txtai.pipeline import Similarity

from higgins.nlp.openai.email_questions import rank_strings
from . import email_utils


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


def get_all(query: Dict):
    client = Elasticsearch()
    s = Search(using=client, index="email")
    resp = s.execute()
    print(f"Hits: {resp.hits.total.value}")


def get_by_id(id_: str, client: Elasticsearch):
    resp = client.get(index=EMAIL_INDEX, id=id_)
    print(type(resp))
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


def search_subjects(query: str, client: Elasticsearch, limit: int = QUERY_LIMIT):
    query = {"size": limit, "query": {"query_string": {"query": query}}}

    results = []
    for result in client.search(index=EMAIL_INDEX, body=query)["hits"]["hits"]:
        source = result["_source"]
        results.append((min(result["_score"], 18) / 18, source["subject"]))

    return results


def dict_to_table(dct, columns=None):
    df = pd.DataFrame(data=dct, columns=columns)
    return df


def semantic_search(query: str, strings: List[str], engine: Similarity):
    # https://github.com/neuml/txtai/blob/master/examples/04_Add_semantic_search_to_Elasticsearch.ipynb
    return [(score, strings[x]) for x, score in engine(query, strings)]


def test_semantic_search(es):
    # query = "+Slack"
    # results = search_subjects(query, client=es, limit=10)
    # print(results)
    # engine = "typeform/distilbert-base-uncased-mnli"  # best?
    engine = "valhalla/distilbart-mnli-12-3"  # tutorial
    # engine = "facebook/bart-large-mnli"
    # engine = "vicgalle/xlm-roberta-large-xnli-anli"  # slow, can't use the fast tokenizer
    similarity = Similarity(engine)

    # email = get_by_id(id_=df.iloc[0]["_id"], client=es)
    # print(email)
    query_field = "subject"
    secondary_fields = ["plain"]
    # queries = ["+job opportunity"]  # + means include/contains? - means exclude
    queries = [
        "+recruiter email"
    ]  # Elasticsearch doesn't understand, but txtai does well
    # queries = [
    #     "+when does my flight arrive?"   # Davinci handles this well
    # ]  # + means include/contains? - means exclude
    for query in queries:
        hits = search_query_string(
            query, fields=[query_field] + secondary_fields, client=es
        )
        print(f"Found {len(hits)} results.")
        results = [dsl_hit_to_dict(hit) for hit in hits]
        df = results_to_df(results, fields=["subject", "sender_address", "date"])
        with pd.option_context("display.max_colwidth", -1):
            print(df.head(20))
        # Create similarity instance for re-ranking
        rankings = []
        for i in range(0, len(results), SIMILARITY_BATCH_SIZE):
            strings = [
                r["_source"][query_field]
                for r in results[i : i + SIMILARITY_BATCH_SIZE]
            ]
            rankings += semantic_search(query, strings, similarity)
            print(f"Processed {len(rankings)} rows")
        df = pd.DataFrame(data=rankings, columns=["score", query_field])
        df = df.sort_values(by="score", ascending=False, inplace=False)
        # with pd.option_context("display.max_colwidth", -1):
        print(df.head(20))

        # OpenAI - Davinci == Way better
        strings = [r["_source"][query_field] for r in results[:200]]
        docs = rank_strings(query, strings)
        for doc in docs[:20]:
            print(doc["score"], strings[doc["document"]])


def extractive_qa(
    email: Dict, questions: List[Tuple], embeddings: Embeddings, extractor: Extractor
):
    # questions: [ (Name, query, question, is_snippet), ... ]
    # They preprocess their articles to extract and label sentences
    # as "informative" or not. Only the salient sentences are fed to model.
    # https://github.com/UKPLab/sentence-transformers
    # https://github.com/neuml/txtai/blob/master/examples/06_Extractive_QA_with_Elasticsearch.ipynb

    # Use QA extractor to derive additional columns
    from higgins.nlp.openai import email_questions

    chunks = email_questions.create_email_chunks(email["plain"], 200)
    answers = extractor(questions, chunks)
    return answers, chunks


def test_extractive_qa_verification_codes():
    # Create embeddings model, backed by sentence-transformers & transformers
    embeddings = Embeddings({"path": "sentence-transformers/nli-mpnet-base-v2"})
    # https://huggingface.co/deepset/roberta-large-squad2
    extractor = Extractor(embeddings, "deepset/roberta-large-squad2")
    # extractor = Extractor(
    #     embeddings, "deepset/bert-large-uncased-whole-word-masking-squad2"
    # )
    questions = [
        ("Sender", "from", "Who is the email from?", False),
        ("Code", "verification code", "What is the code?", False),
        (
            "Verification Code",
            "verification code",
            "What is the verification code?",
            False,
        ),
        ("Expires", "code expires", "When does the code expire?", False),
    ]
    emails = email_utils.search_local_emails(["verification_code"])
    print(f"Found {len(emails)}")
    for email in emails:
        preview = email_utils.get_email_preview(email, show_body=True)
        email["plain"] = preview
        answers, chunks = extractive_qa(email, questions, embeddings, extractor)
        print("--->   ", answers)


def test_extractive_qa_flights():
    # Create embeddings model, backed by sentence-transformers & transformers
    embeddings = Embeddings({"path": "sentence-transformers/nli-mpnet-base-v2"})
    # https://huggingface.co/deepset/roberta-large-squad2
    extractor = Extractor(embeddings, "deepset/roberta-large-squad2")
    questions = [
        ("Traveler", "traveler passenger name", "Who is the traveler?", False),
        (
            "Confirmation number",
            "confirmation number",
            "What is the confirmation number?",
            False,
        ),
        (
            "Airline",
            "airline",
            "What is the airline?",
            False,
        ),
        (
            "Departure time",
            "departure time departs",
            "When does the flight depart?",
            False,
        ),
        (
            "Arrival time",
            "arrival time arrives",
            "When does the flight arrive?",
            False,
        ),
    ]
    emails = email_utils.search_local_emails(["flights"])
    print(f"Found {len(emails)}")
    for email in emails:
        preview = email_utils.get_email_preview(email, show_body=True)
        email["plain"] = preview
        answers, chunks = extractive_qa(email, questions, embeddings, extractor)
        print("--->   ", answers)
        print(email.get("model_labels"))


def elasticsearch_dense_vectors():
    # https://www.sbert.net/examples/applications/semantic-search/README.html
    # https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/semantic-search/semantic_search_quora_elasticsearch.py
    pass


if __name__ == "__main__":
    # search_elastic_emails({})
    # es = Elasticsearch(
    #     hosts=["http://localhost:9200"], timeout=60, retry_on_timeout=True
    # )
    # test_semantic_search(es)
    # test_extractive_qa_verification_codes()
    # test_extractive_qa_flights()
    # emails = email_utils.search_local_emails(["flights"])
    # print(email_utils.get_email_list_preview(emails))

    # for email in emails[:3]:
    #     print(email_utils.get_email_preview(email))

    from higgins.nlp import html_utils

    #     email = emails[0]

    # email = email_utils.load_email(
    #     "cfefa0094fe59fb957197da94d4681e0070c74f8313e8f45637a61c5ba2bc83e"  # "e2230f4e0ac8396781c9f1002c3e759850d57d21c664a919e0d8d994eebfb993"
    # )
    # print(email_utils.get_email_preview(email))
    # from bs4 import BeautifulSoup

    # # print(email["email_id"])
    # # soup = BeautifulSoup(email["html"])
    # # for child in soup.find_all("table"):
    # #     print(child)

    # # for child in soup.find_all("table")[4].children:
    # #     for td in child:
    # #         print(td.text)

    # # tables = html_utils.extract_tables_from_html(email["html"])
    # # print(tables)

    # # tables = html_utils.extract_tables_from_html_pandas(email["html"])
    # plain = email_utils.parse_html_v3(email["html"])
    # print(plain)

    # # tables = soup.find_all("table")
    # # import pdb

    # # pdb.set_trace()

    # test_extractive_qa_verification_codes()
    test_extractive_qa_flights()
