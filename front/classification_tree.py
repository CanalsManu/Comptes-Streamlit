import streamlit as st

db = st.session_state.get('db', None)

if db is not None:

    st.header('Show classification tree')
    st.write(db['Classificació'])
    
else:
    st.write('No file uploaded.')
