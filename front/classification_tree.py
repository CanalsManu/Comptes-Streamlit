import streamlit as st
ss = st.session_state

db = st.session_state.get('db', None)

if db is not None:

    st.header('Mostra l\'esquema de classificació')
    # st.write(st.session_state['clsf_tree'])

    # Prova plotly
    import plotly.express as px
    df = px.data.tips()
    print('\n'*5)
    print(px.data.gapminder().query("year == 2007"))
    print(df)
    print(ss['clsf_dashed'])
    print(ss['clsf_dashed'].str.split('-', expand=True))
    print('\n'*5)

    # fig = px.treemap(df, path=[px.Constant("all"), 'day', 'time', 'sex'], values='total_bill')
    fig = px.treemap(
        ss['clsf_df'],
        path=[0, 1, 2]
    )
    fig.update_traces(root_color="lightgrey", marker=dict(cornerradius=5))
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    # fig.show()

    st.plotly_chart(fig)
    st.write('End.')
    
else:
    st.write('No file uploaded.')
