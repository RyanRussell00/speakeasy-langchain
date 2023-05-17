from flask import Flask, request
from llama_index import GPTVectorStoreIndex, download_loader
from llama_index.readers.schema.base import Document
import os

app = Flask(__name__)

os.environ['OPENAI_API_KEY'] = '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'


@app.route('/endpoint', methods=['GET'])
def single_endpoint():
    query_param = request.args.get('query', '')
    print(f'You sent the query parameter: {query_param}')
    ApifyActor = download_loader("ApifyActor", refresh_cache=True)
    print(f"ApifyActor: {ApifyActor} \n")
    reader = ApifyActor("apify_api_ywr4Xs6t6UW9DOUcudwwFZ04hE5YqR3wbkds")
    print(f"Reader: {reader.load_data} \n")
    documents = reader.load_data(
        actor_id="apify/website-content-crawler",
        run_input={"startUrls": [
            {"url": "https://llamahub.ai/l/apify-actor"}]},
        dataset_mapping_function=tranform_dataset_item,
    )
    print(f"Documents: {str(documents)} \n")
    index = GPTVectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query(query_param)

    return str(response), 200


if __name__ == '__main__':
    app.run(debug=True)

def tranform_dataset_item(item):
    doc = Document(
        item.get("text"),
        extra_info={
            "url": item.get("url"),
        },
    )
    print(f"Doc: {doc} \n")
    return doc

# import os

# from flask import Flask, stream_with_context, request
# # Import necessary packages
# from llama_index import GPTVectorStoreIndex, Document, SimpleDirectoryReader, StorageContext, load_index_from_storage, download_loader
# from llama_index import download_loader
# from llama_index.readers.schema.base import Document
# import os
# from pathlib import Path

# app = Flask(__name__)
# os.environ['OPENAI_API_KEY'] = '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'

# @app.route("/")
# def home():
#     query_text = request.args.get("text", None)
#     if query_text is None:
#         return "No text found, please include a ?text=blah parameter in the URL", 400
#     ApifyActor = download_loader("ApifyActor")
#     print(f"ApifyActor: {ApifyActor} \n")
#     reader = ApifyActor("apify_api_ywr4Xs6t6UW9DOUcudwwFZ04hE5YqR3wbkds")
#     print(f"Reader: {reader.load_data} \n")
#     documents = reader.load_data(
#         actor_id="apify/website-content-crawler",
#         run_input={"startUrls": [
#             {"url": "https://bitcoin.org/bitcoin.pdf"}]},
#         dataset_mapping_function=tranform_dataset_item
#     )
#     print(f"Documents: {documents} \n")
#     index = GPTVectorStoreIndex.from_documents(documents)
#     query_engine = index.as_query_engine()
#     response = query_engine.query(query_text)
#     return str(response), 200



# # @app.route('/')
# # def home():
# #     ApifyActor = download_loader("ApifyActor")

# #     reader = ApifyActor("apify_api_ywr4Xs6t6UW9DOUcudwwFZ04hE5YqR3wbkds")
# #     print(f"Reader: {reader} \n")

# #     documents = reader.load_data(
# #         actor_id="apify/website-content-crawler",
# #         run_input={"startUrls": [
# #             {"url": "https://bitcoin.org/bitcoin.pdf"}]},
# #         dataset_mapping_function=tranform_dataset_item
# #     )
# #     print(f"Documents: {documents} \n")

# #     index = GPTVectorStoreIndex.from_documents(documents)
# #     print(f"Index: {index} \n")

# #     # query_engine = index.as_query_engine()

# #     # response = query_engine.query("Explain proof of work?")
# #     # print(f"Response: {response} \n")
# #     return stream_with_context(index.query("Explain proof of work", streaming=True).response_gen)
# #     # return "OK"
