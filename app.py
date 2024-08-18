from flask import Flask, render_template, jsonify, request
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import  download_gemini_embedding
from QAWithPDF.model_api import load_model
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

try:
    document = load_data('data')
    logger.info("Document loaded successfully.")
    model = load_model()
    logger.info("Model loaded successfully.")
    query_engine = download_gemini_embedding(model, document)
    logger.info("Gemini embedding downloaded and query engine initialized.")
except Exception as e:
    logger.error(f"Error during setup: {e}")

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    logger.info(f"Input message: {msg}")
    try:
        result = query_engine.query(msg)
        logger.info(f"Response: {result.response}")
        return str(result.response)
    except Exception as e:
        logger.error(f"Error during query: {e}")
        return "Error processing your request."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
