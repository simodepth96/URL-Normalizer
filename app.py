import streamlit as st
import pandas as pd
import numpy as np
import base64
from courlan import normalize_url

# Function to remove values after '&post='
def remove_post_value(url):
    return url.split('&post=')[0]

# Streamlit app
def main():
    st.title("URL Normalizer")

    # Introduction
    st.markdown("""
    This Streamlit app returns an array table with normalized URLs based on the provided **XLSX** or **CSV** file.\n
    Ensure your file includes as the only header: \n
    **'URL'**\n
    **Features**:\n
    1. Removes ID session attributes \n
    2. Removes UTM parameters \n
    3. Removes hashbangs (fragments)\n
    **Use Cases** \n
    Mapping out canonical URLs to hand over to developers for implementation.
    """)

    # Upload file
    uploaded_file = st.file_uploader("Upload XLSX or CSV file", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Read the file
        try:
            if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading the file: {e}")
            return

        # Normalize URLs and create a new column with normalized URLs
        df['Normalized_URL'] = df['URL'].apply(lambda url: normalize_url(url, strict=True))

        # Apply the function to remove values after '&post='
        df['Normalized_URL'] = df['Normalized_URL'].apply(remove_post_value)

        # Display the full array as a preview
        st.write("Preview of the Data:")
        st.dataframe(df[['URL', 'Normalized_URL']])

        # Download button for normalized data
        st.markdown(get_binary_file_downloader_html(df), unsafe_allow_html=True)

def get_binary_file_downloader_html(df, file_type='csv'):
    if file_type == 'csv':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        filename = 'normalized_urls.csv'
    elif file_type == 'xlsx':
        excel_writer = pd.ExcelWriter('dummy.xlsx', engine='xlsxwriter')
        df.to_excel(excel_writer, index=False)
        excel_writer.save()
        with open('dummy.xlsx', 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        filename = 'normalized_urls.xlsx'

    href = f'<a href="data:file/{file_type};base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

if __name__ == "__main__":
    main()
