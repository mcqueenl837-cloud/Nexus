#Groq api calling
# import chromadb
# from groq import Groq
# import os
# KEY="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"
# groq_client=Groq(api_key=os.environ.get("KEY"))
# groq_model="llama-3.1-8b-instant"

# client=chromadb.PersistentClient(path="chroma_storage")
# collection=client.get_collection("book_content")
# def build_prompt(question):
#     query_embedding=groq_model.encode(question).tolist()#converts question into embeddings
#     collection=client.get_collection("book_content")
#     results=collection.query(query_embeddings=[query_embedding],n_results=3,include=["metadatas","documents"])
#     documents=results["documents"][0]
#     context="\n\n".join(documents)
#     prompt=f""" Hello Groq, you are a set of teachers, Whose subject depends on the content given to you.
#     You have to give response like you are teaching a college student. Types of questions you could expect from the user:
#     1) Relation betweeen certain topics, equations or figure or it could be in the form of relation of certain topic with ceratin equations or figures.
#     2) Explanation of Topics/Titles, Equations or figures could also be asked.
#     3) Closest candidates of content related to certain topics/titles, equations or figures. You have to give explain their relation.
#     Most Important instruction:
#     - You have to explain by content provided to you. It is usually going to be a set of Three lists.
#     The three lists are going to be closest content related to what have asked .
#     Information about question asked={results},
#     Context={context},
#     Question asked by user={question}
#     You have to give answer in the format of:
#     -Question asked by user
#     -your findings based upon Context given to you.
#     -Information about question asked (provide this at last)
#     You have to give answer in range of 100-200 words only. Give more information by expanding the word range
#     if you think this is not sufficient information for question asked. 
#     You can give more information when someone asks a long query
#     or someone asks relation of upto three entities.
#     answer:
#     """
#     return prompt






# def ask(prompt):
#     client=Groq(api_key=os.environ.get("api_key"))

#     response=client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

#     return response.choices[0].message.content
# question=input("Ask: ")

# prompt=build_prompt(question)

# answer=ask(prompt)

# print(answer)
import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer
import os

KEY = "your_new_key_here"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

groq_client = Groq(api_key=KEY)
groq_model = "llama-3.1-8b-instant"

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chroma_client = chromadb.PersistentClient(path="chroma_storage")
collection = chroma_client.get_collection("book_content")


def build_prompt(question):
    query_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["metadatas", "documents", "distances"]
    )
    best_distance = results["distances"][0][0]

    if best_distance > 1.2:
        return "OUT_OF_BOOK"
    print("Retrieved metadata:")
    print(results["metadatas"][0])

    print("Retrieved documents preview:")
    for doc in results["documents"][0]:
        print(doc[:100])
        print("-" * 50)

    documents = results["documents"][0]
    context = "\n\n".join(documents)

    prompt = f"""Hello Groq, you are a set of teachers, Whose subject depends on the content given to you.
    You have to give response like you are teaching a college student. Types of questions you could expect from the user:
    1) Relation betweeen certain topics, equations or figure or it could be in the form of relation of certain topic with ceratin equations or figures.
     2) Explanation of Topics/Titles, Equations or figures could also be asked.
     3) Closest candidates of content related to certain topics/titles, equations or figures. You have to give explain their relation.
     Most Important instruction:
     - You have to explain by content provided to you. It is usually going to be a set of Three lists.
     The three lists are going to be closest content related to what have asked .
     Context={context},
     Question asked by user={question}
     You have to give answer in the format of:
     -Question asked by user
     -your findings based upon Context given to you.
     You have to give answer in range of 100-200 words only. Give more information by expanding the word range
     if you think this is not sufficient information for question asked. 
     You can give more information when someone asks a long query
     or someone asks relation of upto three entities.
     "I am unable to find any relevant content as per your question asked. It seems like you have 
     asked for something that doesn't exist in the book"
     if you find the retrieved data irrevalent
     answer:
     """
    

    return prompt


def ask(prompt):
    response = groq_client.chat.completions.create(
        model=groq_model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


question = input("Ask: ")
prompt = build_prompt(question)
answer = ask(prompt)


if prompt == "OUT_OF_BOOK":
    print("I am unable to find any relevant content as per your question asked. It seems like you have asked for something that doesn't exist in the book")
else:
    answer = ask(prompt)
    print(answer)
while True:
    question = input("Ask: ")

    if question.lower() == "exit":
        print("Stopped.")
        break

    prompt = build_prompt(question)
    answer = ask(prompt)

    print(answer)






