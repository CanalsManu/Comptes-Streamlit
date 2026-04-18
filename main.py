import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader('Upload your file please', type=('csv', 'py'))

if uploaded_file is not None:
    st.write('File uploaded.')
else:
    st.write('Waiting on file upload...')