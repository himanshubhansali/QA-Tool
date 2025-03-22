
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Load the fine-tuned BERT model
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# Function to scrape content
def fetch_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text only from relevant content (main sections)
            content = ''
            main_content = soup.find('main')  # Often the main content is in <main> tag
            if main_content:
                paragraphs = main_content.find_all('p')
                content = ' '.join([para.get_text() for para in paragraphs])
            else:
                paragraphs = soup.find_all('p')  # Fallback to all <p> tags if no <main>
                content = ' '.join([para.get_text() for para in paragraphs])
            return content
        else:
            return None
    except Exception as e:
        return None

# Function to process and chunk the content (for large pages)
def chunk_content(content, max_length=512):
    tokens = content.split()
    chunks = []
    while tokens:
        chunk = ' '.join(tokens[:max_length])
        chunks.append(chunk)
        tokens = tokens[max_length:]
    return chunks

# Function to get an answer from multiple content chunks
def get_answer_from_chunks(question, content):
    chunks = chunk_content(content)
    answers = []
    for chunk in chunks:
        result = qa_pipeline({'context': chunk, 'question': question})
        answers.append(result['answer'])
    return max(set(answers), key=answers.count)  # Combine answers

# Route for the home page (UI)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['GET'])
def scrape_url():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    content = fetch_content(url)
    if content:
        return jsonify({'content': content}), 200
    else:
        return jsonify({'error': 'Failed to fetch content from the URL'}), 500

@app.route('/ask', methods=['GET'])
def ask_question():
    url = request.args.get('url')
    question = request.args.get('question')
    if not url or not question:
        return jsonify({'error': 'Both URL and Question are required'}), 400

    content = fetch_content(url)
    if content:
        answer = get_answer_from_chunks(question, content)
        return jsonify({'answer': answer}), 200
    else:
        return jsonify({'error': 'Failed to fetch content from the URL'}), 500

if __name__ == '__main__':
    app.run(debug=True)
