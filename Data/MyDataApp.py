import streamlit as st
import pandas as pd
import json
from data_methods import bad_word_count, bad_ads_and_words



# Syftestext input
with open('Data/syftestext.txt', 'r', encoding='utf-8') as g:
    syftestext = g.read()
syftestext = 'Studien som verktyget är framtaget ur kartlägger stora mångfalds- och jämställdhestklyftor inom IT-branschen i Sverige idag. Det som undersökts är den ojämna fördelningen mellan män och kvinnor inom branschen samt vad detta kan bero på. Samtidigt lider IT-branschen av stor kompetensbrist vilket delvis kan spåras tillbaka till bristen på kvinnor inom IT. Verktyget visualiserar data från ett öppet dataset, tillgängliggjort av JobTech, angående arbetsannonser under perioden 2016-2023. Genom (vilken metod vi använt oss av, NLP, Klustring osv) analyserar verktyget användningen av särskilda ord i annonserna. De valda orden är enligt studier* definierade att påverka i vilken utsträckning kvinnor söker jobb beroende på ordens förekomst i annonsen. Syftet med verktyget är att sprida kunskap samt skapa medvetenhet kring hur man som arbetsgivare kan anpassa formuleringen av sina arbetsannonser. Genom att undvika användningen av dessa ord är vår förhoppning att rekrytera fler kvinnor till IT-branschen för att skapa en mer jämställd och mångfaldig bransch.'

# Load data
df = pd.read_json('Data/Testfil_FINAL.json')

with open('Data/Testfil_FINAL.json', 'r', encoding='utf-8') as f:
    job_ads = json.load(f)

# Koden nedan hämtar bara 3 variabler från JSON-filen (förhoppningsvis snabbare vid större JSON-fil)
#with open('Data/Testfil_FINAL.json', 'r', encoding='utf-8') as f:
#    job_ads = json.load(f, object_hook=lambda d: {k: v for k, v in d.items() if k in ('description.text', 'occupation_group.label', 'Bad_words')})

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

    year_interval = st.slider('Välj år', min_value=int(min_value), max_value=int(max_value), value=(2016, 2023))
    st.write('Vald tidsintervall:', year_interval[0],'-',year_interval[1])

    # Selectbox för yrkesroll
    occupation_group_list = df['occupation_group.label'].unique().tolist()
    occupation_group_list.insert(0, 'Alla')
    occupation_group = st.selectbox('Välj yrkesroll:', occupation_group_list, )

    # Konverterar valet av yrkesroll till en lista för att fungera med filtret
    if occupation_group == 'Alla':
        occupation_group = occupation_group_list
    else:
        occupation_group = [occupation_group]

    # Filter appliceras innan datan skickas in i metoder
    filter = (df['publication_date'] >= year_interval[0]) & (df['publication_date'] <= year_interval[1]) & (df['occupation_group.label'].isin(occupation_group))

    job_ads = df[filter]
    ##############################

with col1:
    
    # Sektion för Total inom IT
    st.header('Total inom IT')
    bad_ads = bad_ads_and_words(job_ads)
    st.table(bad_ads)
    ##############################

with col2:
    # Sektion för dåliga ord
    st.header('Dåliga ord:')
    bad_words = bad_word_count(job_ads)
    st.table(bad_words)
    ##############################

    


    


st.header('AI analys')







