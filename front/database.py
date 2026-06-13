import streamlit as st

db = st.session_state.get('db', None)

if db is not None:

    st.header('Mostra la base de dades')
    columns = db.columns.tolist()
    st.dataframe(db[[col for col in columns if col!= 'Classificació']],
                 hide_index=True)

else:
    st.write('No file uploaded.')