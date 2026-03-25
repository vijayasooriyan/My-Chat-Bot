# 🤖 CV Chatbot - Production Ready Chatbot

A fully functional AI-powered chatbot that answers questions about a professional CV using semantic search and OpenAI's GPT-3.5-turbo.

## ✨ Features

### Core Functionality
- ✅ **Real OpenAI Integration** - Uses GPT-3.5-turbo for intelligent responses
- ✅ **Vector Database** - Pinecone-powered semantic search
- ✅ **Conversation Memory** - Remembers all messages in the session
- ✅ **Beautiful UI** - Modern Streamlit interface with custom styling
- ✅ **Persistent Chat History** - Messages persist during session
- ✅ **Error Handling** - Graceful error messages and fallbacks

### Technical Stack
- **Frontend**: Streamlit (web UI)
- **Embeddings**: Sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: Pinecone
- **LLM**: OpenAI GPT-3.5-turbo
- **Language**: Python 3.8+

## 📋 Project Structure

```
my_chatbot/
├── streamlit_app.py          # Main Streamlit application
├── llm.py                    # OpenAI integration & response generation
├── embedder.py              # Text embedding using sentence-transformers
├── vectorstore.py           # Pinecone database operations
├── pdfreader.py             # PDF reading functionality
├── chunker.py               # Text chunking logic
├── dataprocessor.py         # Data pipeline coordinator
├── QueryProcessor.py        # Query processing pipeline
├── .env                     # Environment variables (secrets)
├── requirements.txt         # Python dependencies
└── resources/               # PDF documents folder
    └── Vijayasooriyan-Kamarajah's CV.pdf
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Pinecone account (free tier available)
- OpenAI account with API access

### Step 1: Clone/Setup Project
```bash
cd my_chatbot
```

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
