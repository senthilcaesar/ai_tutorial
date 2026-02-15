import os
import re
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_ollama import ChatOllama

def main():
    pdf_path = os.path.expanduser("~/Desktop/amazon_invoice/118.pdf")

    loader = PDFPlumberLoader(pdf_path)
    documents = loader.load()

    if len(documents) < 2:
        raise ValueError("PDF does not contain a second page.")

    # Extract second page
    text = documents[1].page_content

    # Clean formatting
    text = re.sub(r'\n+', '\n', text)        # remove excessive newlines
    text = re.sub(r'[ \t]+', ' ', text)      # remove extra spaces
    text = text.strip()

    # LLM call
    llm = ChatOllama(model="llama3.1")

    response = llm.invoke(
        f"Format the following invoice page into a clean readable structure:\n\n{text}"
    )

    print("LLM Summary:\n")
    print(response.content)

if __name__ == "__main__":
    main()

