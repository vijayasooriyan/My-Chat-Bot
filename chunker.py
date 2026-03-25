from typing import List,Tuple

def chunk_pages(pages: List[str],chunk_size:   int =900,chunk_overlap: int =150)-> List[str]:

    #"""takes pages from read_pdf and returns (chunks, pages_map)."""
    # chunks:List[str]=[]
    # for text in pages:
    #     start = 0
    #     n = len(text)
    #     while start < n:
    #         end = min(start + chunk_size,n)
    #         chunk = text[start:end]
    #         last_period = chunk.rfind(". ")
    #         if last_period != -1 and end < n and (last_period>chunk_size * 0.5):
    #             end =start + last_period +2
    #             chunk = text[start:end]
    #         chunks.append(chunk.strip())
    #         start = max(end - chunk_overlap,end)
    # return chunks

    chunks:List[str]=[]

    full_text=" ".join(pages)
    text_length=len(full_text)

    if text_length ==0:
        return chunks
    
    start =0
    while start < text_length:
        end=min(start+chunk_size,text_length)

        chunk=full_text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start =end - chunk_overlap

    return chunks

