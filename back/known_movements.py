import pandas as pd
import streamlit as st
ss = st.session_state

def get_known_movements(names, categories):
    """
    Return unique names and corresponding categories from given pd.Series.
    
    Output is a dictionary where keys are the unique names and values a list of
    known catergories for that name (can be more than one for some names).
    """
    assert len(names) == len(categories)

    unique_names = names.unique().tolist()
    return {
        name: categories[names==name].unique().tolist()
        for name in unique_names
    }


def get_autocompletable(known_movements):
    """
    Return known 'autocompletable' movements: only with one known category.
    
    Output is a disctionary where keys are the unique names and values are the
    (dashed) categories.
    """
    return {
        name: categories[0] for name, categories in known_movements.items()
        if len(categories) == 1
    }


@st.dialog('Autcompletar', dismissible=False)
def manage_autocomplete(to_be_auto, autocompletable):
    """
    Ask to autcomplete or ignore known movements (optionally show them).

    If autocompleting, call autocomplete() and set ss['manage_autocomplete']
    to False (to_be_clsf will be updated in the main function).
    """
    # Message
    assert len(to_be_auto) > 0
    if len(to_be_auto) == 1:
        st.text('S\'ha trobat un moviment autocompletable. El vols '
                'autocompletar?')
    else:
        st.text(f'S\'han trobat {len(to_be_auto)} moviments autocompletables. '
                'Vols autocompletar-los?')

    # Buttons
    cols = st.columns([1, 1])
    
    if cols[0].button('Autcompleta', width='stretch', shortcut='1'):
        autocomplete(to_be_auto, autocompletable)
        ss['manage_autocomplete'] = False
        st.rerun()
    
    if cols[1].button('Ignora', width='stretch', shortcut='2'):
        ss['manage_autocomplete'] = False
        st.rerun()

    # Display 
    if st.toggle('Mostra els moviments autocompletables.'):
        st.dataframe(to_be_auto, hide_index=True)
        st.write(autocompletable)


def autocomplete(to_be_auto, autocompletable):
    """
    Autocomplete the given movements.

    Autcomplete means adding categories to to_be_auto, and save the dataframe 
    in st.session_state['autocompleted'] to be used in:
        back.classify_movement_dialog.add_classification_to_db()
    """
    pass
