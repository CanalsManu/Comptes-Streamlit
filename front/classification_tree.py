import streamlit as st

db = st.session_state.get('db', None)

if db is not None:

    st.header('Show classification tree')
    st.write(st.session_state['clsf_tree'])
    
else:
    st.write('No file uploaded.')
