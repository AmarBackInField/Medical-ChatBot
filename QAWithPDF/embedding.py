from llama_index.core import VectorStoreIndex
from llama_index.core import ServiceContext
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.gemini import GeminiEmbedding

from QAWithPDF.data_ingestion import load_data
from QAWithPDF.model_api import load_model

import sys
import logging
import os
from dotenv import load_dotenv
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
def download_gemini_embedding(model,document):
    """
    Downloads and initializes a Gemini Embedding model for vector embeddings.

    Returns:
    - VectorStoreIndex: An index of vector embeddings for efficient similarity queries.
    """
    try:
        logging.info("GeminiEmbeddings is called")
        gemini_embed_model = GeminiEmbedding(api_key=GOOGLE_API_KEY,model_name="models/embedding-001")
        service_context = ServiceContext.from_defaults(llm=model,embed_model=gemini_embed_model, chunk_size=800, chunk_overlap=20)
        
        logging.info("Vector Stores Index called")
        index = VectorStoreIndex.from_documents(document,service_context=service_context)
        index.storage_context.persist()
        
        logging.info(" Done Query Generated")
        query_engine = index.as_query_engine()
        return query_engine
    except Exception as e:
        raise 