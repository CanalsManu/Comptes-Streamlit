import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader('Puja el teu fitxer de comptes si us plau', type=('csv'))

if uploaded_file is not None:
    st.write('File uploaded.')
    df = pd.read_csv(uploaded_file)
    columns = df.columns.tolist()

    st.header('Show data')
    st.write(df[[col for col in columns if col!= 'Classificació']])

    st.header('Show classification tree')
    st.write(df['Classificació'])
else:
    st.write('Waiting on file upload...')