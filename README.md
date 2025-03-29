# Local AI Document Analyzer

This tool provides local analysis of .docx files using Ollama and DeepSeek AI model. It can extract content, analyze structure, and answer questions about the document content.

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally
- DeepSeek model pulled in Ollama

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running and the DeepSeek model is installed:
```bash
ollama pull deepseek-coder
```

## Usage

The tool provides several ways to analyze documents:

### Generate Document Summary
```bash
python main.py --file path/to/document.docx --summary
```

### Ask Questions About the Document
```bash
python main.py --file path/to/document.docx --query "Your question here"
```

### Analyze Importance of Specific Elements
```bash
python main.py --file path/to/document.docx --analyze "Element to analyze"
```

## Features

- Document structure analysis (headings, paragraphs, tables)
- Natural language querying
- Document summarization
- Importance analysis of specific elements
- Local processing using Ollama and DeepSeek

## Architecture

The tool consists of three main components:

1. `docx_processor.py`: Handles document loading and content extraction
2. `ai_agent.py`: Manages AI model integration and analysis
3. `main.py`: Command-line interface for user interaction

## Error Handling

The tool includes comprehensive error handling for:
- File loading issues
- AI model processing errors
- Invalid queries or analysis requests

## Contributing

Feel free to submit issues and enhancement requests! 