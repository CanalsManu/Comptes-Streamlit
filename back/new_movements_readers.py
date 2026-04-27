import pandas as pd
import os
import xml.etree.ElementTree as ET
from datetime import datetime
import streamlit as st


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
    print(df_repeated.columns)
    df_repeated.drop('Classificació', inplace=True, axis=1)

    # Filter contradictory elements (and here only returns different rows)
    df_contradictory = pd.merge(uploaded, db, how='left_anti')
    df_contradictory.drop(['Classificació', 'Categories'],
                          inplace=True, axis=1)

    return df_new, df_repeated, df_contradictory

@st.dialog("S'han trobat moviments controversials...")
def manage_controversial_movements(movements):
    """
    Show all controversial movements (those within db period but new)
    and decide which to classify and which to ignore.
    """
    # Initial setup
    if 'controversial_idx' not in st.session_state:
        current_idx = 0
        st.session_state['controversial_idx'] = 0
    else:
        current_idx = st.session_state['controversial_idx']

    if 'controversial_keep' not in st.session_state:
        st.session_state['controversial_keep'] = [False] * movements.shape[0]
    else:
        keep = st.session_state['controversial_keep']


    st.write('Controversials perque són del periode de temps de la base'
             ' de dades, però són nous moviments. ')
    st.write('Decideix qué fer amb cadascun.')
    st.write('---')

    st.write(movements.iloc[current_idx])

    cols = st.columns(2)

    with cols[0]:
        if st.button('Ignora'):
            st.session_state['controversial_idx'] = current_idx + 1
            st.rerun()

    with cols[1]:
        if st.button('Per calificar'):
            st.session_state['controversial_idx'] = current_idx + 1
            st.rerun()
