# URL-Normalizer

This Streamlit app returns an array table with normalized URLs based on the provided XLSX or CSV file.

## Requirements
Ensure your file includes as the only header:

<li> 
  URL
</li>

## Features
Leverages the Python-based <a href="https://github.com/adbar/courlan" target="_blank" rel="noopener">Courlan</a> library for NLP normalization.
Refer to the main repository to get more from this library designed to ease your efforts with data cleaning
<ul>
  1. Removes ID session attributes
</ul>
<ul>
  2. Removes UTM parameters
</ul>
<ul>
  3. Removes hashbangs (fragments)
</ul>

## Use Cases

Mapping out canonical URLs to hand over to developers for implementation.

## Useful Links

1. You can access the app <a href="https://url-normalizer.streamlit.app/" target="_blank" rel="noopener">here</a>
2. Find more at my <a href="https://seodepths.com/tools-for-seo/" target="_blank" rel="noopener">SEO Toolstation</a>
