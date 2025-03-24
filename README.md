# Web Q&A Tool

This is a simple web-based **Question Answering (Q&A) Tool** that allows users to input URLs, scrape the content from those pages, and ask questions based on that content. The tool uses the **Flask** framework for the backend and **Hugging Face's transformers library** for the Q&A functionality.

## Features

- Scrapes content from provided URLs.
- Allows users to ask questions based on the scraped content.
- Displays answers generated from the content using a pre-trained model like **BERT** or **DistilBERT**.
- Simple, minimal UI built with HTML, CSS, and JavaScript.

## Requirements

To run this project locally, you need to have **Python 3.8 or above** installed. You also need the following dependencies:

- **Flask**
- **BeautifulSoup**
- **requests**
- **transformers**
- **torch**

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/qa-tool.git
cd qa-tool
