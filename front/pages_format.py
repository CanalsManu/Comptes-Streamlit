import os

homepage_kwargs = {
    'page':     os.path.join(os.getcwd(), 'front', 'homepage.py'),
    'default':  True,
    'title':    'Inici',
    'icon':     ':material/home:' 
}
database_kwargs = {
    'page':     os.path.join(os.getcwd(), 'front', 'database.py'),
    'title':    'Base de dades',
    'icon':      ':material/database:'
}
cla_tree_kwargs = {
    'page':     os.path.join(os.getcwd(), 'front', 'classification_tree.py'),
    'title':    'Esquema de classificació',
    'icon':     ':material/family_history:'
}
analysis_kwargs = {
    'page':     os.path.join(os.getcwd(), 'front', 'analysis.py'),
    'title':    'Anàlisi',
    'icon':     ':material/bar_chart:' 
}
add_moves_kwarg  = {
    'page':     os.path.join(os.getcwd(), 'front', 'add_movements.py'),
    'title':    'Afegir moviments',
    'icon':     ':material/add:'
}