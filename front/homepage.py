import streamlit as st
import pandas as pd

@st.dialog("Hola!", dismissible=False)
def init_dialog():
    uploaded_file = st.file_uploader('Puja el teu fitxer de comptes, si us plau', type=('csv'))

    if uploaded_file is not None:
        st.session_state['db'] = pd.read_csv(uploaded_file)
        st.rerun()

    if st.button("Close"):
        st.session_state['db'] = None
        st.rerun()

if 'db' not in st.session_state:
    init_dialog()
else:
    st.write(':)')
    st.write('session state')
    st.write(st.session_state)