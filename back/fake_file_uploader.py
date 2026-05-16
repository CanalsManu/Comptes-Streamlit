"""
Same as st-file_uplader but can accept file path as argument and will display
it.
"""
import streamlit as st
from streamlit.errors import StreamlitDuplicateElementKey
import ntpath


MAX_NAME_LEN = 20

    
def fake_file_uploader(file_name, key, **button_kwargs):
    """ Show a file uploader containing a file (key: unique element key)."""

    # Container
    st.html(f"<style>{container_style(key)}</style>")
    cont = st.container(border=True, key=key, horizontal=True,
                        vertical_alignment='center', height=68)

    # Texts
    button_text = f'{shorten_name(file_name)}'
    info_text = ':small[:gray[Clica per pujar un altre fitxer]]'

    # Display
    with cont:
        st.button(button_text, icon=':material/attach_file:', **button_kwargs)
        st.markdown(info_text)


def container_style(key):
    return f"""
    .st-key-{key} {{
        background-color: rgba(38, 39, 48, 1);
        border-color: rgba(38, 39, 48, 1);
    }}
    """


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def shorten_name(name, max_len=MAX_NAME_LEN):
    """ Shortens a name if it exceeds the max length (adds dots in between). """
    if len(name) <= max_len:
        return name
    else:
        n = max_len // 2 - 1
        return name[:n] + '...' + name[-n:]