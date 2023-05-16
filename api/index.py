import os

from flask import Flask
# Import necessary packages
from llama_index import GPTVectorStoreIndex, Document, SimpleDirectoryReader, StorageContext, load_index_from_storage, download_loader
from llama_index import download_loader
from llama_index.readers.schema.base import Document
import os
from pathlib import Path

app = Flask(__name__)
os.environ['OPENAI_API_KEY'] = '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'

@app.route('/')
def home():
    ApifyActor = download_loader("ApifyActor")

    reader = ApifyActor("apify_api_ywr4Xs6t6UW9DOUcudwwFZ04hE5YqR3wbkds")
    documents = reader.load_data(
        actor_id="apify/website-content-crawler",
        run_input={"startUrls": [
            {"url": "https://bitcoin.org/bitcoin.pdf"}]},
        dataset_mapping_function=tranform_dataset_item
    )
    index = GPTVectorStoreIndex.from_documents(documents)

    query_engine = index.as_query_engine()

    response = query_engine.query("Explain proof of work?")
    print(f"Response: {response} \n")
    return response
    
def tranform_dataset_item(item):
    return Document(
        item.get("text"),
        extra_info={
            "url": item.get("url"),
        },
    )