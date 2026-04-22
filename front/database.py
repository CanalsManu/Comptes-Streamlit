import streamlit as st

db = st.session_state.get('db', None)

if db is not None:

    st.header('Show data')
    columns = db.columns.tolist()
    st.write(db[[col for col in columns if col!= 'Classificació']])

else:
    st.write('No file uploaded.')