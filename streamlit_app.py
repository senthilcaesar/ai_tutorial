import streamlit as st
import os
import json
import tempfile
import time
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_ollama import ChatOllama
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser


# Page configuration
st.set_page_config(
    page_title="Invoice Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77d4;
            margin-bottom: 1rem;
        }
        .status-box {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .info-box {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
    </style>
""", unsafe_allow_html=True)


# Define ResponseSchemas for invoice extraction
def get_response_schemas():
    return [
        ResponseSchema(
            name="shipping_address",
            description="Shipping address details including Name, Address, and State Code"
        ),
        ResponseSchema(
            name="place_of_delivery",
            description="Place of delivery for the order"
        ),
        ResponseSchema(
            name="reverse_charge",
            description="Reverse charge applicable (Yes/No)"
        ),
        ResponseSchema(
            name="payment_transaction_id",
            description="Payment transaction ID"
        ),
        ResponseSchema(
            name="payment_datetime",
            description="Date and time of payment"
        ),
        ResponseSchema(
            name="payment_mode",
            description="Mode of payment used"
        ),
        ResponseSchema(
            name="total_amount",
            description="Total amount charged"
        ),
        ResponseSchema(
            name="order_number",
            description="Order number from the invoice"
        ),
        ResponseSchema(
            name="invoice_number",
            description="Invoice number"
        ),
        ResponseSchema(
            name="order_date",
            description="Order date"
        ),
        ResponseSchema(
            name="quantity",
            description="Qty (Quantity) - the numeric quantity per item from the items table"
        ),
        ResponseSchema(
            name="asin",
            description="ASIN (Amazon Standard Identification Number) - Extract the 10-character alphanumeric code that appears after the last pipe | character. Example: B0FZTX33DW"
        ),
        ResponseSchema(
            name="sku",
            description="SKU (Stock Keeping Unit) - Extract the alphanumeric code that appears inside parentheses ( ) after the ASIN. Example: NM-8PYA-4Y4G"
        ),
        ResponseSchema(
            name="hsn",
            description="HSN (Harmonized System of Nomenclature) code - Extract the numeric code that appears after 'HSN:' in the item details. Example: 10063010"
        ),
        ResponseSchema(
            name="items",
            description="List of purchased item descriptions - extract only strings BEFORE the pipe | character"
        )
    ]


def extract_invoice_data(pdf_path):
    """Extract invoice data from PDF"""
    
    # Step 1: Load PDF
    status_placeholder = st.empty()
    progress_placeholder = st.empty()
    
    extraction_steps = [
        "📂 Loading PDF file...",
        "📄 Extracting text from invoice...",
        "🔍 Sending to AI for processing...",
        "⚙️ Parsing structured data...",
        "✍️ Generating summary...",
        "✅ Extraction complete!"
    ]
    
    try:
        # Step 1: Load PDF
        with status_placeholder.container():
            st.info(extraction_steps[0])
        time.sleep(0.5)
        
        loader = PDFPlumberLoader(pdf_path)
        documents = loader.load()
        
        if len(documents) < 2:
            st.error("❌ PDF does not contain a second page.")
            return None
        
        # Step 2: Extract text
        with status_placeholder.container():
            st.info(extraction_steps[1])
        time.sleep(0.5)
        
        page_text = documents[1].page_content.strip()
        
        # Step 3: Initialize LLM and prepare schemas
        with status_placeholder.container():
            st.info(extraction_steps[2])
        time.sleep(0.5)
        
        llm = ChatOllama(model="llama3.1", temperature=0)
        response_schemas = get_response_schemas()
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        
        format_instructions = output_parser.get_format_instructions()
        
        prompt = f"""
        Extract the following invoice fields from the provided document.

        {format_instructions}

        Invoice Page:
        {page_text}
        """
        
        response = llm.invoke(prompt)
        
        # Step 4: Parse structured output
        with status_placeholder.container():
            st.info(extraction_steps[3])
        time.sleep(0.5)
        
        parsed = output_parser.parse(response.content)
        
        # Step 5: Generate summary
        with status_placeholder.container():
            st.info(extraction_steps[4])
        time.sleep(0.5)
        
        summary_prompt = f"""
        Based on the following extracted invoice data, write a clear and concise summary of the transaction in simple, plain English. 
        Write it as a single paragraph without bullet points or sections. Make it easy to understand for anyone.
        
        {json.dumps(parsed, indent=2)}
        """
        
        summary_response = llm.invoke(summary_prompt)
        
        # Step 6: Complete
        with status_placeholder.container():
            st.success(extraction_steps[5])
        time.sleep(0.5)
        
        return {
            "extracted_data": parsed,
            "summary": summary_response.content
        }
        
    except Exception as e:
        st.error(f"❌ Error during extraction: {str(e)}")
        return None


# Main UI
st.markdown("<h1 class='main-header'>📄 Invoice Data Extractor</h1>", unsafe_allow_html=True)

st.markdown("""
This application uses AI to automatically extract information from Amazon invoices.
Simply upload your PDF invoice and watch as the AI extracts all the important details!
""")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    **Features:**
    - 📤 Upload PDF invoices
    - 🤖 AI-powered data extraction
    - 📊 Structured data output
    - 📝 Human-readable summary
    - 💾 Download results as JSON
    """)
    
    st.divider()
    
    st.header("Extracted Fields")
    st.markdown("""
    - Shipping Address
    - Order Number
    - Invoice Number
    - Order Date
    - Quantity
    - Items Description
    - ASIN (Amazon ID)
    - SKU
    - HSN Code
    - Total Amount
    - Payment Details
    - And More...
    """)


# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Invoice")
    
    uploaded_file = st.file_uploader("Choose a PDF invoice", type="pdf", key="pdf_uploader")
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        if st.button("🚀 Extract Invoice Data", use_container_width=True, type="primary"):
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_pdf_path = tmp_file.name
            
            try:
                with st.spinner("Processing..."):
                    result = extract_invoice_data(temp_pdf_path)
                
                if result:
                    st.session_state.extraction_result = result
                    st.rerun()
            finally:
                # Clean up temp file
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
    else:
        st.info("👆 Upload a PDF invoice to get started")


with col2:
    st.subheader("📋 Instructions")
    st.markdown("""
    1. **Click on "Browse files"** to select your invoice PDF
    2. **Wait for the upload** to complete
    3. **Click "Extract Invoice Data"** button
    4. **Watch the progress** as the AI extracts information
    5. **Review the results** in the sections below
    6. **Download JSON** for further processing
    """)


# Display results if available
if "extraction_result" in st.session_state:
    result = st.session_state.extraction_result
    
    st.divider()
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📝 Summary", "📊 Extracted Data", "💾 Download"])
    
    with tab1:
        st.subheader("Invoice Summary")
        st.markdown(f"""
        <div class='status-box success-box'>
        {result['summary']}
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Extracted Data (JSON Format)")
        
        extracted_data = result['extracted_data']
        
        # Convert extracted data to DataFrame for tabular display
        import pandas as pd
        
        # Create a list of dictionaries for the dataframe
        data_for_table = [
            {
                "Field": key.replace('_', ' ').title(),
                "Value": str(value)
            }
            for key, value in extracted_data.items()
        ]
        
        # Create and display dataframe
        df = pd.DataFrame(data_for_table)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Field": st.column_config.TextColumn(
                    "Field",
                    width="medium"
                ),
                "Value": st.column_config.TextColumn(
                    "Value",
                    width="large"
                )
            }
        )
        
        # Also show raw JSON
        with st.expander("📄 View Raw JSON"):
            st.json(extracted_data)
    
    with tab3:
        st.subheader("💾 Download Results")
        
        # Prepare download data
        download_data = {
            "extracted_fields": result['extracted_data'],
            "summary": result['summary'],
            "extraction_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        json_str = json.dumps(download_data, indent=2)
        
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name="invoice_extraction.json",
            mime="application/json",
            use_container_width=True
        )
        
        # Also offer CSV format for just the fields
        import csv
        import io
        
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Field", "Value"])
        for key, value in result['extracted_data'].items():
            writer.writerow([key, value])
        
        csv_str = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download as CSV",
            data=csv_str,
            file_name="invoice_extraction.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Reset button
    if st.button("🔄 Clear Results & Start Over", use_container_width=True):
        st.session_state.extraction_result = None
        st.rerun()


# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #888; margin-top: 2rem;'>
    <p>🤖 Powered by LLaMA 3.1 AI • Built with Streamlit</p>
    <p><small>Upload your invoices securely. Data is processed locally and not stored.</small></p>
    </div>
""", unsafe_allow_html=True)
