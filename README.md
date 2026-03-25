# 🤖 CV Chatbot - AI-Powered Interview Chatbot

A sophisticated AI-powered chatbot that answers questions about a professional CV using semantic search, vector embeddings, and advanced language models. Built with Streamlit, Pinecone, and Groq Llama 3.3.

## ✨ Features

### Core Functionality
- ✅ **Semantic Search** - Pinecone vector database for intelligent document retrieval
- ✅ **AI Responses** - Groq Llama 3.3 LLM for natural language generation
- ✅ **Conversation Memory** - Maintains chat history throughout the session
- ✅ **Beautiful Responsive UI** - Modern Streamlit interface with animations
- ✅ **Real-time Processing** - Instant responses with visual feedback
- ✅ **Error Handling** - Graceful error management and user guidance

### Technical Stack
- **Frontend**: Streamlit (responsive web UI)
- **Embeddings**: Sentence-transformers (all-MiniLM-L6-v2, 384 dimensions)
- **Vector Database**: Pinecone (512-dimensional index)
- **LLM**: Groq Llama 3.3
- **Language**: Python 3.10+
- **Deployment Ready**: Can be deployed to Streamlit Cloud

## 📋 Project Structure

```
my_chatbot/
├── streamlit_app.py          # Main Streamlit application (UI)
├── llm.py                    # Groq LLM integration
├── embedder.py              # Text embedding & vector processing
├── vectorstore.py           # Pinecone database operations
├── pdfreader.py             # PDF reading & extraction
├── chunker.py               # Text chunking & preprocessing
├── dataprocessor.py         # Data pipeline orchestration
├── QueryProcessor.py        # Query processing script
├── requirements.txt         # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore configuration
├── README.md                # Documentation
└── resources/               # Documents folder
    └── CV.pdf               # Resume/CV document
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Pinecone account (free tier available)
- Groq API key (free at https://console.groq.com)

### Step 1: Clone the Repository
```bash
git clone https://github.com/vijayasooriyan/My-Chat-Bot.git
cd My-Chat-Bot
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Create a .env file with your API keys
echo "PINECONE_API_KEY=your_pinecone_api_key" > .env
echo "PINECONE_INDEX_NAME=your_index_name" >> .env
echo "GROQ_API_KEY=your_groq_api_key" >> .env
```

### Step 5: Add Your Document
Place your PDF file in the `resources/` folder and update the paths in `pdfreader.py` if needed.

### Step 6: Process the Document
```bash
python dataprocessor.py  # This will parse and store chunks in Pinecone
```

### Step 7: Run the Chatbot
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 🔧 Configuration

### Environment Variables (.env)
```
PINECONE_API_KEY=your_api_key_here
PINECONE_INDEX_NAME=your_index_name
GROQ_API_KEY=your_groq_api_key
```

### Embedding Configuration
- **Model**: sentence-transformers/all-MiniLM-L6-v2
- **Dimension**: 384 (padded to 512 for Pinecone)
- **Chunk Size**: Configurable in chunker.py

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Copy `.env` and add your API keys:

```bash
# .env file
PINECONE_API_KEY=your_actual_pinecone_key_here
PINECONE_INDEX_NAME=mychatbot
OPENAI_API_KEY=your_actual_openai_key_here
```

**Get Your API Keys:**
- **Pinecone**: https://www.pinecone.io/ (free tier available)
- **OpenAI**: https://platform.openai.com/api-keys

### Step 4: Populate Vector Database (First Time Only)

```bash
python dataprocessor.py
```

This will:
1. Read the PDF from `resources/`
2. Split text into chunks
3. Generate embeddings
4. Store in Pinecone

### Step 5: Run the Chatbot

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 🎯 How It Works

```
User Question
    ↓
Embed with Sentence-Transformers
    ↓
Search Pinecone (Vector Similarity)
    ↓
Retrieve Top 5 Matching Chunks
    ↓
Send to OpenAI with Context
    ↓
GPT-3.5-turbo Generates Response
    ↓
Display in Chat Interface
```

## 💬 Example Questions

Try asking:
- "What are your technical skills?"
- "Tell me about your Python experience"
- "What projects have you built?"
- "What certifications do you have?"
- "Tell me about your work experience"
- "What tools and frameworks do you know?"

## 🔧 Configuration

### Entities to Customize

**1. Update PDF Source** (`dataprocessor.py`)
```python
pdf_path = "./resources/your-cv-name.pdf"  # Change this
```

**2. Change Pinecone Index Name** (`.env`)
```
PINECONE_INDEX_NAME=my-index-name
```

**3. Customize LLM Behavior** (`llm.py`)
```python
model="gpt-3.5-turbo"      # Can change to gpt-4
temperature=0.7            # Adjust creativity (0-1)
max_tokens=500             # Adjust response length
```

## 📊 Monitoring

The Streamlit sidebar shows:
- Total questions asked
- Number of chat turns
- Conversation ID
- API connection status
- Chat statistics

## ⚠️ Troubleshooting

### Issue: "Missing API Keys"
**Solution**: 
1. Create `.env` file from `.env.example`
2. Add your actual Pinecone and OpenAI keys
3. Save and restart the app

### Issue: "Pinecone index is empty"
**Solution**:
1. Run `python dataprocessor.py` to populate the database
2. Wait for embeddings to generate
3. Then run the Streamlit app

### Issue: OpenAI API errors
**Solution**:
1. Check your OpenAI API key is valid
2. Verify you have sufficient credits
3. Check your usage limits at https://platform.openai.com/account/billing

### Issue: Slow responses
**Solution**:
- This is expected for first request (model loading)
- Subsequent requests are faster
- Can be optimized by caching the embedding model

## 📈 Performance Tips

1. **First Run**: Embedding model downloads (~400MB) - takes time
2. **API Costs**: Each query costs small amount (GPT-3.5-turbo uses ~100 tokens/response)
3. **Batch Processing**: Process multiple queries at once to reduce overhead

## 🔐 Security

- ✅ API keys stored in `.env` (never commit this)
- ✅ `.env` included in `.gitignore`
- ✅ Pinecone API key secured
- ✅ No sensitive data in code

## 📝 Files Overview

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Main web interface |
| `llm.py` | OpenAI GPT integration |
| `embedder.py` | Text-to-vector conversion |
| `vectorstore.py` | Pinecone operations |
| `pdfreader.py` | PDF extraction |
| `chunker.py` | Text splitting |
| `dataprocessor.py` | ETL pipeline |

## All Issues Fixed ✅

✅ **Real LLM Integration** - Now uses actual OpenAI GPT-3.5-turbo  
✅ **API Key Documentation** - .env.example provided with setup guide  
✅ **Conversation Memory** - Remembers all previous messages  
✅ **No Duplicate Files** - Only streamlit_app.py used  
✅ **Error Handling** - Graceful error messages with fallbacks  
✅ **Session Persistence** - Chat history maintained in session  

## 🎓 Learn More

-OpenAI Documentation: https://platform.openai.com/docs
- Pinecone Docs: https://docs.pinecone.io/
- Streamlit Docs: https://docs.streamlit.io/
- Sentence-Transformers: https://www.sbert.net/

## 📄 License

This project is open source for educational purposes.

## 👤 Author

Created with ❤️ for CV chatbot demonstration.

---

**Last Updated**: March 2026  
**Status**: ✅ Production Ready
