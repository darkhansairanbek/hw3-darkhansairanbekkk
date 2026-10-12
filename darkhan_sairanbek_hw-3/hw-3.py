
# 1. Imports and settings

import os
import re
import json
import math

from dotenv import load_dotenv
from openai import OpenAI
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import tiktoken

load_dotenv()

client = OpenAI()
LLM_MODEL = "gpt-5.6-luna"
EMBEDDING_MODEL = "google/embeddinggemma-300m"


# PART A1 — BM25 by hand

documents = [
    "Large language models can generate text and answer questions.",
    "Retrieval-Augmented Generation retrieves relevant documents before generating an answer.",
    "Embeddings represent text as numerical vectors."
]

query = "How does RAG retrieve information?"


# 2.1 Tokenize

def tokenize(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()


tokenized_documents = []

for document in documents:
    tokenized_documents.append(tokenize(document))

tokenized_query = tokenize(query)

print("\nPART A1")
print("Query tokens:", tokenized_query)

for i, document in enumerate(tokenized_documents):
    print("D" + str(i + 1), document)


# 2.2 Term frequency

def term_frequency(words):
    frequencies = {}

    for word in words:
        if word not in frequencies:
            frequencies[word] = 0
        frequencies[word] += 1

    return frequencies


for i, document in enumerate(tokenized_documents):
    print("D" + str(i + 1), term_frequency(document))


# 2.3 Document frequency

def document_frequency(word, all_documents):
    count = 0

    for document in all_documents:
        if word in document:
            count += 1

    return count


N = len(tokenized_documents)
document_lengths = [len(document) for document in tokenized_documents]
average_length = sum(document_lengths) / N

print("Document lengths:", document_lengths)
print("Average length:", average_length)

for word in tokenized_query:
    df = document_frequency(word, tokenized_documents)
    idf = math.log((N - df + 0.5) / (df + 0.5))
    print(word, "DF:", df, "IDF:", round(idf, 4))


# 2.4 Calculate BM25

def calculate_bm25(query_words, all_documents, k1=1.5, b=0.75):
    N = len(all_documents)
    lengths = [len(document) for document in all_documents]
    average_length = sum(lengths) / N
    scores = []

    for i, document in enumerate(all_documents):
        score = 0
        frequencies = term_frequency(document)

        for word in query_words:
            tf = frequencies.get(word, 0)

            if tf == 0:
                continue

            df = document_frequency(word, all_documents)
            idf = math.log((N - df + 0.5) / (df + 0.5))

            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (
                1 - b + b * lengths[i] / average_length
            )

            score += idf * numerator / denominator

        scores.append(score)

    return scores


scores = calculate_bm25(tokenized_query, tokenized_documents)

for i, score in enumerate(scores):
    print("D" + str(i + 1), "BM25:", round(score, 4))

print("Ranking:", [
    "D" + str(i + 1)
    for i in sorted(range(len(scores)), key=lambda x: scores[x], reverse=True)
])


# 2.5 BM25 with stemming

stem_map = {
    "retrieve": "retriev",
    "retrieves": "retriev",
    "retrieval": "retriev",
    "generate": "gener",
    "generating": "gener",
    "generation": "gener",
    "information": "inform",
    "does": "doe"
}


def apply_stemming(words):
    result = []

    for word in words:
        result.append(stem_map.get(word, word))

    return result


stemmed_documents = []

for document in tokenized_documents:
    stemmed_documents.append(apply_stemming(document))

stemmed_query = apply_stemming(tokenized_query)

print("Stemmed query:", stemmed_query)

stemmed_scores = calculate_bm25(stemmed_query, stemmed_documents)

for i, score in enumerate(stemmed_scores):
    print("D" + str(i + 1), "BM25 with stemming:", round(score, 4))

print("Ranking with stemming:", [
    "D" + str(i + 1)
    for i in sorted(
        range(len(stemmed_scores)),
        key=lambda x: stemmed_scores[x],
        reverse=True
    )
])


# PART A2 — Cosine similarity

Q = [0.8, 0.2, 0.5]

vectors = {
    "D1": [0.7, 0.1, 0.4],
    "D2": [0.9, 0.3, 0.6],
    "D3": [0.1, 0.8, 0.2]
}


# 3.1 Dot product

def dot_product(vector1, vector2):
    result = 0

    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]

    return result


# 3.2 Vector length

def vector_length(vector):
    total = 0

    for number in vector:
        total += number ** 2

    return math.sqrt(total)


# 3.3 Cosine similarity

def cosine_similarity(vector1, vector2):
    return dot_product(vector1, vector2) / (
        vector_length(vector1) * vector_length(vector2)
    )


print("\nPART A2")

for name, vector in vectors.items():
    print(name)
    print("Dot product:", round(dot_product(Q, vector), 4))
    print("Query length:", round(vector_length(Q), 4))
    print("Document length:", round(vector_length(vector), 4))
    print("Cosine:", round(cosine_similarity(Q, vector), 4))


# PART B1 — Load corpus and BM25

# 4.1 Load JSONL

def load_jsonl(path):
    result = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                result.append(json.loads(line))

    return result


# 4.2 Get value

def get_value(item, names, default=None):
    for name in names:
        if isinstance(item, dict) and name in item:
            if item[name] is not None:
                return item[name]

    return default


corpus = load_jsonl("data/corpus.jsonl")

chunk_ids = []
chunk_titles = []
chunk_texts = []

for i, item in enumerate(corpus):
    chunk_ids.append(str(get_value(
        item, ["id", "chunk_id", "document_id"], i
    )))
    chunk_titles.append(str(get_value(
        item, ["title", "heading", "name"], "No title"
    )))
    chunk_texts.append(str(get_value(
        item, ["text", "content", "chunk", "body"], ""
    )))

print("\nPART B1")
print("Number of chunks:", len(chunk_texts))


# 4.3 Tokenize BM25

def tokenize_bm25(text):
    return re.findall(r"\w+", text.lower())


tokenized_corpus = []

for text in chunk_texts:
    tokenized_corpus.append(tokenize_bm25(text))

bm25_model = BM25Okapi(
    tokenized_corpus,
    k1=1.5,
    b=0.75
)


# 4.4 BM25 search

def bm25_search(query, k=3):
    query_tokens = tokenize_bm25(query)
    scores = bm25_model.get_scores(query_tokens)

    indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    results = []

    for i in indices:
        results.append({
            "index": i,
            "id": chunk_ids[i],
            "title": chunk_titles[i],
            "text": chunk_texts[i],
            "score": float(scores[i])
        })

    return results


# 4.5 Print results

def print_results(results):
    for rank, item in enumerate(results, start=1):
        first_line = item["text"].splitlines()
        first_line = first_line[0] if first_line else ""

        print(
            rank,
            item["id"],
            "Score:", round(item["score"], 4),
            "Title:", item["title"],
            "First line:", first_line
        )


print_results(bm25_search("How does RAG retrieve information?", 3))


# PART B2 — EmbeddingGemma

# 5.1 Embedding search

hf_token = os.getenv("HF_TOKEN")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL,
    token=hf_token
)

document_embeddings = embedding_model.encode_document(
    chunk_texts,
    convert_to_tensor=True,
    show_progress_bar=True
)


def embedding_search(query, k=3):
    query_embedding = embedding_model.encode_query(
        query,
        convert_to_tensor=True
    )

    similarities = embedding_model.similarity(
        query_embedding,
        document_embeddings
    )[0]

    indices = similarities.argsort(
        descending=True
    )[:k].tolist()

    results = []

    for i in indices:
        results.append({
            "index": i,
            "id": chunk_ids[i],
            "title": chunk_titles[i],
            "text": chunk_texts[i],
            "score": float(similarities[i].item())
        })

    return results


print("\nPART B2")
print_results(embedding_search("How does RAG retrieve information?", 3))


# PART B3 — Queries and Hit@3

# 6.1 Load JSON

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_list(data, names):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for name in names:
            if isinstance(data.get(name), list):
                return data[name]

        for value in data.values():
            if isinstance(value, list):
                return value

    raise ValueError("Could not find a list in the JSON file.")


queries_data = load_json("data/queries.json")
queries = get_list(queries_data, ["queries", "items", "data"])


# 6.2 Get query

def get_query_text(item):
    if isinstance(item, str):
        return item

    return str(get_value(
        item, ["query", "question", "text"], ""
    ))


# 6.3 Get relevant IDs

def get_relevant_ids(item):
    relevant = get_value(
        item,
        [
            "relevant", "relevant_ids", "relevant_chunks",
            "relevant_chunk_ids", "expected_ids"
        ],
        []
    )

    if isinstance(relevant, str):
        return [relevant]

    if isinstance(relevant, list):
        result = []

        for value in relevant:
            if isinstance(value, dict):
                value = get_value(value, ["id", "chunk_id"], "")

            if value != "":
                result.append(str(value))

        return result

    return []


own_queries = [
    {
        "query": "Narxoz University",
        "relevant": []
    },
    {
        "query": "What should an applicant do if they disagree with a grant decision?",
        "relevant": []
    }
]

all_queries = queries + own_queries

bm25_hits = []
embedding_hits = []
hit_count = 0

for number, item in enumerate(all_queries, start=1):
    question = get_query_text(item)
    relevant_ids = get_relevant_ids(item)

    print("\nPART B3 — Query", number, ":", question)

    bm25_results = bm25_search(question, 3)
    embedding_results = embedding_search(question, 3)

    print("\nBM25 TOP 3")
    print_results(bm25_results)

    print("\nEMBEDDING TOP 3")
    print_results(embedding_results)

    if relevant_ids:
        bm25_hit = any(
            result["id"] in relevant_ids for result in bm25_results
        )
        embedding_hit = any(
            result["id"] in relevant_ids for result in embedding_results
        )

        bm25_hits.append(int(bm25_hit))
        embedding_hits.append(int(embedding_hit))

        print("BM25 hit@3:", int(bm25_hit))
        print("Embedding hit@3:", int(embedding_hit))
        hit_count += 1
    else:
        print("Hit@3: add the relevant chunk IDs before scoring.")

if hit_count > 0:
    print("BM25 hit@3 average:", sum(bm25_hits) / len(bm25_hits))
    print("Embedding hit@3 average:", sum(embedding_hits) / len(embedding_hits))


# PART C1 — Prompt and token counts

# 7.1 Make context

def make_context(results):
    context = ""

    for number, item in enumerate(results, start=1):
        context += (
            "\n[" + str(number) + "]\n"
            "Chunk ID: " + item["id"] + "\n"
            "Title: " + item["title"] + "\n"
            + item["text"] + "\n"
        )

    return context


# 7.2 Make user message

def make_user_message(question, context=None):
    if context is None:
        return question

    return (
        "Context:\n" + context +
        "\nQuestion:\n" + question
    )


system_message = (
    "Answer the question using only the provided context. "
    "If the answer cannot be found in the context, say that you do not know. "
    "Cite the context blocks you used, like [1] or [2][3]."
)


# 7.3 Ask model

def ask_model(question, context=None):
    user_message = make_user_message(question, context)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )

    answer = response.choices[0].message.content

    return answer, response, user_message


# 7.4 Count tokens

encoding = tiktoken.get_encoding("o200k_base")


def count_tokens(text):
    return len(encoding.encode(text))


# PART C2 — Compare three methods

qa_data_raw = load_json("data/qa.json")
qa_data = get_list(qa_data_raw, ["questions", "qa", "items", "data"])


def get_qa_question(item):
    if isinstance(item, str):
        return item

    return str(get_value(
        item, ["question", "query", "text"], ""
    ))


def get_reference_answer(item):
    if isinstance(item, str):
        return ""

    return str(get_value(
        item,
        ["reference_answer", "reference", "expected_answer", "answer", "ground_truth"],
        ""
    ))


# 8.1 LLM only
# 8.2 BM25 RAG
# 8.3 Embedding RAG

c2_results = []

for number, item in enumerate(qa_data, start=1):
    question = get_qa_question(item)
    reference = get_reference_answer(item)

    print("\nPART C2 — Question", number)
    print("Question:", question)
    print("Reference:", reference)

    llm_answer, llm_response, _ = ask_model(question)

    bm25_results = bm25_search(question, 3)
    bm25_context = make_context(bm25_results)
    bm25_answer, bm25_response, _ = ask_model(question, bm25_context)

    embedding_results = embedding_search(question, 3)
    embedding_context = make_context(embedding_results)
    embedding_answer, embedding_response, _ = ask_model(
        question, embedding_context
    )

    print("\nLLM ONLY:")
    print(llm_answer)

    print("\nBM25 RAG:")
    print("IDs:", [r["id"] for r in bm25_results])
    print(bm25_answer)

    print("\nEMBEDDING RAG:")
    print("IDs:", [r["id"] for r in embedding_results])
    print(embedding_answer)

    c2_results.append({
        "question": question,
        "reference": reference,
        "llm_only": llm_answer,
        "bm25_answer": bm25_answer,
        "embedding_answer": embedding_answer,
        "bm25_chunks": bm25_results,
        "embedding_chunks": embedding_results
    })


# PART C1 — Print complete prompt and token counts

first_question = get_qa_question(qa_data[0])
first_results = embedding_search(first_question, 3)
first_context = make_context(first_results)
first_user_message = make_user_message(first_question, first_context)

print("\nPART C1 — COMPLETE PROMPT")
print("\nSYSTEM:")
print(system_message)
print("\nUSER:")
print(first_user_message)

system_tokens = count_tokens(system_message)
question_tokens = count_tokens(first_question)
context_tokens = count_tokens(first_context)

print("\nSystem tokens:", system_tokens)
print("Question tokens:", question_tokens)
print("Context tokens:", context_tokens)
print("User message tokens:", count_tokens(first_user_message))
print("Approximate total:", system_tokens + count_tokens(first_user_message))
print("Context characters:", len(first_context))
print("Number of chunks:", len(first_results))

for number, item in enumerate(first_results, start=1):
    print(
        "Chunk", number,
        "ID:", item["id"],
        "Characters:", len(item["text"]),
        "Tokens:", count_tokens(item["text"])
    )

first_answer, first_response, _ = ask_model(
    first_question, first_context
)

print("Answer:", first_answer)

if first_response.usage is not None:
    print("API prompt tokens:", first_response.usage.prompt_tokens)


# PART C3 — Top-K experiment and failure analysis

# 9.1 K = 1
# 9.2 K = 3
# 9.3 K = 8

experiment_question = get_qa_question(qa_data[0])

for k in [1, 3, 8]:
    print("\nPART C3 — TOP K =", k)

    results = embedding_search(experiment_question, k)
    context = make_context(results)

    print("Retrieved IDs:", [item["id"] for item in results])

    answer, response, _ = ask_model(experiment_question, context)
    print("Answer:", answer)


# 9.4 Inspect three questions

selected_questions = [1, 3, 6]

for number in selected_questions:
    if number > len(c2_results):
        continue

    item = c2_results[number - 1]

    print("\nPART C3 — ANALYSIS QUESTION", number)
    print("Question:", item["question"])
    print("Reference:", item["reference"])

    print("\nBM25 retrieved chunks:")

    for result in item["bm25_chunks"]:
        print(
            result["id"],
            "Score:", round(result["score"], 4),
            "Title:", result["title"]
        )
        print(result["text"])

    print("\nEmbedding retrieved chunks:")

    for result in item["embedding_chunks"]:
        print(
            result["id"],
            "Score:", round(result["score"], 4),
            "Title:", result["title"]
        )
        print(result["text"])

    print("\nLLM only:", item["llm_only"])
    print("BM25 RAG:", item["bm25_answer"])
    print("Embedding RAG:", item["embedding_answer"])


# 10. End

print("\nEND — HW3 FINISHED")
