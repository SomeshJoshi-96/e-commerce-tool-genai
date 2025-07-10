import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from groq import Groq
import os


load_dotenv()

faqs_path = Path(__file__).parent/"resources/faq_data.csv"

chroma_client = chromadb.Client()
collection_name_faq = 'faq'

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)


groq_client = Groq()

def ingest_faq_data(faqs_path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        collection = chroma_client.get_or_create_collection(
            name = collection_name_faq,
            embedding_function=ef
        )
        print(faqs_path)
        df = pd.read_csv(faqs_path)
        docs = df['question'].to_list()
        metadata = [{'answer':ans} for ans in df['answer'].to_list()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collection.add(documents=docs, metadatas=metadata, ids=ids)
        print(f"FAQ data successfully ingested into chrome collection: {collection_name_faq}")
    else:
        print(f"Collection: {collection_name_faq} already present")

def get_relevant_qa(query):
    collection = chroma_client.get_collection(name=collection_name_faq)
    result = collection.query(
        query_texts=[query],
        n_results=2
    )
    return result

def faq_chain(query):
    result = get_relevant_qa(query)
    context = ''.join([r.get('answer') for r in result['metadatas'][0]])
    answer = generate_answer(query, context)
    return answer


def generate_answer(query, context):
    prompt = f'''Given the question and context below, generate the answer based on the context only.
    If you don't find the answer inside the context then say "I don't know".
    Do not make things up.

    QUESTION: {query}

    CONTEXT: {context}
    '''
    # call llm
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=os.environ['GROQ_MODEL'],
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    ingest_faq_data(faqs_path)
    query = "When will I get my refund once I return something?"
    result = faq_chain(query)
    print(result)