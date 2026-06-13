import streamlit as st
import pandas as pd
from back.classification_tree import (
    dashed_to_tree,
    check_clsf_tree
)
from back.known_movements import get_known_movements
from back.fake_file_uploader import fake_file_uploader
from front.pages_format import (
    database_kwargs,
    cla_tree_kwargs,
    analysis_kwargs,
    add_moves_kwarg
)
ss = st.session_state

@st.dialog("Hola!", dismissible=False)
def init_dialog():
    uploaded_file = st.file_uploader('Puja el teu fitxer de comptes, si us plau', type=('csv'))

    if uploaded_file is not None:
        ss['uploaded_comptes_file'] = uploaded_file
        db = pd.read_csv(uploaded_file)
        known_movements = get_known_movements(db['Nom'], db['Categories'])

        clsf = db.pop('Classificació')
        clsf = clsf[~clsf.isnull()]  # removing nans from df

        ss['db'] = db
        ss['known_movements'] = known_movements
        ss['clsf_tree'] = dashed_to_tree(clsf)
        check_clsf_tree(ss['clsf_tree'])

        st.rerun()
        

if 'db' not in ss:
    init_dialog()
else:
    st.markdown(':small[:grey[Fitxer de comptes pujat correctament...]]')
    info_file_upload = 'Recarrega la página per canviar de fitxer.'
    fake_file_uploader(ss['uploaded_comptes_file'].name, 'test_key',
                       info_text=f':small[:gray[{info_file_upload}]]',
                       disabled=True)
    
    
    st.header('Gestiona els comptes', divider='grey')
    cols = st.columns(2)
    for index, page_kwargs in enumerate((database_kwargs, cla_tree_kwargs,
                                        add_moves_kwarg, analysis_kwargs)):
        col_id = index % 2
        if cols[col_id].button(page_kwargs['title'],
                            icon=page_kwargs['icon'],
                            type='primary',
                            width='stretch',
                            shortcut=str(index+1)
        ):
            st.switch_page(page_kwargs['page'])
        # st.page_link(page_kwargs['page'], icon=page_kwargs['icon'])
