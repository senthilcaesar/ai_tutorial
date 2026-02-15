# 📄 Automated PDF Invoice Extraction Using AI - A Beginner's Guide

## Table of Contents

1. [What is This Project?](#what-is-this-project)
2. [The Problem We're Solving](#the-problem-were-solving)
3. [Key Technologies Explained](#key-technologies-explained)
4. [Setup Instructions](#setup-instructions)
5. [Code Walkthrough](#code-walkthrough)
6. [How to Run the Code](#how-to-run-the-code)
7. [Understanding the Output](#understanding-the-output)

---

## What is This Project?

Imagine you receive hundreds of PDF invoices from Amazon and need to extract specific information from each one - like order numbers, customer addresses, product names, and prices. **Manually** doing this would take forever!

This Python program **automatically reads PDF invoices and extracts structured data** using an AI model called LLaMA 3.1. Instead of reading the PDF and manually copying data, the AI reads the invoice and pulls out the information we ask for, then organizes it into a nice format we can use.

**What does it extract?**

- Shipping address (name, address, state)
- Order and invoice numbers
- Payment details (transaction ID, date, mode)
- Items purchased with descriptions
- Product identifiers (ASIN, SKU, HSN)
- Order dates and quantities

---

## The Problem We're Solving

### Without AI:

```
❌ Open each PDF manually
❌ Read through the invoice
❌ Copy shipping address to Excel
❌ Copy order number to Excel
❌ Copy each item to Excel
❌ Repeat 100+ times manually
⏰ Takes HOURS!
```

### With AI:

```
✅ Run one Python script
✅ AI reads all invoices
✅ Data automatically extracted
✅ Organized in JSON format
⏰ Takes SECONDS!
```

---

## Key Technologies Explained

### 1. **Python**

Python is a programming language. Think of it as giving instructions to a computer in English-like syntax.

### 2. **PDF Reading - PDFPlumberLoader**

```python
from langchain_community.document_loaders import PDFPlumberLoader
```

**What it does:** Reads PDF files and extracts text while **preserving the table structure**.

**Why PDFPlumberLoader?** It's better than regular PDF readers because:

- Keeps tables organized (rows and columns stay in order)
- Preserves spacing and formatting
- Great for invoice extraction where data is in tables

**Simple analogy:**

- Regular PDF reader = reads the words but mixes them up
- PDFPlumberLoader = reads the words AND keeps the table structure intact

### 3. **LangChain - The Orchestrator**

```python
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_ollama import ChatOllama
```

**What is LangChain?**
LangChain is a framework that makes it easy to work with AI models. Without it, working with AI would be complicated. LangChain handles:

- Communication with the AI model
- Structuring requests
- Parsing responses

**Why use LangChain?**

- Simplifies AI integration
- Handles data formatting automatically
- Makes code more reliable

### 4. **LLaMA 3.1 - The AI Brain**

```python
llm = ChatOllama(model="llama3.1", temperature=0)
```

**What is LLaMA?** LLaMA stands for "Large Language Model Meta AI". It's an AI trained to understand text and answer questions intelligently.

**What is `temperature=0`?**

- Temperature controls how "creative" the AI is
- `temperature=0` = AI gives consistent, factual answers (perfect for invoice extraction)
- `temperature=1` = AI is more creative (good for creative writing)

**Simple analogy:**

- High temperature = AI is a creative writer (unpredictable)
- Low temperature = AI is an accountant (precise and consistent)

### 5. **JSON - Organized Output**

```python
json.dumps(parsed, indent=4)
```

**What is JSON?**
JSON stands for "JavaScript Object Notation". It's a way to organize data that both humans and computers can read easily.

**Example:**

```json
{
  "order_number": "123-456-789",
  "shipping_address": "123 Main St, Springfield, IL",
  "total_amount": "$99.99"
}
```

---

## Understanding Schemas

**What is a Schema?**
A schema is like a **template** or **form** that tells the AI exactly what information to extract.

Think of it like this:

- Before: "Extract information from the invoice" (too vague, AI doesn't know what to extract)
- After: "Extract the order number, shipping address, and total amount" (clear instructions)

### How Schemas Work:

```python
shipping_address_schema = ResponseSchema(
    name="shipping_address",              # Name of the field
    description="Shipping address details including Name, Address, and State Code"
                                          # What to extract (detailed instructions for AI)
)
```

**Breaking it down:**

- `name="shipping_address"` = This is the field name in our output
- `description="..."` = Instructions for the AI on what exactly to extract

### Why Multiple Schemas?

We create 14 different schemas (one for each field):

```python
response_schemas = [
    shipping_address_schema,    # What is the shipping address?
    delivery_schema,            # Where is it being delivered?
    order_number_schema,        # What's the order number?
    quantity_schema,            # How many items?
    asin_schema,               # What's the ASIN (Amazon ID)?
    sku_schema,                # What's the SKU?
    hsn_schema,                # What's the HSN (tax code)?
    items_schema,              # What items were ordered?
    # ... and more
]
```

**Why?** This tells the AI: "I want you to extract THESE specific 14 pieces of information."

### Structured Output Parser

```python
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
```

**What does it do?**

- Takes all our schemas
- Creates a template for the AI to follow
- Automatically formats the AI's response into structured data

**Simple analogy:** It's like giving the AI a form to fill out instead of just asking "tell me about this invoice."

---

## Setup Instructions

### Step 1: Install Python

If you don't have Python installed, download it from [python.org](https://www.python.org/)

### Step 2: Create a Project Folder

```bash
mkdir invoice_extraction
cd invoice_extraction
```

### Step 3: Create a Virtual Environment (Recommended)

A virtual environment keeps your project's dependencies isolated.

```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Required Libraries

Copy and paste this in your terminal:

```bash
pip install langchain langchain-community langchain-ollama pdfplumber
```

**What are we installing?**

- `langchain` = Main LangChain framework
- `langchain-community` = Additional LangChain tools for PDF reading
- `langchain-ollama` = Connection to LLaMA AI
- `pdfplumber` = Smart PDF reading

### Step 5: Install and Run LLaMA Locally

You need to install Ollama to run LLaMA 3.1 on your computer:

1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Install it
3. Open terminal and run:

```bash
ollama pull llama3.1  # Downloads the LLaMA 3.1 model (first time takes ~5-10 min)
ollama serve         # Starts the AI server
```

**Keep `ollama serve` running in a separate terminal while you run the Python script!**

---

## Code Walkthrough

### Part 1: Import Libraries

```python
import os                          # For working with file paths
import json                        # For formatting output as JSON
import re                          # For text pattern matching
from langchain_community.document_loaders import PDFPlumberLoader
                                  # Smart PDF reader
from langchain_ollama import ChatOllama
                                  # Connect to LLaMA AI
from langchain.output_parsers import ResponseSchema
                                  # Create extraction templates
from langchain.output_parsers import StructuredOutputParser
                                  # Format AI output as structured data
```

### Part 2: Define Schemas (Lines 11-104)

```python
shipping_address_schema = ResponseSchema(
    name="shipping_address",
    description="Shipping address details including Name, Address, and State Code"
)
```

**What's happening:**

1. We create a schema called `shipping_address_schema`
2. We tell LangChain: "Look for a field called 'shipping_address'"
3. We give detailed instructions: "Include Name, Address, and State Code"

**This repeats 14 times** for each piece of information we want to extract.

### Part 3: Combine All Schemas

```python
response_schemas = [
    shipping_address_schema,
    delivery_schema,
    reverse_charge_schema,
    # ... 11 more schemas ...
    items_schema
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
```

**What's happening:**

1. We put all schemas in a list
2. We create an `output_parser` that knows about all these schemas
3. This parser will format the AI's response according to these schemas

### Part 4: Main Function - Load PDF

```python
def main():
    # Get the PDF file path
    pdf_path = os.path.expanduser("~/Desktop/amazon_invoice/118.pdf")

    # Check if file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    # Load the PDF
    loader = PDFPlumberLoader(pdf_path)
    documents = loader.load()
```

**What's happening:**

1. `pdf_path` = Location of our PDF file (in Desktop folder)
2. We check: "Does this file exist?" (error prevention)
3. `PDFPlumberLoader` reads the PDF
4. `documents` = List of pages from the PDF

### Part 5: Extract Second Page

```python
if len(documents) < 2:
    raise ValueError("PDF does not contain a second page.")

page_text = documents[1].page_content.strip()
```

**What's happening:**

1. We check: "Does the PDF have at least 2 pages?"
2. `documents[1]` = Get the 2nd page (remember: computers count from 0)
3. `.page_content` = Get the text from that page
4. `.strip()` = Remove extra spaces at the beginning/end

### Part 6: Initialize the AI

```python
llm = ChatOllama(
    model="llama3.1",    # Use LLaMA 3.1 model
    temperature=0        # Give consistent, factual answers
)
```

**What's happening:**

1. `llm` = Create a connection to LLaMA 3.1
2. We tell it to be precise (temperature=0)

### Part 7: Create the Prompt

```python
format_instructions = output_parser.get_format_instructions()

prompt = f"""
Extract the following invoice fields from the provided document.

{format_instructions}

Invoice Page:
{page_text}
"""
```

**What's happening:**

1. `format_instructions` = Instructions telling AI HOW to format the answer
2. We create a prompt (message to the AI) that includes:
   - What we want: "Extract invoice fields"
   - How to format it: (from the parser)
   - The actual invoice text: `{page_text}`

**Example of what gets sent to AI:**

````
Extract the following invoice fields from the provided document.

The output should be a markdown code snippet formatted in the following schema,
including the leading and trailing "```json" and "```":

```json
{
    "shipping_address": <string>,
    "order_number": <string>,
    "items": <string>,
    ...
}
````

Invoice Page:
[ALL THE INVOICE TEXT HERE]

````

### Part 8: Send to AI and Get Response
```python
response = llm.invoke(prompt)
````

**What's happening:**

1. We send the prompt to LLaMA 3.1
2. LLaMA reads the invoice and prompt
3. LLaMA generates a response with the extracted information
4. We store the response

### Part 9: Parse and Display Results

```python
try:
    parsed = output_parser.parse(response.content)
    print(json.dumps(parsed, indent=4))
except Exception as e:
    print(f"⚠️ Could not parse structured output: {e}\n")
    print("Raw LLM output below:\n")
    print(response.content)
```

**What's happening:**

1. `try:` = Try to parse the AI's response
2. `output_parser.parse()` = Convert AI's response into structured JSON
3. `json.dumps(..., indent=4)` = Format it nicely and print it
4. `except:` = If something goes wrong, show the raw output for debugging

---

## How to Run the Code

### Step 1: Set Up Your Invoice

```bash
# Make sure you have a PDF invoice at:
~/Desktop/amazon_invoice/118.pdf

# If your file is elsewhere, modify this line in the code:
pdf_path = os.path.expanduser("~/Desktop/amazon_invoice/118.pdf")
```

### Step 2: Open Terminal and Activate Virtual Environment

```bash
cd invoice_extraction
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Step 3: Make Sure Ollama is Running

In a **separate terminal**, run:

```bash
ollama serve
```

**Keep this running!** It's your AI server.

### Step 4: Run the Python Script

```bash
python test.py
```

### Step 5: Watch the Magic!

The script will:

1. Load the PDF
2. Extract the text
3. Send it to LLaMA 3.1
4. Parse the response
5. Print the extracted data as JSON

---

## Understanding the Output

### Raw Output from Code:

```json
{
  "shipping_address": "John Doe, 123 Main St, Springfield, IL 62701",
  "place_of_delivery": "123 Main St, Springfield, IL 62701",
  "order_number": "123-456-789",
  "invoice_number": "INV-2024-001",
  "order_date": "2024-02-10",
  "quantity": "1",
  "items": "Amudham Naturals Pesarattu Dosa Mix, Green Gram Dosa Instant Batter Mix, High Protein, Gluten-Free, 500g",
  "asin": "B0G44TN82N",
  "sku": "TL-FZ0S-DZYT",
  "hsn": "21069099",
  "total_amount": "$256.19",
  "payment_mode": "Credit Card",
  "payment_transaction_id": "TXN-123456789",
  "payment_datetime": "2024-02-10 14:30:00",
  "reverse_charge": "No"
}
```

### What Each Field Means:

| Field                    | Example                                      | Explanation                       |
| ------------------------ | -------------------------------------------- | --------------------------------- |
| `shipping_address`       | John Doe, 123 Main St, Springfield, IL 62701 | Where the package was shipped     |
| `order_number`           | 123-456-789                                  | Unique identifier for the order   |
| `invoice_number`         | INV-2024-001                                 | Unique identifier for the invoice |
| `items`                  | Amudham Naturals Pesarattu Dosa Mix...       | Product name and description      |
| `quantity`               | 1                                            | How many units ordered            |
| `asin`                   | B0G44TN82N                                   | Amazon's product identifier       |
| `sku`                    | TL-FZ0S-DZYT                                 | Seller's product identifier       |
| `hsn`                    | 21069099                                     | Tax classification code           |
| `total_amount`           | $256.19                                      | Total price paid                  |
| `payment_mode`           | Credit Card                                  | How payment was made              |
| `payment_transaction_id` | TXN-123456789                                | Unique payment transaction code   |
| `payment_datetime`       | 2024-02-10 14:30:00                          | When payment was processed        |
| `reverse_charge`         | No                                           | Tax information                   |

---

## Troubleshooting

### Problem: "PDF not found"

**Solution:** Check that your PDF file path is correct in the code

```python
pdf_path = os.path.expanduser("~/Desktop/amazon_invoice/118.pdf")
```

### Problem: "ModuleNotFoundError: No module named 'langchain'"

**Solution:** Make sure you installed dependencies and activated virtual environment

```bash
pip install langchain langchain-community langchain-ollama pdfplumber
```

### Problem: "Connection refused" error

**Solution:** Ollama server is not running. In a separate terminal:

```bash
ollama serve
```

### Problem: AI response is empty or incorrect

**Possible solutions:**

1. Make sure the PDF actually contains the data you're looking for
2. Try a different invoice to test
3. The schema descriptions might need adjustment

---

## Extending This Code

### Want to extract from multiple PDFs?

```python
import os
pdf_folder = os.path.expanduser("~/Desktop/amazon_invoice/")
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        # Process each PDF
```

### Want to save results to CSV?

```python
import csv
with open("invoices.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=parsed.keys())
    writer.writerow(parsed)
```

### Want to use a different AI model?

```python
llm = ChatOllama(model="mistral", temperature=0)  # Try Mistral instead
```

---

## Summary

**What we learned:**

1. ✅ How to read PDFs using Python
2. ✅ What LangChain is and why it's useful
3. ✅ How AI models like LLaMA work
4. ✅ How to structure extracted data using schemas
5. ✅ How to automate information extraction

**Key Takeaway:** This code demonstrates how AI can automate tedious data extraction tasks, turning hours of manual work into seconds of automated processing!

---

## Questions?

Feel free to ask! This is a great foundation for:

- Processing business documents
- Automating data entry
- Building AI-powered applications
- Learning about LangChain and LLMs

**Happy coding! 🚀**
