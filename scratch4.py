#Embeddings
from sentence_transformers import SentenceTransformer,util
import numpy as np
import json
import chromadb



model = SentenceTransformer("all-MiniLM-L6-v2")
with open("phase2_topics.json", "r", encoding="utf-8") as file:
    phase2= json.load(file)


# embeddings = model.encode(phase2)


def prepare(phase2):
    ids = []
    metadatas = []
    documents = []

    for topic_key, topic_data in phase2.items():
        placement = topic_data["placement"]
        content = topic_data["text"]
        page_number = topic_data["page"]
        related_content = topic_data.get("related_content", {})

        document_text = f"""Title: {topic_key} , Placement: {placement} , Page number: {page_number}, Content:{content} , Related content:{related_content}"""
        record_id = f"{topic_key}".replace(" ", "_")
        metadata = {"topic_key": topic_key,"placement": placement,"page": page_number}

        ids.append(record_id)
        documents.append(document_text)
        metadatas.append(metadata)

    return ids, documents, metadatas
ids,document,metadatas= prepare(phase2)  
embeddings = model.encode(document)

# print("Total documents:", len(document))
# print("Embeddings shape:", embeddings.shape)
# similar=util.pytorch_cos_sim(embeddings[56],embeddings[100])
# print(similar)
query=input("enter your query:")
query_embedding=model.encode(query)
# query=input("enter your query:")
# query_embedding=model.encode(query)

similar=util.pytorch_cos_sim(query_embedding,embeddings)
# print(similar)
import chromadb


def store_in_chromadb(ids, documents, metadatas, embeddings):
    client = chromadb.PersistentClient(path="chroma_storage")

    collection = client.get_or_create_collection(name="book_content")

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist()
    )

    print("Data stored in ChromaDB successfully.")
store_in_chromadb(ids, document, metadatas, embeddings)   



