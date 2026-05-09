import streamlit as st


MAX_CATEGORIES_PER_ROW = 4

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

    # End page
    if curr_idx >= n:
        _clsf_end_page()

    # Movement info
    else:
        curr_move = movements.iloc[curr_idx]
        _clsf_movement_info(curr_move)

        # Classification info
        _clsf_show_categories(curr_move)

        # Add curr_classification info
        _clsf_curr_res_info(curr_move)

    # Navigation buttons and progress
    _clsf_nav_buttons(curr_idx, n)


def _clsf_end_page():
    """End page. If (all) clasf done, button to write to database."""
    st.write('end page.')


def _clsf_progress(n):
    """Show progress. st.progress() or array of buttons."""
    curr_idx = st.session_state['classification']['curr_idx']
    results = st.session_state['classification']['results']

    # st.progress(curr_idx/n)

    # Array of buttons: one button for each movement, each buttons shows if 
    # that movement has been completed, also allows to click and jump there, 
    # also somehow highlight current position.
    cont = st.container(horizontal=True, horizontal_alignment='center',
                        vertical_alignment='center', gap=None)
    for move_idx in range(n):
        # Choose icon
        is_curr_idx = move_idx == curr_idx
        completed = _is_completed(results[move_idx])
        icon = _choose_icon(is_curr_idx, completed)

        # Action
        def _action(target_idx):
            st.session_state['classification']['curr_idx'] = target_idx

        # Button
        cont.button(icon, type='tertiary', key=f'progress_btn_{move_idx}',
                    on_click=_action, args=[move_idx])


def _is_completed(curr_res):
    """Return if clsf completed given the current results (str)."""
    if curr_res is None:
        return False
    elif curr_res[-1] == '-':
        return False
    else:
        return True


def _choose_icon(is_curr_idx, completed):
    match (is_curr_idx, completed):
        case (True, True): return ':material/check_circle:'
        case (True, False): return ':material/circle:'
        case (False, True): return ':material/check_small:'
        case (False, False): return ':material/check_indeterminate_small:'
        case _: raise Exception


def _clsf_curr_res_info(curr_move):
    """Show current result under buttons."""
    curr_idx = st.session_state['classification']['curr_idx']
    curr_res = st.session_state['classification']['results'][curr_idx]

    # Get info
    if curr_res is None:
        show_res = 'despeses-' if curr_move['Import'] <= 0 else 'ingressos-'
    else:
        show_res = curr_res

    # Display info
    badges_md = []
    first_color = {'ingressos': 'green', 'despeses': 'red'}
    for idx, category in enumerate(show_res.split('-')):
        color = first_color[category] if idx==0 else 'blue'
        badges_md.append(f':{color}-badge[{category}]')
    cont = st.container(width='stretch', horizontal_alignment='center',
                        vertical_alignment='center', horizontal=True)
    cont.markdown(' -> '.join(badges_md))

    # for category in show_res.split('-'):
    #     st.badge(category)
    # st.button(show_res, type='tertiary', width='stretch')


def _clsf_movement_info(curr_move):
    move_cols = st.columns(2)

    with move_cols[0]:
        st.write(curr_move['Data'])

    with move_cols[1]:
        st.write(curr_move['Nom'])
        st.write(curr_move['Import'])

    st.write('---')
    

def _clsf_show_categories(curr_move):
    """
    Show possible categories from clsf tree and choose.
    
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
    - elif curr_res end with '-' -> clsf in progress
        - show and choose subcategories based on curr_res, e.g., subcat2
        - if there are no more subcategories
            - save curr_res = 'cat1-subcat2'
            - go next
        - if there are more subcategories
            - save curr_res = 'cat1-subcat2-'
    - else (curr res is not None and doesn't end with -) -> clsf done
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
    tree = st.session_state['clsf_tree']
    curr_idx = st.session_state['classification']['curr_idx']
    curr_res = st.session_state['classification']['results'][curr_idx]

    # Starting new classification
    if curr_res is None:
        top_category = 'despeses' if curr_move['Import'] <= 0 else 'ingressos'
        next_categories = list(tree[top_category].keys())
        _show_clsf_buttons(next_categories, top_category=top_category)
        # choose (similar)

    # On-going classification
    elif curr_res[-1] == '-':
        prev_categories = curr_res[:-1].split('-')
        subtree = get_with_multikey(tree, prev_categories)
        if subtree is None:
            raise TypeError(f"No more subtree to clsf, should've been caught.")
        next_categories = list(subtree.keys())
        _show_clsf_buttons(next_categories)
        # choose (similar)

    # Classification done, showing result (possible overwrite)
    else:
        top_category = 'despeses' if curr_move['Import'] <= 0 else 'ingressos'
        next_categories = list(tree[top_category].keys())
        highlight = curr_res.split('-')[1]
        _show_clsf_buttons(next_categories, highlight=highlight)
        # choose (similar)


def _show_clsf_buttons(categories, highlight=None, top_category=None):
    """
    Show categories buttons. Each button has on click effects.
    
    Parameters:
        - categories: list[str]
        - highlight: (optional) str, button to highlight
        - top_category: (optional) str, top category to append to curr_res.
                        Only to be used when curr_res = None.
    """
    tree = st.session_state['clsf_tree']
    curr_idx = st.session_state['classification']['curr_idx']
    curr_res = st.session_state['classification']['results'][curr_idx]

    def _action(category):
        """Add choice to result. If still need to clasf -> add ash, else ->
        go next. If highlight, overwrite result."""
        # New result
        if top_category is not None:  # showing 1st subcat under despe./ingres.
            assert curr_res is None
            new_res = top_category + '-'
        elif highlight is not None:  # clasf done, if triggered overwrite
            new_res = curr_res.split('-')[0] + '-'
        else:  # on-going clasf
            assert curr_res[-1] == '-'
            new_res = curr_res
        new_res += category

        # Check if clasf is done
        subtree = get_with_multikey(tree, new_res.split('-'))
        if subtree is None: # No more clasf -> save and go next
            st.session_state['classification']['results'][curr_idx] = new_res
            st.session_state['classification']['curr_idx'] += 1

        else: # More subcategories -> save with dash and show same idx
            new_res += '-'
            st.session_state['classification']['results'][curr_idx] = new_res

    # Show max num per row   
    for step_idx in range(0, len(categories), MAX_CATEGORIES_PER_ROW):
        # Gather row categories
        curr_num_categories = min(MAX_CATEGORIES_PER_ROW,
                                  len(categories) - step_idx)
        row_categories = categories[step_idx:step_idx+curr_num_categories]

        # Show row
        cols = st.columns(curr_num_categories)
        for idx, category in enumerate(row_categories):    
            typ = 'primary' if highlight == category else 'secondary'
            cols[idx].button(category, type=typ, width='stretch',
                            shortcut=str(step_idx+idx+1),
                            on_click=_action, args=[category])


def _clsf_nav_buttons(curr_idx, n):
    nav_cols = st.columns([1, 3, 1])

    def _go_left():
        st.session_state['classification']['curr_idx'] -= 1 
    cont_left = nav_cols[0].container(horizontal_alignment='left')
    cont_left.button('', disabled = (curr_idx <= 0), on_click = _go_left,
                      type='tertiary', shortcut='Left')
    
    with nav_cols[1]:
        _clsf_progress(n)

    def _go_right():
        st.session_state['classification']['curr_idx'] += 1 
    cont_right = nav_cols[2].container(horizontal_alignment='right')
    cont_right.button('', disabled = (curr_idx  >= n), on_click = _go_right,
                      type='tertiary', shortcut='Right')


@st.dialog('Classificació feta.')
def show_classification():
    """Show classification"""
    st.write(st.session_state['classification']['results'])


def _safe_get_curr_res(n, default=None):
    """Get current result if 0 <= curr_idx <= n-1 (n should be size)."""
    curr_idx = st.session_state['classification']['curr_idx']
    if 0 <= curr_idx <= n-1:
        return st.session_state['classification']['results'][curr_idx]
    else:
        return default
    

def get_with_multikey(d, keys):
    """Get d[keys[0]][...][keys[-1]], where keys is list of strings."""
    assert len(keys) >= 1

    multi_key = ''.join(f'["{k}"]' for k in keys)
    result = eval('d'+multi_key)
    return result