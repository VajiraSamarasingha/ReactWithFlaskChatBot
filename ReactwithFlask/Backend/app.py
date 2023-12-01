from flask import Flask, request, jsonify
from flask_cors import CORS

import pickle
import datetime

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import pinecone
import os
import sys
import pinecone

from langchain.document_loaders.onedrive_file import CHUNK_SIZE


app = Flask(__name__)
CORS(app)

def prediction(question):

    loader = PyPDFDirectoryLoader("pdfs")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunk = text_splitter.split_documents(data)

    os.environ['GOOGLE_API_KEY'] = 'AIzaSyCY1astH7htKBLHyzP8NohZ9JUFp7RWK1U'
    embeddings = GooglePalmEmbeddings()
    query_result = embeddings.embed_query("Hello World") 
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY','fc863bc0-4450-4667-ac34-84e77ee1552c')
    PINECODE_API_ENV = os.environ.get('PINECONE_API_ENV','gcp-starter')

    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment = PINECODE_API_ENV
    )
    index_name = "langchain"

    docsearch = Pinecone.from_texts([t.page_content for t in text_chunk], embeddings,index_name=index_name)

    query = "what is vinaya pitaka"

    docs = docsearch.similarity_search(query,k=4)

    llm = GooglePalm(temperature=0.1)

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
     
    user_input = question

    if user_input == "exit":
        print("Existing")
    if user_input == '':
        print("Please enter a question")
    result = qa({'query': user_input})

    if 'result' in result:
        return result['result']
    else:
        return "Sorry, I don't know the answer to that question."



@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data['message']

    #bot_response = f"Received your message: '{user_message}'"
    bot_response = prediction(user_message)


    return jsonify({'message': bot_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
