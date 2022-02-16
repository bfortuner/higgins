"""
This script contains an example how to perform semantic search with ElasticSearch.

As dataset, we use the Quora Duplicate Questions dataset, which contains about 500k questions:
https://www.quora.com/q/quoradata/First-Quora-Dataset-Release-Question-Pairs

Questions are indexed to ElasticSearch together with their respective sentence
embeddings.

The script shows results from BM25 as well as from semantic search with
cosine similarity.

You need ElasticSearch (https://www.elastic.co/de/elasticsearch/) up and running. Further, you need the Python
ElasticSearch Client installed: https://elasticsearch-py.readthedocs.io/en/master/

As embeddings model, we use the SBERT model 'quora-distilbert-multilingual',
that it aligned for 100 languages. I.e., you can type in a question in various languages and it will
return the closest questions in the corpus (questions in the corpus are mainly in English).
"""

import csv
import os
from typing import Dict, List

from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer, util
import time
import tqdm.autonotebook

from higgins.database import elastic
from higgins.automation.email import email_utils
from higgins.nlp import nlp_utils

es = Elasticsearch()

tokenizer = nlp_utils.get_tokenizer()


def create_vector_index(
    index: str, text_field: str, vector_field: str, vector_dims: int
):
    if not es.indices.exists(index=index):
        es_index = {
            "mappings": {
                "properties": {
                    text_field: {"type": "text"},
                    vector_field: {"type": "dense_vector", "dims": vector_dims},
                }
            }
        }
        es.indices.create(index=index, body=es_index, ignore=[400])
    else:
        print(f"Index {index} already exists!")


def create_and_upload_embeddings(
    model: SentenceTransformer,
    rows: List[Dict],
    index: str,
    text_field: str,
    vector_field: str,
    chunk_size: int = 500,
):
    print("inside create and upload")
    with tqdm.tqdm(total=len(rows)) as pbar:
        for start_idx in range(0, len(rows), chunk_size):
            row_slice = rows[start_idx : start_idx + chunk_size]
            # print(
            #     "num tokens before encoding",
            #     nlp_utils.get_num_tokens(row_slice[0][text_field], tokenizer),
            # )
            embeddings = model.encode(
                sentences=[row[text_field] for row in row_slice],
                show_progress_bar=False,
            )
            bulk_data = []
            for row, embedding in zip(row_slice, embeddings):
                row[vector_field] = embedding
                row_id = row["_id"]
                del row["_id"]
                document = {
                    "_index": index,
                    "_id": row_id,
                    "_source": row,
                }
                bulk_data.append(document)

            helpers.bulk(es, bulk_data)
            pbar.update(chunk_size)


def init_query_session(
    model,
    index,
    text_field,
    vector_field,
    max_results: int = 20,
    display_field: str = None,
):
    """Open interactive query session"""
    while True:
        inp_question = input("Please enter a question: ")

        encode_start_time = time.time()
        question_embedding = model.encode(inp_question)
        encode_end_time = time.time()

        # Lexical search
        bm25 = es.search(
            index=index,
            body={
                "size": max_results,
                "query": {"match": {f"{text_field}": inp_question}},
            },
        )
        print(f"bm25 Hits: {bm25['hits']['total']}")

        # Sematic search
        # Example of searching multiple dense fields
        # "source": "cosineSimilarity(params.queryVector, doc['Text_Vector1']) + cosineSimilarity(params.queryVector, doc['Text_Vector2'])  + 2.0",
        sem_search = es.search(
            index=index,
            body={
                "size": max_results,
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": f"cosineSimilarity(params.queryVector, doc['{vector_field}']) + 1.0",
                            "params": {"queryVector": question_embedding},
                        },
                    }
                },
            },
        )
        print(f"Sem Hits: {sem_search['hits']['total']}")

        print("Input question:", inp_question)
        print(
            "Computing the embedding took {:.3f} seconds, BM25 search took {:.3f} seconds, semantic search with ES took {:.3f} seconds".format(
                encode_end_time - encode_start_time,
                bm25["took"] / 1000,
                sem_search["took"] / 1000,
            )
        )
        display_field = display_field if display_field is not None else text_field
        print("BM25 results:")
        for hit in bm25["hits"]["hits"]:
            print("\t{} - {}".format(hit["_score"], hit["_source"][display_field]))

        print("\nSemantic Search results:")
        for hit in sem_search["hits"]["hits"]:
            print("\t{} - {}".format(hit["_score"], hit["_source"][display_field]))

        print("\n\n========\n")


def prepare_quora_dataset(max_corpus_size: int = 100000):
    url = "http://qim.fs.quoracdn.net/quora_duplicate_questions.tsv"
    dataset_path = "quora_duplicate_questions.tsv"

    # Download dataset if needed
    if not os.path.exists(dataset_path):
        print("Download dataset")
        util.http_get(url, dataset_path)

    # Get all unique sentences from the file
    all_questions = {}
    with open(dataset_path, encoding="utf8") as fIn:
        reader = csv.DictReader(fIn, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            all_questions[row["qid1"]] = row["question1"]
            if len(all_questions) >= max_corpus_size:
                break

            all_questions[row["qid2"]] = row["question2"]
            if len(all_questions) >= max_corpus_size:
                break

    qids = list(all_questions.keys())
    questions = [
        {
            "_id": qid,
            "question": all_questions[qid],
        }
        for qid in qids
    ]
    return questions


def create_quora_embeddings_index(model):
    vector_dims = model.get_sentence_embedding_dimension()
    index = "quora"
    text_field = "question"
    vector_field = text_field + "_vector"
    corpus_size = 100000
    questions = prepare_quora_dataset(corpus_size)
    create_vector_index(index, text_field, vector_field, vector_dims)
    create_and_upload_embeddings(model, questions, index, text_field, vector_field)


def prepare_email_dataset(corpus_size):
    hits = elastic.get_all(client=es, index="email", start=0, stop=corpus_size)
    email_dicts = []
    for hit in hits:
        dct = hit.to_dict()
        document = email_utils.get_email_body_extended(dct)
        # print("num tokens before", nlp_utils.get_num_tokens(document, tokenizer))
        document = email_utils.remove_whitespace(document)
        # print("num tokens after", nlp_utils.get_num_tokens(document, tokenizer))
        document = nlp_utils.trim_tokens(document, 4000, tokenizer)
        dct["body_extended"] = document
        dct["_id"] = hit.meta.id
        email_dicts.append(dct)
    return email_dicts


def create_email_subject_embeddings_index(model, vector_dims):
    vector_dims = model.get_sentence_embedding_dimension()
    index = "email_subject_embed"
    text_field = "subject"
    vector_field = text_field + "_vector"
    emails = prepare_email_dataset(corpus_size=10000)
    create_vector_index(index, text_field, vector_field, vector_dims)
    create_and_upload_embeddings(model, emails, index, text_field, vector_field)


def create_email_body_embeddings_index(model):
    vector_dims = model.get_sentence_embedding_dimension()
    index = "email_body_embed"
    text_field = "body_extended"
    vector_field = text_field + "_vector"
    emails = prepare_email_dataset(corpus_size=10000)
    create_vector_index(index, text_field, vector_field, vector_dims)
    create_and_upload_embeddings(
        model, emails, index, text_field, vector_field, chunk_size=5
    )


if __name__ == "__main__":
    # Email body embedding (errors out, likely documents that are too large)
    engine = "allenai/longformer-base-4096"
    # model = SentenceTransformer(engine)
    # create_email_body_embeddings_index(model)
    # init_query_session(
    #     model,
    #     index="email_body_embed",
    #     text_field="body_extended",
    #     vector_field="body_extended_vector",
    #     display_field="subject",
    #     max_results=20,
    # )

    # Email subject embedding
    engine = "msmarco-distilbert-base-v4"
    model = SentenceTransformer(engine)
    # create_email_subject_embeddings_index(model)
    init_query_session(
        model,
        index="email_subject_embed",
        text_field="subject",
        vector_field="subject_vector",
        max_results=30,
    )

    sentences = [
        "TI Briefing: Instacart’s Facebook Hiring Program",
        "Hitched onto the acquisition wagon",
        "are you ready for job hunt season?",
        "Startup Spotlight #151: Jestor",
        "TI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting Advantage TI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting Advantage TI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting AdvantageTI Crypto Global: Robinhood's Dogecoin Problem; Crypto’s Recruiting Advantage",
    ]
    embeddings = model.encode(sentences)
    print(embeddings[-1].shape)

    # create_quora_embeddings_index(model)

    # init_query_session(
    #     model, index="quora", text_field="question", vector_field="question_vector"
    # )

    # emails = prepare_email_dataset(corpus_size=10)
    # print(emails[0])
