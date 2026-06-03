from datetime import date as ddate
import pandas as pd

def build_clsf_badges(classification, amount = None):
    """Get md string to render dashed classification as badges with arrows."""

    # Get info
    if classification is None:
        assert amount is not None  # amount must be given here
        show_res = 'despeses-' if amount <= 0 else 'ingressos-'
    else:
        show_res = classification

    # Display info
    badges_md = []
    first_color = {'ingressos': 'green', 'despeses': 'red'}

    for idx, category in enumerate(show_res.split('-')):
        color = first_color[category] if idx==0 else 'grey'
        badges_md.append(f':{color}-badge[{category}]')
        
    sep = ' -> '
    return sep.join(badges_md)


def format_date(date_str):
    """Format 'dd/mm/yyyy' into 'weekday, d de m. de yyyy'."""
    d, m, y = date_str_to_tuple(date_str)

    # Weekday
    weekday_idx = weekday_from_date(date_str)
    weekday_names = ['Dl.', 'Dt.', 'Dc.', 'Dj.', 'Dv.', 'Ds.', 'Dg.']

    # Month
    de_month_names = ['de gen.', 'de feb.', 'de mar.', "d'abr.",
                   'de mai.', 'de jun.', 'de jul.', "d'ago.",
                   'de set.', "d'oct.", 'de nov.', 'de dec.']
    return f'{weekday_names[weekday_idx]}, {d} {de_month_names[m-1]} de {y}'


def weekday_from_date(date):
    """Date in format 'dd/mm/yyyy' or (d, m, y) to weekday (mon:0, sun:6)."""
    if isinstance(date, str):
        date = date_str_to_tuple(date)
    return ddate(date[2], date[1], date[0]).weekday()


def date_str_to_tuple(date_str):
    """Date in format (str) dd/mm/yyyy to (list[int]) (d, m, y)."""
    return (int(date_str[:2]), int(date_str[3:5]), int(date_str[6:]))


def format_import(amount):
    """Format import to show with green/red badge and +/- sign."""
    import_str = ':green[+' if amount > 0 else ':red[-'
    import_str += f'{abs(amount):.2f}' + ']'
    return import_str


def get_start_end_of_series(series):
    """Get start and end date of given pd.series with dates DD/MM/YYYY."""
    datetimes = pd.to_datetime(series, format='%d/%m/%Y')
    start = datetimes.min().strftime('%d/%m/%Y')
    end = datetimes.max().strftime('%d/%m/%Y')
    return start, end