import streamlit as st
import pandas as pd
from back.classification_tree import tree_to_dashed, check_clsf_tree


def gather_comptes_in_df():
    """Gather db and classification tree into a dataframe."""
    db = st.session_state['db']
    check_clsf_tree(st.session_state['clsf_tree'])
    clsf_tree = tree_to_dashed(st.session_state['clsf_tree'])
    
    merged = db.copy()
    merged['Classificació'] = pd.Series(sorted(clsf_tree, reverse=True))
    return merged.to_csv(index=False)
