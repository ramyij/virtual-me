import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
# from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
# import pinecone
from pinecone import Pinecone, ServerlessSpec


# ----- LOAD ENV VARS -----
load_dotenv()

# ----- CONFIG -----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = "virtual-me"

# ----- INIT -----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

# Load embedding + vectorstore
embedding = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY, dimensions=1024)
index = pc.Index(PINECONE_INDEX)
vectorstore = PineconeVectorStore(index=index, embedding=embedding)
retriever = vectorstore.as_retriever()


# Chat model + retrieval chain
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# ----- API Schema -----
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# ----- Endpoint -----
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    user_message = req.message
    response = qa_chain.run(user_message)
    return {"response": response}

# Optional: root ping
@app.get("/")
def read_root():
    return {"message": "Virtual You API is running."}
