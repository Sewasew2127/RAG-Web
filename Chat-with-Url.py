import streamlit as st
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Page configuration
st.set_page_config(
    page_title="WebChat AI",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #f5f7fa, #e3eeff);
    }
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        color: #1e3c72;  
        background: linear-gradient(90deg, #2193b0, #6dd5ed);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4em !important;
        font-weight: 800;
        text-align: center;
        margin: 1em 0 0.2em 0 !important;
        padding: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .sub-title {
        color: #4a4a4a;
        font-size: 1.5em !important;
        margin: 0 0 2em 0 !important;
        font-style: italic;
        text-align: center;
        font-weight: 300;
    }
    .url-input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .user-message {
        background: #E3F2FD;
    }
    .assistant-message {
        background: white;
    }
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0,0,0,.3);
        border-radius: 50%;
        border-top-color: #1e3c72;
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    .thinking {
        display: flex;
        align-items: center;
        font-style: italic;
        color: #666;
        padding: 1rem;
        border-radius: 10px;
        background: rgba(255,255,255,0.8);
        margin-bottom: 1rem;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Header section with custom styling
st.markdown('<h1 class="main-title">WebChat AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Your helpful companion for webpage exploration.</p>', unsafe_allow_html=True)

# Create two columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # URL input with custom styling
    webpage_url = st.text_input("🔗 Enter webpage URL:", 
                               type="default",
                               placeholder="https://example.com",
                               help="Enter the URL of any webpage you'd like to chat about")

    if webpage_url and st.session_state.vectorstore is None:
        with st.spinner("🔄 Processing webpage content..."):
            loader = WebBaseLoader(webpage_url)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=10)
            splits = text_splitter.split_documents(docs)
            embeddings = OllamaEmbeddings(model='mistral')
            st.session_state.vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
            st.success("✨ Webpage loaded successfully! Ask me anything about it.")

def ollama_llm(question, context, conversation_history):
    # Format the conversation history
    history_text = ""
    if conversation_history:
        history_text = "Previous conversation:\n"
        for msg in conversation_history[-4:]:  # Get last 4 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
    
    if context.strip():
        formatted_prompt = f"""Please help me understand the webpage content and answer the question. Feel free to provide insights, interpretations, or additional context beyond the literal text.

{history_text}
Webpage Context: {context}

Current Question: {question}

Guidance:
- Provide a comprehensive and thoughtful response
- Draw connections and insights where possible
- If the context is limited, supplement with relevant background knowledge"""
    else:
        formatted_prompt = f"""I'm seeking insights on the following question. While no specific context is provided, please offer a helpful and informative response.

{history_text}
Current Question: {question}

Guidance:
- Provide a detailed and nuanced answer
- Feel free to draw from general knowledge
- If relevant, suggest ways to find more specific information"""

    response = ollama.chat(model='mistral', messages=[{"role": "user", "content": formatted_prompt}])
    return response['message']['content']

def rag_chain(question):
    if st.session_state.vectorstore is None:
        return "Please enter a webpage URL first."
    
    retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 5})
    retrieved_docs = retriever.invoke(question)
    
    formatted_context = "\n\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else ""
    return ollama_llm(question, formatted_context, st.session_state.messages[:-1] if len(st.session_state.messages) > 0 else [])

# Display chat messages with improved styling
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <b>You:</b> {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant-message">
                     {message["content"]}
                </div>
            """, unsafe_allow_html=True)

# Chat input with custom styling
if prompt := st.chat_input("💭 Ask about the webpage..."):
    with st.container():
        # Display user message
        st.markdown(f"""
            <div class="chat-message user-message">
                <b>You:</b> {prompt}
            </div>
        """, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show thinking animation
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("""
        <div class="thinking">
            <div class="loading"></div>
            <span>Thinking...</span>
        </div>
    """, unsafe_allow_html=True)

    # Generate and display assistant response
    with st.container():
        response = rag_chain(prompt)
        thinking_placeholder.empty()  # Remove thinking animation
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <b>AI:</b> {response}
            </div>
        """, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button with better styling
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()