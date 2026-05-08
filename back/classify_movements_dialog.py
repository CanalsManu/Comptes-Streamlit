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
    if 0 <= curr_idx <= n-1:
        curr_res = st.session_state['classification']['results'][curr_idx]
    else:
        curr_res = None

    # End page
    if curr_idx >= n:
        st.write('end page.')

    # Movement info
    else:
        curr_move = movements.iloc[curr_idx]
        _clsf_movement_info(curr_move)

        # Classification info
        _clsf_show_categories(curr_res, curr_move)
    
    # Progress info
    st.progress(curr_idx/n)

    # Navigation buttons
    _clsf_nav_buttons(curr_idx, n)

    return 


def _clsf_movement_info(curr_move):
    move_cols = st.columns(2)

    with move_cols[0]:
        st.write(curr_move['Data'])

    with move_cols[1]:
        st.write(curr_move['Nom'])
        st.write(curr_move['Import'])

    st.write('---')
    

def _clsf_show_categories(curr_res, curr_move):
    """
    Show possible categories from clasf tree and choose.
    
    - if curr_res is not None: highlight = True and show current choices?
    - see if import neg or pos
    - get corresponding categories
    - upon choosing, store result and show next subcategory
    - show current choices?
    - when no more category, show next movement

    Maybe I can do this:
    - if curr_res == None -> show initial cat based on import
        - then, choose category, e.g., cat1
        - if there are no subcategories
            - save curr_res = 'cat1'
            - go next
        - if there are subcategories
            - save curr_res = 'cat1-' (notice the dash)
    - elif curr_res end with '-' -> clasf in progress
        - show and choose subcategories based on curr_res, e.g., subcat2
        - if there are no more subcategories
            - save curr_res = 'cat1-subcat2'
            - go next
        - if there are more subcategories
            - save curr_res = 'cat1-subcat2-'
    - else (curr res is not None and doesn't end with -) -> clasf done
        - show starting categories with highligh
        - if something is chosen, e.g. cat2
            - overwrite: curr_res = 'cat2' or 'cat2-' (similar as before)

    The current function should handle just the above logic. Buttons somewhere
    else. So basically, in this function I will choose the categories, and in 
    another function I will show the corresponding buttons. Each button will
    have an on_click function (build there or somewhere) that will do the
    appropriate action.

    I am currently assuming top categories are ['despesses', 'ingressos']
    """

    if curr_res is None:
        if curr_move['Import'] <= 0:
            # get import subcategories
            # show those categories
            # each button wil have the on-click effect of saving curr_res and/or go next and/or overwrite
            pass
        else:
            # get despesses subcategories
            # show other categories (similar)
            # choose (similar)
            pass

    elif curr_res[-1] == '-':
        # get following categories
        # show (simlar)
        # choose (similar)
        pass

    else:
        # indicate highlight
        # get top categories (similar)
        # show (similar)
        # choose (similar)
        pass





    classification_cols = st.columns(4)

    with classification_cols[0]:
        st.write('C1')

    with classification_cols[1]:
        st.write('C2')

    with classification_cols[2]:
        st.write('C3')

    with classification_cols[3]:
        st.write('C4')


def _clsf_nav_buttons(curr_idx, n):
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
    st.write(st.session_state['classification']['results'])