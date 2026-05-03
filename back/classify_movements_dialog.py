import streamlit as st


def start_classification(movements):
    """First call to classify_movements. Setting defaults."""
    st.session_state['classification'] = {
        'status': 'in-progress',
        'results': [None] * movements.shape[0],
        'curr_idx': 0
    }
    classify_movements(movements)


@st.dialog('Classifica els nous moviments', width='medium')
def classify_movements(movements):
    """
    Dialog to classify movements.
    
    Show on a dialog name, date and import of a specific movement. Show buttons
    with possible categories, based on user classification (recursively if there
    are subcategories). Record answer. Upon submission, write to data base.

    Classification info will be held in session's 'classification', a dict with:
        - 'status': string, 'done' or 'in-progress'
        - 'results': list[tuple[str]], categories
        - 'curr_idx': int, current index 
    """
    # Get current values
    n = movements.shape[0]
    curr_idx = st.session_state['classification']['curr_idx']

    # Movement info
    if curr_idx >= n:
        st.write('end page.')
    else:
        move_cols = st.columns(2)

        with move_cols[0]:
            st.write(movements.iloc[curr_idx]['Data'])

        with move_cols[1]:
            st.write(movements.iloc[curr_idx]['Nom'])
            st.write(movements.iloc[curr_idx]['Import'])

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
    

    # Progress info
    st.progress(curr_idx/n)

    # Navigation buttons
    nav_cols = st.columns([1, 1])

    def _go_left():
        st.session_state['classification']['curr_idx'] -= 1 
    cont_left = nav_cols[0].container(horizontal_alignment='left')
    cont_left.button('<', disabled = (curr_idx <= 0), on_click = _go_left,
                      type='tertiary')

    def _go_right():
        st.session_state['classification']['curr_idx'] += 1 
    cont_right = nav_cols[1].container(horizontal_alignment='right')
    cont_right.button('>', disabled = (curr_idx  >= n), on_click = _go_right,
                      type='tertiary')

@st.dialog('Classificació feta.')
def show_classification():
    """Show classification"""
    st.write(st.session_state['classification']['result'])