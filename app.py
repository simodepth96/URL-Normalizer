import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from courlan import normalize_url

# Function to remove values after '&post='
def remove_post_value(url):
    return url.split('&post=')[0]

# Streamlit app
def main():
    st.title("URL Normalizer")

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

        # Display the normalized URLs
        st.write("Normalized URLs:")
        st.dataframe(df[['URL', 'Normalized_URL']])

        # Download button for normalized data
        st.markdown(get_binary_file_downloader_html(df), unsafe_allow_html=True)

# Function to create a download link for the DataFrame
def get_binary_file_downloader_html(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # B64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="normalized_urls.csv">Download Normalized URLs</a>'
    return href

if __name__ == "__main__":
    main()
