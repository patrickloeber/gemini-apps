import json
import streamlit as st
from gemini_service import analyze_pdf, analyze_unhealthy_items, suggest_recipes


st.header("Gemini Supermarket Assistant")

st.markdown("""Upload a PDF with your supermarket invoice and Gemini will:
            
1. Extract invoice items
2. Flag potentially unhealthy items
3. Suggest a few recipes          
""")

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    with st.spinner("Extracting invoice items...", show_time=True):
        invoice_items = analyze_pdf(bytes_data)
    st.success("Extracting invoice items done!")
    st.text(json.dumps(invoice_items, indent=4))

    with st.spinner("Finding potentially unhealthy items...", show_time=True):
        text = analyze_unhealthy_items(invoice_items)
    st.success("Finding potentially unhealthy items done!")
    st.markdown(text)

    with st.spinner("Suggest recipes...", show_time=True):
        text = suggest_recipes(invoice_items)
    st.success("Generating recipe suggestions done!")
    st.markdown(text)





