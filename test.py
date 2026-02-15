import os
import json
import re
import csv
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama


def clean_llm_json(raw_output: str):
    """
    Cleans LLM response if wrapped in markdown or extra text.
    """
    cleaned = re.sub(r"```json|```", "", raw_output).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        return match.group(0)
    return cleaned


def main():
    pdf_path = os.path.expanduser("~/Desktop/amazon_invoice/118.pdf")
    output_csv = "invoice_output.csv"

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    if len(documents) < 2:
        raise ValueError("PDF does not contain a second page.")

    page_text = documents[1].page_content.strip()

    # Initialize Ollama
    llm = ChatOllama(model="llama3.1", temperature=0)

    prompt = f"""
    Extract the following invoice fields.

    Return ONLY valid JSON with this exact structure:

    {{
        "Shipping Address": {{
            "Name": "",
            "Address": "",
            "State Code": ""
        }},
        "Place of delivery": "",
        "Payment Details": {{
            "Reverse Charge": "",
            "Payment Transaction ID": "",
            "Date & Time": "",
            "Mode of Payment": ""
        }},
        "Total Amount": "",
        "Order and Invoice Information": {{
            "Order Number": "",
            "Invoice Number": "",
            "Order Date": "",
            "Invoice Date": "",
            "Invoice ID": ""
        }},
        "Items": [
            {{
                "Description": "",
                "Unit Price": "",
                "Quantity": ""
            }}
        ]
    }}

    Invoice Page:
    {page_text}
    """

    response = llm.invoke(prompt)

    cleaned_json = clean_llm_json(response.content)

    try:
        data = json.loads(cleaned_json)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse JSON. Raw output:\n")
        print(response.content)
        return

    # Flatten data for CSV
    row = {
        "Shipping Name": data["Shipping Address"]["Name"],
        "Shipping Address": data["Shipping Address"]["Address"],
        "State Code": data["Shipping Address"]["State Code"],
        "Place of delivery": data["Place of delivery"],
        "Reverse Charge": data["Payment Details"]["Reverse Charge"],
        "Payment Transaction ID": data["Payment Details"]["Payment Transaction ID"],
        "Payment Date & Time": data["Payment Details"]["Date & Time"],
        "Mode of Payment": data["Payment Details"]["Mode of Payment"],
        "Total Amount": data["Total Amount"],
        "Order Number": data["Order and Invoice Information"]["Order Number"],
        "Invoice Number": data["Order and Invoice Information"]["Invoice Number"],
        "Order Date": data["Order and Invoice Information"]["Order Date"],
        "Invoice Date": data["Order and Invoice Information"]["Invoice Date"],
        "Invoice ID": data["Order and Invoice Information"]["Invoice ID"]
    }

    # Write items separately (one row per item)
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = list(row.keys()) + ["Description", "Unit Price", "Quantity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for item in data["Items"]:
            item_row = row.copy()
            item_row["Description"] = item["Description"]
            item_row["Unit Price"] = item["Unit Price"]
            item_row["Quantity"] = item["Quantity"]
            writer.writerow(item_row)

    print(f"\n✅ Invoice data written to {output_csv}")


if __name__ == "__main__":
    main()

