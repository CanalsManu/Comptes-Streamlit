import streamlit as st
import os
from back.save_progress_to_file import gather_comptes_in_df
from back.format import get_start_end_of_series
ss = st.session_state

with st.sidebar:
    # Navigation
    homepage = st.Page(os.path.join(os.getcwd(), 'front', 'homepage.py'),
                    default=True, title='Inici')
    database = st.Page(os.path.join(os.getcwd(), 'front', 'database.py'),
                    title='Base de dades')
    cla_tree = st.Page(os.path.join(os.getcwd(), 'front', 'classification_tree.py'),
                    title='Esquema de classificació')
    analysis = st.Page(os.path.join(os.getcwd(), 'front', 'analysis.py'),
                    title='Anàlisi')
    add_moves = st.Page(os.path.join(os.getcwd(), 'front', 'add_movements.py'),
                        title='Afegir moviments')

    pg = st.navigation([homepage, database, cla_tree, add_moves, analysis],
                    position='sidebar')
    
    # Download
    with st.sidebar.container(key="sidebar_bottom"):
        if 'db' in ss:
            data = gather_comptes_in_df()
            start_date, end_date = get_start_end_of_series(ss['db']['Data'])
            file_name = 'comptes_del_{}_al_{}.csv'.format(
                start_date.replace('/', '-'),
                end_date.replace('/', '-')
            )
        else:
            data = ''
            file_name = 'comptes_(buits).csv'
        
        st.download_button('Descarrega els comptes',
                           data=data,
                           file_name=file_name,
                           type='primary',
                           icon=':material/download:')

    st.html("""
    <style>
        .st-key-sidebar_bottom {
            position: absolute;
            bottom: 20px;
        }
    </style>
    """)


if 'assigned_at_refresh' in ss:
    pg.run()
else:  # Refreshed, assign flag and run homepage
    ss['assigned_at_refresh'] = True
    st.switch_page(homepage)