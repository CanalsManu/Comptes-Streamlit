import streamlit as st

@st.dialog('Classifica els nous moviments', dismissible=False)
def classify_movements():

    # Movement info
    move_cols = st.columns(3)

    with move_cols[0]:
        st.write('Data')

    with move_cols[1]:
        st.write('Nom')

    with move_cols[2]:
        st.write('Import')

    st.write('---')

    # Classification info
    classification_cols = st.columns(4)

    with classification_cols[0]:
        st.write('C1')

    with classification_cols[1]:
        st.write('C2')

    with classification_cols[2]:
        st.write('C3')

    with classification_cols[3]:
        st.write('C4')

    # Navigation info

    if st.button('Close'):
        st.rerun()