import pandas as pd
import os
import xml.etree.ElementTree as ET
from datetime import datetime


def read_xml_to_df(path):
    """Read xml, trim it and return as df with Data, Nom, Import."""

    content = read_xml(path)
    trimmed = trim_data(content)
    df = pd.DataFrame(data=trimmed, columns=('Data', 'Nom', 'Import'))

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
    new movements, repeated movements and contradictory movements.
    """
    db_enddate = datetime.strptime(db.iloc[0]['Data'], '%d/%m/%Y')
    db_startdate = datetime.strptime(db.iloc[-1]['Data'], '%d/%m/%Y')

    date_filter = datetime.strptime(db['Data'], '%d/%m/%Y')
