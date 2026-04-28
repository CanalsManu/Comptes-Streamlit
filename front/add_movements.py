import streamlit as st
import pandas as pd
from back.new_movements_readers import (
    read_xml_to_df,
    compare_movements,
    manage_controversial_movements,
    add_controversial_to_new
)
from back.classify_movements_dialog import classify_movements

db = st.session_state.get('db', False)

if db is False:
    st.write("Falta el fitxer de comptes, ves a Inici i puja'l.")
    st.stop()

uploaded_file = st.file_uploader('Puja els nous moviments a classificar.', type=('xml'))
if uploaded_file is None:
    st.stop()

uploaded_movements = read_xml_to_df(uploaded_file)
new, repeated, controversial = compare_movements(uploaded_movements, db)
manage_controversial = st.session_state.get(
    'manage_controversial', not controversial.empty
)

if manage_controversial:
    manage_controversial_movements(controversial)

if 'controversial_select' in st.session_state:
    newnew = add_controversial_to_new(new, st.session_state['controversial_select'])

st.write('newnew')
st.write(newnew)
st.write('new')
st.write(new)
st.write('repeated')
st.write(repeated)
st.write('controversial')
st.write(controversial)

if st.button('Classifica'):
    classify_movements()

if st.toggle('Mostra els nous moviments.'):
    st.write(uploaded_movements)