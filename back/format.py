import streamlit as st
from datetime import date as ddate
import pandas as pd

def build_clsf_badges(classification, amount = None):
    """
    Get md string to render dashed classification as badges with arrows.
    
    amount is used when classification is None.
    """

    # Get info
    if isinstance(classification, str):
        show_res = classification
    else:
        assert amount is not None  # amount must be given here
        show_res = 'despeses-' if amount <= 0 else 'ingressos-'

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


def format_dataframe(df, columns, formats):
    """Iteratiely apply function in formats to column name in columns."""
    assert len(columns) == len(formats)

    formated = df.copy()
    for col_name, format_func in zip(columns, formats):
        formated[col_name] = formated[col_name].apply(format_func)

    return formated


def format_database(db,
                    fdate = format_date, fname = lambda x: x,
                    fimport = format_import, fcategories = build_clsf_badges):
    """
    Wrap format_dataframe() for df with Data, Nom, Import and Categories.
    
    Expected input formats in db:
        - data: (str) dd/mm/yyyy
        - nom: (str) any
        - import: (float) any
        - categories: (str) DASHED categories
    """
    return format_dataframe(
        db,
        columns=['Data', 'Nom', 'Import', 'Categories'],
        formats=[fdate, fname, fimport, fcategories]
    )


def show_move_w_calendar(move):
    """Show move with calendar (left col) and formated info (right col)."""
    move_cols = st.columns(2)

    with move_cols[0]:
        date = date_str_to_tuple(move['Data'])
        month_calendar(date[1], date[2], hightlight=date[0])

    with move_cols[1]:
        cont = st.container(vertical_alignment='center', height='stretch')
        cont.write(move['Nom'])
        cont.write(format_import(move['Import']))


def month_calendar(month, year, hightlight=None):
    """Month: int from 1 to 12 (inclusive). highlight (optional) day (int)."""
    # Formats
    off_month = ':gray-badge[····]'
    off_month = ':gray-badge[&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]'
    in_month = ':gray-badge[ {:02} ]'
    curr_day = ':primary-badge[ {:02} ]'
    week_name = ':primary-badge[{}]'

    # Set up
    assert 1 <= month <= 12 
    month_days = days_in_month(month, year)
    def write_week(week, sep=''):
        week.insert(5, '|')
        st.markdown(sep.join(week), text_alignment='center')

    # Prepare week names
    names = ['  dl', 'dt', 'dc', 'dj', 'dv', 'ds', 'dg']
    names = ['DL', 'DT', 'DC', 'DJ', 'DV', 'DS', 'DG']
    week_names = [week_name.format(d) for d in names]

    # Build first week
    first_weekday = weekday_from_date((1, month, year))  # mon: 0, sun: 6
    first_week = [off_month] * first_weekday
    first_week += [in_month.format(n) for n in range(1, 7 - first_weekday + 1)]

    # Container with multiple markdowns
    month_cont = st.container(horizontal=False, horizontal_alignment='center',
                             gap=None, vertical_alignment='center',
                             width='stretch', border=False)
    with month_cont:

        # Write header and first week
        spacing = ' ' * 30
        st.text(month_name(month).upper() + spacing + str(year), 
                text_alignment='center')
        
        # If given, highlight day
        if hightlight is None:
            pass
        elif 1 - first_weekday <= hightlight <= 7 - first_weekday:
            first_week[hightlight - 1 + first_weekday] = curr_day.format(hightlight)
        write_week(first_week)

        # Rest of the month
        for start_day in range(8 - first_weekday, month_days, 7):
            # Build week
            days_in_week = min(month_days - start_day, 7)
            week = [in_month.format(n)
                    for n in range(start_day, start_day+days_in_week)]
            week += [off_month] * (7 - days_in_week)

            # If given, highlight day
            if hightlight is None:
                pass
            elif start_day <= hightlight <= start_day + days_in_week - 1:
                week[hightlight - start_day] = curr_day.format(hightlight)

            write_week(week)
   

def days_in_month(month, year):
    """month: int from 1 to 12 (inclusive)."""
    assert 1 <= month <= 12
    if month == 12:
        return 31
    return (ddate(year, month+1, 1) - ddate(year, month, 1)).days + 1
   

def month_name(month):
    """month: int from 1 to 12 (inclusive)."""
    assert 1 <= month <= 12
    names = ['Gener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny',
             'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Decembre']
    return names[month-1]

