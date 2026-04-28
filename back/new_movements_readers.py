import pandas as pd
import os
import xml.etree.ElementTree as ET
from datetime import datetime
import streamlit as st
import numpy as np


def read_xml_to_df(path):
    """Read xml, trim it and return as df with Data, Nom, Import."""

    content = read_xml(path)
    trimmed = trim_data(content)
    df = pd.DataFrame(data=trimmed, columns=('Data', 'Nom', 'Import'))

    # Initial formatting
    df['Nom'] = df['Nom'].map(str.upper)
    df['Import'] = df['Import'].map(lambda x: float(x))

    return df

def trim_data(content):
    """ Trim content and keep only date, description and amount. """
    # print('Keeping cols 0, 1 and 3 from rows 6 until (len - 9) inclusive (row number, not index).')
    trimmed = [[r[0], r[1], r[3]] for r in content[6-1:-7]]
    return trimmed


def read_xml(file_path: str) -> list:
    """ Read file_path's Row>Cell>Data and returns a list with the rows. """
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Excel SpreadsheetML usually uses namespaces — handle that
    namespaces = {'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}
    content = _extract_rows(root, namespaces)
    return content

def _extract_rows(root, namespaces):
    """ Extract rows (Row>Cell>Data) from root. """
    content = []
    rows = root.findall('.//ss:Row', namespaces)
    for row in rows: # Extract text inside each <Data> tag
        cells = [
            cell.find('ss:Data', namespaces).text if cell.find('ss:Data', namespaces) is not None else ''
            for cell in row.findall('ss:Cell', namespaces)
        ]
        content.append(cells)
    return content


SEP = '>'
INDENT = ' | '
def _get_tag(element):
    """ Return tag without namespace (leading {}). """
    tag = element.tag
    closing_claudator_idx = tag.find('}') 
    return element.tag[closing_claudator_idx+1:]


def _print_family_tree(parent, level = 0):
    """ Recursively print children (usually parent = root). """
    tag = _get_tag(parent)
    print(INDENT * level + SEP, tag)
    if len(parent) == 0: print(INDENT * (level + 1) + '=', parent.text)
    for child in list(parent):
        _print_family_tree(child, level = level + 1)


def compare_movements(uploaded, db):
    """
    Compare updated movements with the current database and returns
    new movements, repeated movements and controversial movements 
    (controversial as in within the db time period but new).
    """
    # Filter new movements
    db_enddate = datetime.strptime(db.iloc[0]['Data'], '%d/%m/%Y')
    db_startdate = datetime.strptime(db.iloc[-1]['Data'], '%d/%m/%Y')

    def date_not_in_db_period(date_str):
        """Border dates count as 'in' the db period."""
        date_dt = datetime.strptime(date_str, '%d/%m/%Y')
        return not (db_startdate <= date_dt <= db_enddate)

    new_mask = uploaded['Data'].map(date_not_in_db_period)
    df_new = uploaded[new_mask]
    uploaded = uploaded[~new_mask]

    # Filter repeated movements (pd.merge like this only returns equal rows)
    df_repeated = pd.merge(uploaded, db)
    df_repeated.drop('Classificació', inplace=True, axis=1)

    # Filter controversial elements (and here only returns different rows)
    df_controversial = pd.merge(uploaded, db, how='left_anti')
    df_controversial.drop(['Classificació', 'Categories'],
                          inplace=True, axis=1)

    return df_new, df_repeated, df_controversial


@st.dialog("S'han trobat moviments controversials", dismissible=False)
def manage_controversial_movements(movements):
    """
    Show all controversial movements (those within db period but new)
    and decide which to classify and which to ignore.

    Flag that we are done with 'manage_controversial' = False.
    """
    # Starting values
    n = movements.shape[0]
    if 'controversial_idx' not in st.session_state:
        st.session_state['controversial_idx'] = 0
        st.session_state['controversial_keep'] = [None] * n

    # Current status
    curr_idx = st.session_state['controversial_idx']
    keep = st.session_state['controversial_keep']
    curr_state = keep[curr_idx]if curr_idx < n else None

    # Info
    if st.toggle('Info', key='info_toggle'):
        _controversial_info()

    # Show movement
    if curr_idx >= n:
        _controversial_end_page(movements)
    else:
        st.write(pd.DataFrame(movements.iloc[curr_idx]).T)

    # Buttons
    _controversial_buttons(curr_idx, curr_state, n)
        

def _controversial_end_page(movements):
    """Last 'page' on the controversial dialog."""
    _, col, _ = st.columns([1, 6, 1])
    col.button('Cap més moviment controversial.', width='stretch', type='tertiary')

    # only close if all answered
    disable_save = any([
        (item == None) for item in st.session_state['controversial_keep']
    ])

    # Store selection in session, delete keys and flag out
    if col.button('Guarda les eleccions', width='stretch', type='primary',
                    disabled=disable_save):
        
        # store only if any want to be kept
        if any(st.session_state['controversial_keep']):
            mask = st.session_state['controversial_keep']
            st.session_state['controversial_select'] = movements[mask]

        del st.session_state['controversial_idx']
        del st.session_state['controversial_keep']

        # this flag controls if dialog opens
        st.session_state['manage_controversial'] = False
        st.rerun()


def _controversial_info():
    """Controversial information shown on dialog."""

    def switch_off_toggle():
        """Toggle programmatically."""
        st.session_state['info_toggle'] = False

    st.write('---')
    st.write('Controversials perque són del periode de temps de la base'
            ' de dades, però són nous moviments. ')
    _, col, _ = st.columns([1, 3, 1])
    col.button('Decideix qué fer amb cadascun', on_click=switch_off_toggle,
                width='stretch')
    st.write("L'opció elegida serà indicada amb color.")
    st.write('---')


def _controversial_buttons(curr_idx, curr_state, n):
    """Set of buttons on controversial dialog."""
    cols = st.columns([1, 2, 2, 1])
    main_btn_w = 150

    with cols[0]:  # left
        cont_0 = st.container(horizontal_alignment='left')
        if cont_0.button('<', disabled = curr_idx <= 0):
            st.session_state['controversial_idx'] = curr_idx - 1
            st.rerun()
    
    with cols[1]:  # ignora
        cont_1 = st.container(horizontal_alignment='right')
        if cont_1.button('Ignora',
                         width=main_btn_w,
                         disabled = not (0 <= curr_idx <= n-1),
                         type='primary' if curr_state == False else 'secondary'):
            st.session_state['controversial_keep'][curr_idx] = False
            st.session_state['controversial_idx'] = curr_idx + 1
            st.rerun()
    
    with cols[2]:  # per calificar
        cont_2 = st.container(horizontal_alignment='left')
        if cont_2.button('Per calificar',
                         width=main_btn_w,
                         disabled = not (0 <= curr_idx <= n-1),
                         type='primary' if curr_state == True else 'secondary'):
            st.session_state['controversial_keep'][curr_idx] = True
            st.session_state['controversial_idx'] = curr_idx + 1
            st.rerun()
    
    with cols[3]:  # right
        cont_3 = st.container(horizontal_alignment='right')
        if cont_3.button('>', disabled = curr_idx >= n):
            st.session_state['controversial_idx'] = curr_idx + 1
            st.rerun()


def add_controversial_to_new(new, selection):
    """Add selection from controversial to new and sort."""
    # Add
    new = pd.concat((new, selection))

    # Sort
    ref_date = datetime.strptime('05/07/1998', '%d/%m/%Y')
    new['Seconds'] = new['Data'].map(
        lambda d: (datetime.strptime(d, '%d/%m/%Y') - ref_date).total_seconds()
    )
    new.sort_values('Seconds', ascending=False, inplace=True)
    new.drop('Seconds', axis=1, inplace=True)

    return new