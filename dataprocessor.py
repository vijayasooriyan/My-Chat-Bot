from pdfreader import read_pdf
from chunker import chunk_pages
from embedder import embed_chunks
from vectorstore import store_in_pinecone
from typing import List

pdf_path = "./resources/Vijayasooriyan-Kamarajah's CV.pdf"

def run():
    pages=read_pdf(pdf_path)
    print(f"Extracted Pages: {len(pages)} pages from the PDF.")
    
    chunks=chunk_pages(pages)
    print(f"Created {len(chunks)} chunks from PDF.")
    
    embeddings=embed_chunks(chunks)
    print(f"Generated {len(embeddings)} embeddings.")
    
    store_in_pinecone(chunks,embeddings)
    print("Successfully stored embeddings in Pinecone!")

if __name__ =="__main__":
    run()