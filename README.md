# 🌐 Web Content RAG Chatbot

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)](https://github.com/hwchase17/langchain)
[![Mistral](https://img.shields.io/badge/Mistral-AI-purple.svg)](https://mistral.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 💡 Have interactive, context-aware conversations about any webpage's content using advanced AI technology.

<div align="center">
  <img src="https://github.com/Sewasew2127/RAG-Web/blob/main/assets/Demo.gif" alt="Demo GIF" width="600px">
</div>

## ✨ Features

- 🔍 **Smart Content Processing**: Automatically extracts and processes webpage content
- 🧠 **Contextual Memory**: Maintains conversation history for coherent dialogue
- 🎯 **Precise Retrieval**: Uses vector similarity to find relevant information
- 💬 **ChatGPT-like Interface**: Clean and intuitive chat experience
- 🚀 **Real-time Responses**: Powered by the Mistral language model

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Language Model**: Mistral (via Ollama)
- **Vector Database**: Chroma
- **Document Processing**: LangChain
- **Embeddings**: Ollama Embeddings

## 🚀 Getting Started

### Prerequisites

```bash
# Install Ollama (Mac/Linux)
curl https://ollama.ai/install.sh | sh

# Pull the Mistral model
ollama pull mistral
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sewasew2127/RAG-Web.git
cd RAG-Web
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run Chat-with-Url.py
```

## 🎮 Usage

1. Launch the application
2. Enter any webpage URL in the input field
3. Wait for the content to be processed
4. Start asking questions about the webpage content
5. Enjoy natural, context-aware conversations!

## 📝 Example Conversation

```
User: What is the main topic of this webpage?
Assistant: [Provides comprehensive summary of the webpage's main topic]

User: Can you elaborate more on that?
Assistant: [Gives detailed explanation while maintaining context]

User: How does this compare to [related topic]?
Assistant: [Offers relevant comparison based on webpage content]
```



## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [LangChain](https://github.com/hwchase17/langchain) for document processing capabilities
- [Mistral AI](https://mistral.ai/) for the powerful language model
- [Ollama](https://ollama.ai/) for local model hosting

---

<div align="center">
  Made with ❤️ by Sewasew Hailu
</div>


