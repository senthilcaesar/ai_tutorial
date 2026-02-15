# 🎯 Invoice Extractor UI - Quick Start Guide

## What is This?

A **professional web-based UI** for extracting invoice data using AI. Upload a PDF invoice, and watch as the application automatically extracts all important information and generates a human-readable summary.

**Built with:** Streamlit (industry best practice for data apps) + LangChain + LLaMA 3.1 AI

---

## Features

✨ **User-Friendly Interface**

- Beautiful, responsive design
- Real-time progress indicators
- Animated extraction status

📤 **Easy Upload**

- Drag-and-drop PDF upload
- File validation
- Support for multi-page invoices

🤖 **AI-Powered Extraction**

- Extracts 15+ data fields
- Generates human-readable summary
- Shows extraction progress step-by-step

💾 **Multiple Export Formats**

- Download data as JSON
- Download data as CSV
- Copy data directly

---

## Prerequisites

### Step 1: Install Python (if not already installed)

Download from [python.org](https://www.python.org/)

### Step 2: Ensure Ollama is Running

Make sure you have Ollama installed and LLaMA 3.1 model ready:

```bash
# Install Ollama from https://ollama.ai

# Download LLaMA 3.1 model
ollama pull llama3.1

# Start Ollama server (keep this running in another terminal)
ollama serve
```

---

## Installation

### Step 1: Navigate to Project Folder

```bash
cd /Users/senthilpalanivelu/AI/llama
```

### Step 2: Create Virtual Environment (Recommended)

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Step 1: Ensure Ollama is Running

In a **separate terminal**, run:

```bash
ollama serve
```

**Keep this running while you use the app!**

### Step 2: Start the Streamlit App

```bash
streamlit run streamlit_app.py
```

### Step 3: Open in Browser

The app will automatically open at:

```
http://localhost:8501
```

If it doesn't open automatically, copy-paste the URL into your browser.

---

## How to Use the Application

### Step 1: Upload Invoice

1. Click on "Browse files" button
2. Select your PDF invoice
3. Wait for file to upload (green checkmark will appear)

### Step 2: Extract Data

1. Click "🚀 Extract Invoice Data" button
2. Watch the animated progress as the AI processes:
   - 📂 Loading PDF file
   - 📄 Extracting text from invoice
   - 🔍 Sending to AI for processing
   - ⚙️ Parsing structured data
   - ✍️ Generating summary
   - ✅ Extraction complete

### Step 3: Review Results

Three tabs show different views:

- **📝 Summary Tab**: Clean, readable summary of the invoice
- **📊 Extracted Data Tab**: All extracted fields with values
- **💾 Download Tab**: Export options

### Step 4: Download Results

- Click "📥 Download as JSON" to get structured data
- Click "📥 Download as CSV" to get spreadsheet-friendly format

### Step 5: Extract Another Invoice

Click "🔄 Clear Results & Start Over" to process a new invoice

---

## Data Extracted

The application extracts the following information:

| Field                      | Description                                  |
| -------------------------- | -------------------------------------------- |
| **Shipping Address**       | Complete address where package was shipped   |
| **Place of Delivery**      | Specific delivery location                   |
| **Order Number**           | Unique order identifier                      |
| **Invoice Number**         | Unique invoice identifier                    |
| **Order Date**             | When order was placed                        |
| **Quantity**               | Number of items ordered                      |
| **Items**                  | Product descriptions and details             |
| **ASIN**                   | Amazon Standard Identification Number        |
| **SKU**                    | Stock Keeping Unit (seller's product ID)     |
| **HSN**                    | Harmonized System of Nomenclature (tax code) |
| **Total Amount**           | Total price paid                             |
| **Payment Mode**           | How payment was made                         |
| **Payment Transaction ID** | Unique payment identifier                    |
| **Payment Date & Time**    | When payment was processed                   |
| **Reverse Charge**         | Tax information                              |

---

## Understanding the UI Components

### Main Interface

- **Left Panel**: File upload and instructions
- **Right Panel**: Quick feature information
- **Sidebar**: About section and extracted fields list

### Extraction Progress

During extraction, you'll see animated status messages showing:

- Which step is currently being processed
- Real-time progress through the pipeline

### Results View (Tabbed Interface)

**Tab 1: Summary**

- Human-readable paragraph summary
- Easy to understand at a glance
- Perfect for presentations

**Tab 2: Extracted Data**

- All fields displayed clearly
- Column layout for easy scanning
- Raw JSON view for technical users

**Tab 3: Download**

- Download extracted data as JSON
- Export to CSV for Excel/Sheets
- Ready for further processing

---

## Troubleshooting

### Problem: "Connection refused" error

**Solution:** Make sure Ollama is running

```bash
# In a separate terminal:
ollama serve
```

### Problem: "Model 'llama3.1' not found"

**Solution:** Download the model first

```bash
ollama pull llama3.1
```

### Problem: Application won't start

**Solution:** Check all dependencies are installed

```bash
pip install -r requirements.txt
```

### Problem: Upload doesn't work

**Solution:**

1. Make sure file is a PDF
2. Try a different PDF
3. Check file size (should be reasonable)

### Problem: Extraction takes too long

**Solution:** This is normal for the first run. Subsequent runs will be faster.

### Problem: AI response is empty or incorrect

**Solution:**

1. Verify the PDF actually contains the invoice data
2. Try extracting from a different invoice
3. Check that Ollama model loaded correctly

---

## Performance Tips

### Fast Extraction

- Use single-page invoices when possible
- Ensure good internet connection to Ollama
- Close other applications to free up memory

### Better Results

- Use clear, readable invoices
- Ensure PDF text is selectable (not scanned images)
- Test with a known good invoice first

---

## Advanced: Customization

### Change PDF Page

To extract from a different page, find this line in `streamlit_app.py`:

```python
page_text = documents[1].page_content.strip()
```

Change the number:

- `documents[0]` = First page
- `documents[1]` = Second page (current)
- `documents[2]` = Third page

### Change AI Model

To use a different model, modify the code:

```python
llm = ChatOllama(model="mistral", temperature=0)  # Use Mistral instead
```

Available models (run `ollama list` to see all):

- `llama3.1` (recommended for invoices)
- `mistral` (faster but less accurate)
- `neural-chat` (good balance)

### Adjust Extraction Details

Modify schema descriptions in `streamlit_app.py` to customize what gets extracted.

---

## Deployment

### Run on Different Machine

1. Install dependencies on the new machine
2. Ensure Ollama is running there
3. Run the same command:

```bash
streamlit run streamlit_app.py
```

### Share with Others on Same Network

After starting Streamlit, you can share the URL shown in terminal with others on your network.

---

## Support

If you encounter issues:

1. **Check error messages** - They usually tell you what's wrong
2. **Verify Ollama is running** - Most common issue
3. **Try with a different PDF** - The issue might be with the invoice
4. **Check terminal output** - Streamlit shows detailed logs

---

## What Happens to My Data?

✅ **Your data is completely safe:**

- All processing happens on your local computer
- PDFs are never sent to external servers
- Data is not stored permanently
- Temp files are deleted after processing

---

## Next Steps

1. **Test with your invoices** using the web UI
2. **Export data** and integrate into your workflow
3. **Automate bulk processing** by running the command-line version
4. **Customize extraction fields** for your specific needs

---

## Questions or Issues?

Refer back to the troubleshooting section or check the inline help in the application!

**Happy extracting! 🚀**
