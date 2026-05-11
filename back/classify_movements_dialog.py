import streamlit as st
from datetime import date as ddate
import pandas as pd


MAX_CATEGORIES_PER_ROW = 4

def start_classification(movements):
    """First call to classify_movements. Setting defaults."""
    st.session_state['classification'] = {
        'status': 'in-progress',
        'results': [None] * movements.shape[0],
        'curr_idx': 0
    }
    classify_movements(movements)


@st.dialog(':small[Classificant...]', width='medium', on_dismiss='rerun')
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
        _clsf_end_page(movements)

    # Movement info
    else:
        curr_move = movements.iloc[curr_idx]
        _clsf_movement_info(curr_move)

        # Classification info
        st.space()
        _clsf_show_categories(curr_move)

        # Add curr_classification info
        _clsf_curr_res_info(curr_move)

    # Navigation buttons and progress
    st.space()
    _clsf_nav_buttons(curr_idx, n)


def _clsf_end_page(movements):
    """
    End page. If (all) clasf done, button to write to database.
    
    - if all clsf is done:
        - offer button to write to database
        - toggle to see/double check clsf
    - if not all clsf is done:
        - disables button to write to database
        - toggle to see/double check clsf
    """
    # Set up
    results = st.session_state['classification']['results']
    completed = all([_is_completed(res) for res in results])

    if completed:
        info_text = 'Classificació completa!'
        disabled = False
    else:
        info_text = 'Classificació incompleta. Si us plau, acaba-la per' \
                    ' continuar).'
        disabled = True

    # Display after add movements
    if st.session_state['classification']['status'] == 'done':
        st.balloons()
        st.text('CLASSIFICACIÓ FETA!', text_alignment='center',
                width='stretch')
        show_current_clsf(movements, results)
        st.stop()

    # Display before adding movements
    st.text(info_text)
    st.button('Afegeix a la base de dades', disabled=disabled,
                type='primary', width='stretch',
                on_click=add_classification_to_db, args=(movements, results))
    if st.toggle('Revisa la classificació'):
        show_current_clsf(movements, results)    


def add_classification_to_db(movements, results):
    """
    Add classification (results) of the movements to the database. Basically:
    - add movements (safely?)
    - flag that we are done
    - close
    """
    # add
    db = st.session_state['db']
    
    st.session_state['classification']['status'] = 'done'


def show_current_clsf(movements, results):
    """Show table to double check classifications at end page."""
    show_moves = movements.copy()
    show_moves['Data'] = show_moves['Data'].map(_format_date)
    show_moves['Import'] = show_moves['Import'].map(_format_import)
    show_moves['Classificació'] = [
        _build_clsf_badges(res, amount)
        for res, amount in zip(results, movements['Import'])
    ]
    st.table(
        show_moves,
        hide_index=True,
        border='horizontal'
    )


def _format_date(date_str):
    """Format 'dd/mm/yyyy' into 'weekday, d de m. de yyyy'."""
    d, m, y = date_str_to_tuple(date_str)

    # Weekday
    weekday_idx = weekday_from_date(date_str)
    weekday_names = ['Dl.', 'Dt.', 'Dc.', 'Dj.', 'Dv.', 'Ds.', 'Dg.']

    # Month
    de_month_names = ['de gen.', 'de feb.', 'de mar.', "d'abr.",
                   'de mai.', 'de jun.', 'de jul.', "d'ago.",
                   'de set.', "d'oct.", 'de nov.', 'de dec.']
    return f'{weekday_names[weekday_idx]}, {d} {de_month_names[m]} de {y}'



def _clsf_progress(n):
    """Show progress. Array of buttons showing status, on_click jump to idx."""
    curr_idx = st.session_state['classification']['curr_idx']
    results = st.session_state['classification']['results']
    # st.progress(curr_idx/n)

    # Each button moves to taret_idx
    def _action(target_idx):
        st.session_state['classification']['curr_idx'] = target_idx

    # Array of buttons
    cont = st.container(horizontal=True, horizontal_alignment='center',
                        vertical_alignment='center', gap=None)
    for move_idx in range(n+1):
        is_curr_idx = move_idx == curr_idx

        # Choose icon
        if move_idx == n:
            icon = (':material/add_circle:' if is_curr_idx
                    else ':material/add:')
        else:
            completed = _is_completed(results[move_idx])
            icon = _choose_icon(is_curr_idx, completed)

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

    info_str = _build_clsf_badges(curr_res, curr_move['Import'])

    cont = st.container(width='stretch', horizontal_alignment='center',
                        vertical_alignment='center', horizontal=True)
    cont.markdown(info_str)


def _build_clsf_badges(curr_res, amount):
    """Return string with markdown to render badges."""
    # Get info
    if curr_res is None:
        show_res = 'despeses-' if amount <= 0 else 'ingressos-'
    else:
        show_res = curr_res

    # Display info
    badges_md = []
    first_color = {'ingressos': 'green', 'despeses': 'red'}
    for idx, category in enumerate(show_res.split('-')):
        color = first_color[category] if idx==0 else 'grey'
        badges_md.append(f':{color}-badge[{category}]')
        
    sep = ' -> '
    return sep.join(badges_md)


def _clsf_movement_info(curr_move):
    move_cols = st.columns(2)

    with move_cols[0]:
        date = date_str_to_tuple(curr_move['Data'])
        month_calendar(date[1], date[2], hightlight=date[0])

    with move_cols[1]:
        cont = st.container(vertical_alignment='center', height='stretch')
        cont.write(curr_move['Nom'])
        cont.write(_format_import(curr_move['Import']))


def _format_import(amount):
    import_str = ':green[+' if amount > 0 else ':red[-'
    import_str += f'{abs(amount):.2f}' + ']'
    return import_str


def month_calendar(month, year, hightlight=None):
    """Month: int from 1 to 12 (inclusive). highlight (optional) day (int)."""
    # Formats
    off_month = ':gray-badge[····]'
    off_month = ':gray-badge[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]'
    in_month = ':gray-badge[ {:02} ]'
    curr_day = ':primary-badge[ {:02} ]'
    week_name = ':primary-badge[{}]'

    # Set up
    assert 1 <= month <= 12 
    month_days = days_in_month(month, year)
    def write_week(week, sep=''):
        week.insert(5, '|')
        st.markdown(sep.join(week), text_alignment='center')

    # Prepare week names
    names = ['  dl', 'dt', 'dc', 'dj', 'dv', 'ds', 'dg']
    names = ['DL', 'DT', 'DC', 'DJ', 'DV', 'DS', 'DG']
    week_names = [week_name.format(d) for d in names]

    # Build first week
    first_weekday = weekday_from_date((1, month, year))  # mon: 0, sun: 6
    first_week = [off_month] * first_weekday
    first_week += [in_month.format(n) for n in range(1, 7 - first_weekday + 1)]

    # Container with multiple markdowns
    month_cont = st.container(horizontal=False, horizontal_alignment='center',
                             gap=None, vertical_alignment='center',
                             width='stretch', border=False)
    with month_cont:

        # Write header and first week
        spacing = ' ' * 30
        st.text(month_name(month).upper() + spacing + str(year), 
                text_alignment='center')
        write_week(first_week)

        # Rest of the month
        for start_day in range(8 - first_weekday, month_days, 7):
            # Build week
            days_in_week = min(month_days - start_day, 7)
            week = [in_month.format(n)
                    for n in range(start_day, start_day+days_in_week)]
            week += [off_month] * (7 - days_in_week)

            # If given, highlight day
            if hightlight is None:
                pass
            elif start_day <= hightlight <= start_day + days_in_week - 1:
                week[hightlight - start_day] = curr_day.format(hightlight)

            write_week(week)
    

def month_name(month):
    """month: int from 1 to 12 (inclusive)."""
    assert 1 <= month <= 12
    names = ['Gener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny',
             'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Decembre']
    return names[month]


def days_in_month(month, year):
    """month: int from 1 to 12 (inclusive)."""
    assert 1 <= month <= 12
    if month == 12:
        return 31
    return (ddate(year, month+1, 1) - ddate(year, month, 1)).days

def weekday_from_date(date):
    """Date in format 'dd/mm/yyyy' or (d, m, y) to weekday (mon:0, sun:6)."""
    if isinstance(date, str):
        date = date_str_to_tuple(date)
    return ddate(date[2], date[1], date[0]).weekday()


def date_str_to_tuple(date_str):
    """Date in format (str) dd/mm/yyyy to (list[int]) (d, m, y)."""
    return (int(date_str[:2]), int(date_str[3:5]), int(date_str[6:]))
    

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
            st.session_state['classification']['curr_idx'] = _find_nxt_unclsf()

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


def _find_nxt_unclsf():
    """Find next index with unclsf item."""
    curr_idx = st.session_state['classification']['curr_idx']
    results = st.session_state['classification']['results']
    for next_idx in range(curr_idx+1, len(results)):
        if results[next_idx] is None:
            return next_idx
        if results[next_idx][-1] == '-':
            return next_idx
    else:
        return len(results)


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


@st.dialog('Classificació feta.', width='medium')
def show_classification(movements):
    """Show classification"""
    show_current_clsf(movements, st.session_state['classification']['results'])


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