import pandas as pd

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
    Return known 'autocompletable' movements: only one known category.
    
    Output is a disctionary where keys are the unique names and values are the
    (dashed) categories.
    """
    return {
        name: categories[0] for name, categories in known_movements.items()
        if len(categories) == 1
    }