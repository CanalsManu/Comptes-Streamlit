import streamlit as st
import os

homepage = st.Page(os.path.join(os.getcwd(), 'front', 'homepage.py'),
                   default=True)
database = st.Page(os.path.join(os.getcwd(), 'front', 'database.py'))
cla_tree = st.Page(os.path.join(os.getcwd(), 'front', 'classification_tree.py'))
analysis = st.Page(os.path.join(os.getcwd(), 'front', 'analysis.py'))
add_moves = st.Page(os.path.join(os.getcwd(), 'front', 'add_movements.py'))

pg = st.navigation([homepage, database, cla_tree, add_moves, analysis],
                   position='sidebar')

if 'assigned_at_refresh' in st.session_state:
    pg.run()
else:  # Refreshed, assign flag and run homepage
    st.session_state['assigned_at_refresh'] = True
    st.switch_page(homepage)