import os
import json
import re
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_ollama import ChatOllama
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser


# Define ResponseSchemas for invoice extraction
shipping_address_schema = ResponseSchema(
    name="shipping_address",
    description="Shipping address details including Name, \
    Address, and State Code"
)

delivery_schema = ResponseSchema(
    name="place_of_delivery",
    description="Place of delivery for the order"
)

reverse_charge_schema = ResponseSchema(
    name="reverse_charge",
    description="Reverse charge applicable (Yes/No)"
)

payment_transaction_id_schema = ResponseSchema(
    name="payment_transaction_id",
    description="Payment transaction ID"
)

payment_datetime_schema = ResponseSchema(
    name="payment_datetime",
    description="Date and time of payment"
)

payment_mode_schema = ResponseSchema(
    name="payment_mode",
    description="Mode of payment used"
)

total_amount_schema = ResponseSchema(
    name="total_amount",
    description="Total amount charged"
)

order_number_schema = ResponseSchema(
    name="order_number",
    description="Order number from the invoice"
)

invoice_number_schema = ResponseSchema(
    name="invoice_number",
    description="Invoice number"
)

order_date_schema = ResponseSchema(
    name="order_date",
    description="Order date"
)

quantity_schema = ResponseSchema(
    name="quantity",
    description="Qty (Quantity) - the numeric quantity per item \
    from the items table, typically found in a Qty column"
)

asin_schema = ResponseSchema(
    name="asin",
    description="ASIN (Amazon Standard Identification Number) - \
    Extract the 10-character alphanumeric code that appears after the last pipe | character. \
    Example: B0FZTX33DW"
)

sku_schema = ResponseSchema(
    name="sku",
    description="SKU (Stock Keeping Unit) - Extract the alphanumeric code \
    that appears inside parentheses ( ) after the ASIN. \
    Example: NM-8PYA-4Y4G"
)

hsn_schema = ResponseSchema(
    name="hsn",
    description="HSN (Harmonized System of Nomenclature) code - \
    Extract the numeric code that appears after 'HSN:' in the item details. \
    Example: 10063010"
)

items_schema = ResponseSchema(
    name="items",
    description="List of purchased item descriptions - extract \
    only the strings BEFORE the pipe | character, which contains \
    the product name and details"
)

response_schemas = [
    shipping_address_schema,
    delivery_schema,
    reverse_charge_schema,
    payment_transaction_id_schema,
    payment_datetime_schema,
    payment_mode_schema,
    total_amount_schema,
    order_number_schema,
    invoice_number_schema,
    order_date_schema,
    quantity_schema,
    asin_schema,
    sku_schema,
    hsn_schema,
    items_schema
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)


def main():
    # Expand path properly
    pdf_path = os.path.expanduser("~/Desktop/amazon_invoice/118.pdf")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    # Load PDF with PDFPlumberLoader for better table extraction
    loader = PDFPlumberLoader(pdf_path)
    documents = loader.load()

    if len(documents) < 2:
        raise ValueError("PDF does not contain a second page.")

    # Extract only second page
    page_text = documents[1].page_content.strip()

    print("\n--- Extracting Invoice Fields ---\n")

    # Initialize Ollama LLM
    llm = ChatOllama(
        model="llama3.1",
        temperature=0
    )

    # Get formatting instructions from the output parser
    format_instructions = output_parser.get_format_instructions()

    # Structured extraction prompt
    prompt = f"""
    Extract the following invoice fields from the provided document.

    {format_instructions}

    Invoice Page:
    {page_text}
    """

    print("Prompt sent to LLM:\n")
    print(prompt)
    print("\n---\n")

    response = llm.invoke(prompt)

    try:
        # Parse structured output
        parsed = output_parser.parse(response.content)
        print(json.dumps(parsed, indent=4))
        
        # Generate summary based on extracted data
        print("\n--- Generating Summary ---\n")
        
        summary_prompt = f"""
        Based on the following extracted invoice data, write a clear and concise summary of the transaction in simple, plain English. 
        Write it as a single paragraph without bullet points or sections. Make it easy to understand for anyone.
        
        {json.dumps(parsed, indent=2)}
        """
        
        summary_response = llm.invoke(summary_prompt)
        
        print("Invoice Summary:\n")
        print(summary_response.content)
        
    except Exception as e:
        print(f"⚠️ Could not parse structured output: {e}\n")
        print("Raw LLM output below:\n")
        print(response.content)


if __name__ == "__main__":
    main()

