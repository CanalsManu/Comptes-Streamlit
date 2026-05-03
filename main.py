import streamlit as st
import pandas as pd
import os

homepage = st.Page(os.path.join(os.getcwd(), 'front', 'homepage.py'),
                   default=True)
database = st.Page(os.path.join(os.getcwd(), 'front', 'database.py'))
cla_tree = st.Page(os.path.join(os.getcwd(), 'front', 'classification_tree.py'))
analysis = st.Page(os.path.join(os.getcwd(), 'front', 'analysis.py'))
add_moves = st.Page(os.path.join(os.getcwd(), 'front', 'add_movements.py'))

pg = st.navigation([homepage, database, cla_tree, add_moves, analysis])
pg.run() 