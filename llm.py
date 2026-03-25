from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def query_llm_with_context(query: str, context: str) -> str:
    """Generate a response using Groq API with the provided context."""
    
    if not context or context.strip() == "":
        return "I couldn't find any relevant information in the CV to answer your question. Please try a different question."
    
    system_prompt = """You are a helpful assistant answering questions about a professional's CV and experience.
    Use the provided context to give accurate, relevant, and helpful answers.
    Be concise but informative. If the context doesn't have enough information, acknowledge that.
    Format your response in a clear, readable way."""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context from CV:\n{context}\n\nQuestion: {query}\n\nAnswer based on the context:"}
            ],
            temperature=0.4,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}. Please try again."