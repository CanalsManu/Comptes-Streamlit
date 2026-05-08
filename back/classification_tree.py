import streamlit as st

def dashed_to_tree(dashed):
    """
    Get classification tree from list or Series of dashed classification.
    
    Tree is a dictionary, where None indicates the end of one branch.
    """
    if not isinstance(dashed, list):  # assume is then pd.Series
        dashed = dashed.tolist()

    tree = {}
    for item in dashed:
        split = item.split('-')
        multi_key = ''.join(f'["{k}"]' for k in split)
        assert 'tree' in locals()

        # If try successeeds -> branch already exists -> continue
        try:
            eval('tree' + multi_key)
            continue

        # If it fails -> split is a new branch -> add it
        except KeyError:
            tree = _add_branch_to_tree(tree, split)

    return tree

        
def _add_branch_to_tree(tree, branch):
    """
    Sets a value in a nested dictionary, creating intermediate 
    dictionaries if they do not exist.
    """
    current = tree
    # Iterate through the path except for the very last key
    for key in branch[:-1]:
        # If the key isn't there, or isn't a dictionary, create one
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    
    # Set the value for the final key in the path
    current[branch[-1]] = None
    return tree


def check_tree(tree):
    """Run checks on the classification tree and raise error if needed."""
    assert len(tree.keys()) == 2
    keys = sorted(list(tree.keys()))
    assert keys == ['despeses', 'ingressos']


