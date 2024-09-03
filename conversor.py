import streamlit as st
import pandas as pd
import json
import os
from PIL import Image
import io
import base64
import PyPDF2


# Função para detectar o formato do arquivo
def detectar_formato(file):
    if file.name.endswith('.csv'):
        return 'CSV'
    elif file.name.endswith('.xlsx'):
        return 'Excel'
    elif file.name.endswith('.json'):
        return 'JSON'
    elif file.name.endswith('.txt'):
        return 'TXT'
    elif file.name.endswith(('.png', '.jpg', '.jpeg')):
        return 'Imagem'
    elif file.name.endswith('.pdf'):
        return 'PDF'
    else:
        return 'Formato desconhecido'

# Função para converter CSV para Excel
def converter_csv_para_excel(file):
    df = pd.read_csv(file)
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)
    return excel_buffer.getvalue()

# Função para converter Excel para CSV
def converter_excel_para_csv(file):
    df = pd.read_excel(file)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()


# Função para converter JSON para CSV
def converter_json_para_csv(file):
    data = json.load(file)
    df = pd.json_normalize(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

# Função para converter CSV para JSON
def converter_csv_para_json(file):
    df = pd.read_csv(file)
    return df.to_json(orient='records')

# Função para converter imagem para PDF
def converter_imagem_para_pdf(file):
    img = Image.open(file)
    pdf_buffer = io.BytesIO()
    img.save(pdf_buffer, format='PDF')
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# Função para converter PDF para TXT
def converter_pdf_para_txt(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Função para converter TXT para CSV (assumindo que o TXT tem um formato tabular, como valores separados por vírgulas)
def converter_txt_para_csv(file):
    df = pd.read_csv(file, delimiter='\t')  # Ou delimiter=',' se for CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()


# Função para converter TXT para JSON
def converter_txt_para_json(file):
    df = pd.read_csv(file, delimiter='\t')  # Ou delimiter=',' se for CSV
    return df.to_json(orient='records')

# Função para converter TXT para Excel
def converter_txt_para_excel(file):
    df = pd.read_csv(file, delimiter='\t')  # Ou delimiter=',' se for CSV
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)
    return excel_buffer.getvalue()

# Interface do Streamlit
st.title('Conversor de Arquivos')

# Upload do arquivo
uploaded_file = st.file_uploader("Carregue o arquivo para conversão", type=['csv', 'xlsx', 'json', 'txt', 'png', 'jpg', 'jpeg', 'pdf'])

if uploaded_file is not None:
    formato = detectar_formato(uploaded_file)

    st.write(f"Formato detectado: **{formato}**")

    if formato == 'CSV':
        option = st.selectbox("Converter para:", ["Excel", "JSON"])
        if option == 'Excel':
            excel_data = converter_csv_para_excel(uploaded_file)
            st.download_button(label="Baixar Excel", data=excel_data, file_name='converted.xlsx')
        elif option == 'JSON':
            json_data = converter_csv_para_json(uploaded_file)
            st.download_button(label="Baixar JSON", data=json_data, file_name='converted.json')

    elif formato == 'Excel':
        option = st.selectbox("Converter para:", ["CSV"])
        if option == 'CSV':
            csv_data = converter_excel_para_csv(uploaded_file)
            st.download_button(label="Baixar CSV", data=csv_data, file_name='converted.csv')

    elif formato == 'JSON':
        option = st.selectbox("Converter para:", ["CSV"])
        if option == 'CSV':
            csv_data = converter_json_para_csv(uploaded_file)
            st.download_button(label="Baixar CSV", data=csv_data, file_name='converted.csv')

    elif formato == 'Imagem':
        option = st.selectbox("Converter para:", ["PDF"])
        if option == 'PDF':
            pdf_data = converter_imagem_para_pdf(uploaded_file)
            st.download_button(label="Baixar PDF", data=pdf_data, file_name='converted.pdf')

    elif formato == 'PDF':
        option = st.selectbox("Converter para:", ["TXT"])
        if option == 'TXT':
            txt_data = converter_pdf_para_txt(uploaded_file)
            st.download_button(label="Baixar TXT", data=txt_data, file_name='converted.txt')

    elif formato == 'TXT':
        option = st.selectbox("Converter para:", ["CSV", "JSON", "Excel"])
        if option == 'CSV':
            csv_data = converter_txt_para_csv(uploaded_file)
            st.download_button(label="Baixar CSV", data=csv_data, file_name='converted.csv')
        elif option == 'JSON':
            json_data = converter_txt_para_json(uploaded_file)
            st.download_button(label="Baixar JSON", data=json_data, file_name='converted.json')
        elif option == 'Excel':
            excel_data = converter_txt_para_excel(uploaded_file)
            st.download_button(label="Baixar Excel", data=excel_data, file_name='converted.xlsx')

    else:
        st.error("Formato de arquivo não suportado ou ainda não implementado.")