import pandas as pd
import os


def create_comptes_files_new_version(
    classification_path,
    movements_path,
    classification_tree_path,
    save_to_path
) -> pd.DataFrame:
    """
    Given the paths of old files create new comptes.csv file.
    
    Patameters:
        - classification_path: no-header .csv with Categoria and Subcategoria
        - movements_path: no-header .csv with Data Nom Import
        - classification_tree_path: .csv with classification three in new format
                                    and header Classificació 1
        - save_to_path: .csv with Data Nom Import Categories Classifiació
    """
    # Get csv
    df_cat = pd.read_csv(classification_path, header=None,
                         names=['Categoria', 'Subcategoria'])
    df_mvs = pd.read_csv(movements_path, header=None,
                         names=['Data', 'Nom', 'Import'])
    df_cla = pd.read_csv(classification_tree_path)

    # Print heads
    print('Classification\n', df_cat.head())
    print('Movements\n', df_mvs.head())
    print('Classif. tree\n', df_cla.head())

    # Rename
    categories = df_cat['Categoria'].to_list()
    subcategories = df_cat['Subcategoria'].to_list()
    import_ = df_mvs['Import']
    renamed = []
    for cat, subcat, imp in zip(categories, subcategories, import_):
        name = 'despeses-' if float(imp) < 0 else 'ingressos-'
        name += cat+'-'+subcat if subcat != '-' else cat
        renamed.append(name)
    df_cat['Renamed'] = pd.DataFrame(renamed)
    
    # Merge it
    df_merge = pd.DataFrame()
    df_merge['Data'] = df_mvs['Data']
    df_merge['Nom'] = df_mvs['Nom']
    df_merge['Import'] = df_mvs['Import']
    df_merge['Categories'] = pd.DataFrame(renamed)
    df_merge['Classificació'] = df_cla['Classificació 1']
    print('New file\n', df_merge.head())

    # Save it
    df_merge.to_csv(save_to_path, index=False)

    return df_merge


# File paths
classification_path = os.path.join(os.getcwd(), 'data', 'old_comptes_files', 'classification.csv')
movements_path = os.path.join(os.getcwd(), 'data', 'old_comptes_files', 'movements.csv')
classification_tree_path = os.path.join(os.getcwd(), 'data', 'old_comptes_files', 'classificacio1.csv')
save_to_path = os.path.join(os.getcwd(), 'data', 'comptes.csv')

# Run
output = create_comptes_files_new_version(
    classification_path,
    movements_path,
    classification_tree_path,
    save_to_path
)

# Try reading it
# df_read = pd.read_csv(save_to_path)
# print(df_read)