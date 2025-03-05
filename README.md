# Talk with PDF

A local, multi-modal LLM-powered chat application that processes PDFs and Word files, answers questions about their content, and generates Mermaid syntax for diagrams—all running on your machine with no external server required. Built with Streamlit, LLaVA 7B (via Ollama), and Python, this project was developed and tested on an M3 Mac with 16GB RAM.

<img width="3008" alt="Screenshot 2025-03-04 at 5 29 47 PM" src="https://github.com/user-attachments/assets/8ea0322a-3d4a-4007-9af9-aedf3c3e407c" />

*Main interface showing file upload and chat with question/answer styling.*

## Features
- **File Support**: Upload and process `.pdf` and `.docx` files locally.
- **Multi-Modal**: Extracts text and OCRs images/charts from PDFs (text-only for `.docx` currently).
- **Chat Interface**: Ask questions via a web UI, submit with "Enter" or "Send" button.
- **Font Styling**: Questions in larger font (20px) than answers (16px) for readability.
- **Mermaid Syntax**: Request diagram syntax (e.g., flowcharts) based on document content.
- **Local Execution**: Runs entirely on your machine using LLaVA 7B via Ollama.

## Why LLaVA?

This project uses LLaVA 7B (Large Language and Vision Assistant), a multi-modal LLM, for several key reasons:

- **Multi-Modal Capability**: LLaVA can process both text and images, making it ideal for handling PDFs with mixed content (text, images, charts). While Word file support is currently text-only, LLaVA’s vision capability sets the stage for future `.docx` image extraction.
- **Local Execution**: Paired with Ollama, LLaVA runs entirely on your machine, aligning with the project’s goal of privacy and offline functionality—no cloud dependency required.
- **Resource Efficiency**: The 7B parameter version (quantized to ~8-10GB) fits within the 16GB RAM of an M3 Mac, balancing performance and memory constraints. Larger models (e.g., 13B) would exceed available resources.
- **Natural Language Understanding**: LLaVA excels at reasoning and generating human-like responses, crucial for answering questions and structuring Mermaid syntax from document content.
- **Open-Source Flexibility**: Available via Ollama, LLaVA is free, customizable, and well-supported, making it a practical choice over proprietary or heavier alternatives like GPT-4 or larger LLaMA variants.

## Prerequisites
- **Hardware**: Tested on an M3 Mac with 16GB RAM (CPU-only; GPU optional).
- **OS**: macOS (adaptable to Linux/Windows with minor tweaks).
- **Software**:
  - Python 3.10+ (3.13 used here).
  - Homebrew (for macOS dependencies).
  - Ollama (to run LLaVA 7B locally).

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Baki998899/AI_Chat.git
cd AI_Chat
```
### 2. Virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install libraries
```bash
pip install --upgrade pip
pip install pymupdf pillow pytesseract pdf2image ollama streamlit python-docx
```
### 4. Homebrew dependencies
```bash
brew install tesseract poppler
```
### 5. [Download and Install Ollama](ollama.com) and LLaVA 7B
### 6. After Installing Ollama, then in terminal run:
```bash
ollama pull llava:7b
```
