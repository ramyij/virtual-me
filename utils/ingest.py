import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document

# ----- LOAD ENV VARS -----
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = "virtual-me"

# ----- INIT -----
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)





document_1 = Document(
    page_content="I had chocalate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
)

document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    metadata={"source": "news"},
)

document_3 = Document(
    page_content="Building an exciting new project with LangChain - come check it out!",
    metadata={"source": "tweet"},
)

document_4 = Document(
    page_content="Robbers broke into the city bank and stole $1 million in cash.",
    metadata={"source": "news"},
)

document_5 = Document(
    page_content="Wow! That was an amazing movie. I can't wait to see it again.",
    metadata={"source": "tweet"},
)

document_6 = Document(
    page_content="Is the new iPhone worth the price? Read this review to find out.",
    metadata={"source": "website"},
)

document_7 = Document(
    page_content="The top 10 soccer players in the world right now.",
    metadata={"source": "website"},
)

document_8 = Document(
    page_content="LangGraph is the best framework for building stateful, agentic applications!",
    metadata={"source": "tweet"},
)

document_9 = Document(
    page_content="The stock market is down 500 points today due to fears of a recession.",
    metadata={"source": "news"},
)

document_10 = Document(
    page_content="I have a bad feeling I am going to get deleted :(",
    metadata={"source": "tweet"},
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
]
uuids = [str(uuid4()) for _ in range(len(documents))]

vector_store.add_documents(documents=documents, ids=uuids)

# # ----- FILE LOADER MAPPING -----
# loader_map = {
#     ".pdf": UnstructuredPDFLoader,
#     ".docx": UnstructuredWordDocumentLoader,
#     ".md": UnstructuredMarkdownLoader,
#     ".html": UnstructuredHTMLLoader
# }

# # ----- LOAD DOCS -----
# def load_documents_from_folder(folder_path: str):
#     documents = []
#     for filename in os.listdir(folder_path):
#         filepath = os.path.join(folder_path, filename)
#         ext = os.path.splitext(filename)[1].lower()
#         loader_class = loader_map.get(ext)

#         if loader_class:
#             print(f"Loading {filename}...")
#             loader = loader_class(filepath)
#             docs = loader.load()
#             documents.extend(docs)
#         else:
#             print(f"Skipping unsupported file: {filename}")
#     return documents

# # ----- SPLIT & INGEST -----
# def ingest_documents(folder_path: str):
#     raw_docs = load_documents_from_folder(folder_path)
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     split_docs = splitter.split_documents(raw_docs)

#     vectorstore = PineconeVectorStore(index=index, embedding=embedding)
#     vectorstore.add_documents(split_docs)
#     print("\n✅ Ingestion complete.")

# # ----- RUN -----
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python ingest.py <folder_path>")
#         sys.exit(1)

#     folder_path = sys.argv[1]
#     if not os.path.isdir(folder_path):
#         print(f"Error: {folder_path} is not a valid directory.")
#         sys.exit(1)

#     ingest_documents(folder_path)
