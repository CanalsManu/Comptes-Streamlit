import streamlit as st
import pandas as pd
from back.classification_tree import (
    dashed_to_tree,
    check_clsf_tree
)

@st.dialog("Hola!", dismissible=False)
def init_dialog():
    uploaded_file = st.file_uploader('Puja el teu fitxer de comptes, si us plau', type=('csv'))

    if uploaded_file is not None:
        db = pd.read_csv(uploaded_file)
        clsf = db.pop('Classificació')

        st.session_state['db'] = db
        st.session_state['clsf_tree'] = dashed_to_tree(clsf[~clsf.isnull()])
        check_clsf_tree(st.session_state['clsf_tree'])

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