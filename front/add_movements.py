import streamlit as st
import pandas as pd
from back.new_movements_readers import read_xml_to_df, compare_movements
from back.classify_movements_dialog import classify_movements

db = st.session_state.get('db', False)

if db is False:
    st.write("Falta el fitxer de comptes, ves a Inici i puja'l.")
    st.stop()

uploaded_file = st.file_uploader('Puja els nous moviments a classificar.', type=('xml'))
if uploaded_file is None:
    st.stop()

uploaded_movements = read_xml_to_df(uploaded_file)
new_movements = compare_movements(uploaded_movements, db)

if st.button('Classifica'):
    classify_movements()

if st.toggle('Mostra els nous moviments.'):
    st.write(uploaded_movements)