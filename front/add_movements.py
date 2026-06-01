import streamlit as st
import pandas as pd
from back.new_movements_readers import (
    read_xml_to_df,
    compare_movements,
    manage_controversial_movements,
    add_controversial_to_new
)
from back.classify_movements_dialog import (
    classify_movements,
    show_classification,
    start_classification
)
from back.fake_file_uploader import fake_file_uploader
from back.known_movements import (
    get_autocompletable,
    manage_autocomplete
)
ss = st.session_state


# ------------------------------------------------------------------------------
# INITIAL STATE
# ------------------------------------------------------------------------------


db = ss.get('db', False)
if db is False:
    st.write("Falta el fitxer de comptes, ves a Inici i puja'l.")
    st.stop()


# ------------------------------------------------------------------------------
# FILE UPLOADER AND READER
# ------------------------------------------------------------------------------


def cleanup_post_discard_file():
    """If uploaded file is discarded, run these to restart cleanly."""
    # Reset controversial settings
    ss.pop('controversial_select', 0)
    ss.pop('manage_controversial', 0)
    ss.pop('classification', 0)

    # Reset uploaded file info (movements and name)
    ss.pop('uploaded_movements', 0)
    ss.pop('uploaded_file_name', 0)

    # Reset autocomplete settings
    ss.pop('manage_autocomplete', 0)
    ss.pop('autocompleted', 0)


# uploaded file -> fake it and continue
if 'uploaded_movements' in ss:
    assert 'uploaded_file_name' in ss
    st.markdown(':small[Fitxer amb els nous moviments a classificar.]')
    fake_file_uploader(ss['uploaded_file_name'], 'uploader_cont',
                       on_click=cleanup_post_discard_file)

# not uploaded file -> show real uploader
else:
    st.markdown(':small[Puja el fitxer amb els nous moviments a classificar.]')
    uploaded_file = st.file_uploader('_', type='xml',
                                    accept_multiple_files=False,
                                    label_visibility='collapsed')
    
    if uploaded_file is not None:
        uploaded_movements = read_xml_to_df(uploaded_file)
        ss['uploaded_movements'] = uploaded_movements
        ss['uploaded_file_name'] = uploaded_file.name
        st.rerun()  # rerun to show fake uploader and continue
    else:
        st.stop()


# ------------------------------------------------------------------------------
# READ, UPLOAD AND MANAGE CONTROVERSIALS
# ------------------------------------------------------------------------------

# Read
# uploaded_movements = read_xml_to_df(uploaded_file)
uploaded_movements = ss['uploaded_movements']
new, repeated, controversial = compare_movements(uploaded_movements, db)

# Manage
# 'manage_controversial' is set in manage_controversial_movements() 
if ss.get('manage_controversial', not controversial.empty):
    manage_controversial_movements(controversial)

# Update movements
if 'controversial_select' in ss:
    to_be_clsf = add_controversial_to_new(new, ss['controversial_select'])
else:
    to_be_clsf = new

# Movements info
if st.toggle('Mostra els nous moviments.'):
    st.write('---')
    st.write('uploaded')
    st.dataframe(uploaded_movements, hide_index=True)
    st.write('new')
    st.dataframe(new, hide_index=True)
    st.write('repeated')
    st.dataframe(repeated, hide_index=True)
    st.write('controversial')
    st.dataframe(controversial, hide_index=True)
    if 'controversial_select' in ss:
        st.write('controversial selection')
        st.dataframe(ss['controversial_select'], hide_index=True)
    st.write('to be classified')
    st.dataframe(to_be_clsf, hide_index=True)
    st.write('---')


# ------------------------------------------------------------------------------
# AUTOCOMPLETE
# ------------------------------------------------------------------------------

# Set up
autocompletable = get_autocompletable(ss['known_movements'])
mask_auto = to_be_clsf['Nom'].isin(list(autocompletable.keys()))
to_be_auto = to_be_clsf[mask_auto]

# Manage it
if ss.get('manage_autocomplete', not to_be_auto.empty):
    manage_autocomplete(to_be_auto, autocompletable)

if 'autocompleted' in ss:
    to_be_clsf = to_be_clsf[~mask_auto]
# ------------------------------------------------------------------------------
# CLASSIFICATION
# ------------------------------------------------------------------------------


st.space('small')
_, col, _ = st.columns([1, 6, 1])

if to_be_clsf.empty:
    pass

if 'classification' not in ss:
    if to_be_clsf.empty:
        name, disabled = 'Cap moviment nou', True
    else:
        name, disabled = 'Comença la classificació', False

    # use on_click to force rerun
    col.button(name, width='stretch', type='primary', disabled=disabled,
               on_click=start_classification, args=[to_be_clsf],
               shortcut='Enter')

elif ss['classification']['status'] == 'done':
    if col.button('Classificació feta! Mostra-la.', width='stretch',
                  type='tertiary', shortcut='Enter'):
        # TODO?: add autocompleted movements to show too
        show_classification(to_be_clsf)

else:
    if col.button('Continua la classificació', width='stretch',
                  type='secondary', shortcut='Enter'):
        classify_movements(to_be_clsf)

