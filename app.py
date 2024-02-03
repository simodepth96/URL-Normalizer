import streamlit as st
import pandas as pd
from datetime import datetime
import base64

def generate_hreflang_sitemap(df, use_both):
    # Define sitemap header and footer
    sitemap_header = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    sitemap_footer = '</urlset>'

    # Save output to a single XML file
    output_file_path = 'hreflang_sitemap.xml'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_header)

        # Process each row and append to the same file
        for _, row in df.iterrows():
            today_date = datetime.today().strftime('%Y-%m-%d')
            f.write(f'<url>\n  <loc>{row["URL"]}</loc>\n')

            # Add xhtml:link elements
            for _, link_row in df.iterrows():
                if use_both:
                    alternate_value = f'{link_row["Language"]}-{link_row["Region"]}' if link_row["Language"] != "none" and link_row["Region"] != "none" else "x-default"
                else:
                    alternate_value = link_row["Language"] if link_row["Language"] != "none" else link_row["Region"]

                f.write(f'  <xhtml:link rel="alternate" hreflang="{alternate_value}" href="{link_row["URL"]}"/>\n')

            f.write(f'  <xhtml:link rel="alternate" hreflang="x-default" href="{row["X-Default"]}"/>\n  <lastmod>{today_date}</lastmod>\n</url>\n')

        f.write(sitemap_footer)

    st.success("hreflang XML sitemap generated successfully.")
    return output_file_path

# Streamlit UI
st.title("Hreflang XML Sitemap Generator")

# Introduction
st.markdown("""
This Streamlit app returns an array table with normalized URLs based on the provided **XLSX** or **CSV** file.\n
Ensure your file includes: \n
**'URL'** as the main header\n
**Features**:\n
1. Removes ID session attributes \n
2. Removes UTM parameters \n
3. Removes hashbangs (fragments)\n
**Use Cases** \n
Mapping out canonical URLs to provide to developers for implementation.
""")

# File upload
file = st.file_uploader("Upload XLSX or CSV file", type=["xlsx", "csv"])

if file is not None:
    st.write("File Uploaded Successfully!")

    # Read the file content
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    # Display file content
    st.dataframe(df)

    # Ask user choice
    use_both = st.radio("Do you want to use both Language and Region?", options=["Yes", "No"]) == "Yes"

    # Generate hreflang sitemap on button click
    if st.button("Generate Hreflang Sitemap"):
        output_file_path = generate_hreflang_sitemap(df, use_both)

        # Download link for XML
        st.markdown("### Download XML Sitemap")
        st.markdown(f"Click the link below to download the generated hreflang XML sitemap.")

        # Generate a download link
        with open(output_file_path, 'rb') as f:
            st.markdown(f'<a href="data:application/xml;base64,{base64.b64encode(f.read()).decode()}" download="hreflang_sitemap.xml">Download hreflang_sitemap.xml</a>', unsafe_allow_html=True)
