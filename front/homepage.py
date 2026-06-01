import streamlit as st
import pandas as pd
from back.classification_tree import (
    dashed_to_tree,
    check_clsf_tree
)
from back.known_movements import get_known_movements
ss = st.session_state

@st.dialog("Hola!", dismissible=False)
def init_dialog():
    uploaded_file = st.file_uploader('Puja el teu fitxer de comptes, si us plau', type=('csv'))

    if uploaded_file is not None:
        db = pd.read_csv(uploaded_file)
        known_movements = get_known_movements(db['Nom'], db['Categories'])

        clsf = db.pop('Classificació')
        clsf = clsf[~clsf.isnull()]  # removing nans from df

        ss['db'] = db
        ss['known_movements'] = known_movements
        ss['clsf_tree'] = dashed_to_tree(clsf)
        check_clsf_tree(ss['clsf_tree'])

        st.rerun()

    if st.button("Close"):
        ss['db'] = None
        st.rerun()

if 'db' not in ss:
    init_dialog()
else:
    st.write(':)')
    st.write('session state')
    st.write(ss)