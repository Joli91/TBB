import streamlit as st
import pandas as pd
from data_methods import bad_word_count, bad_ads_and_words, bar_chart_st
import altair as alt


# Syftestext input
with open('Data/syftestext.txt', 'r', encoding='utf-8') as g:
    syftestext = g.read()

# Load data
df = pd.read_json('Data/Testfil_FINAL.json')


# Kod för att gömma index kolumnen i tables. Fungerar ej för dataframes i senaste streamlit version
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

##############################

# Title
st.title('The Bouncing Benjamins 🏀')

## Syfte
st.header('Syfte')
# Syftestext
st.markdown(f'<span style="word-wrap:break-word;">{syftestext}</span>', unsafe_allow_html=True)

st.divider()
# Kolumner    
col1, col2, col3 = st.columns([1,1,1])


with col3:

    # Interatkivitet
    # Slider för år
    min_value = df['publication_date'].min()
    max_value = df['publication_date'].max()

    year_interval = st.slider('Välj år', min_value=int(min_value), max_value=int(max_value), value=(2016, 2017))
    st.write('Vald tidsintervall:', year_interval[0],'-',year_interval[1])

    # Selectbox för yrkesroll
    occupation_group_list = df['occupation_group_label'].unique().tolist()
    occupation_group_list.insert(0, 'Alla')
    occupation_group = st.selectbox('Välj yrkesroll:', occupation_group_list, )

    # Konverterar valet av yrkesroll till en lista för att fungera med filtret
    if occupation_group == 'Alla':
        occupation_group = occupation_group_list
    else:
        occupation_group = [occupation_group]

    # Filter appliceras innan datan skickas in i metoder
    filter = (df['publication_date'] >= year_interval[0]) & (df['publication_date'] <= year_interval[1]) & (df['occupation_group_label'].isin(occupation_group))

     # Filtrerar datasetet enligt interaktiva val i appen
    job_ads = df[filter]
    ##############################

    #Visa bar chart via stremlit istället för matplotlib
    green, yellow, red = bar_chart_st(job_ads)
    chart_data = pd.DataFrame({'Antal annonser': [green, yellow, red]}, index=['Green', 'Yellow', 'Red'])
    colors = ['#32CD32', '#FFC107', '#FF0000']
    bars = alt.Chart(chart_data.reset_index()).mark_bar().encode(x='index', y='Antal annonser', color=alt.Color('index', scale=alt.Scale(domain=['Green', 'Yellow', 'Red'], range=colors))).properties(width=400, height=300)

    st.altair_chart(bars)

with col1:
    
    # Sektion för Total inom IT    
    st.header('Total inom IT')
    bad_ads = bad_ads_and_words(job_ads)
    st.table(bad_ads)
    
with col2:
    # Sektion för dåliga ord
    st.header('Dåliga ord:')
    bad_words = bad_word_count(job_ads)
    st.table(bad_words)
    ##############################

    


    


st.header('AI analys')







