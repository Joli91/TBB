import streamlit as st
import pandas as pd
from data_methods import bad_word_count, bad_ads_and_words, bar_chart_st, generate_rephrased_sentences, bubble_chart
import altair as alt
import plotly.express as px

st.set_page_config(layout="wide")

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
st.header('- Mångfald och jämställdhet i IT-branschen')
## Syfte
st.header('Syfte')
# Syftestext
st.markdown(f'<span style="word-wrap:break-word;">{syftestext}</span>', unsafe_allow_html=True)

st.divider()

#Sidebar för filtrering
with st.sidebar:    
    # Interatkivitet
    # Slider för år
    min_value = df['publication_date'].min()
    max_value = df['publication_date'].max()

    year_interval = st.slider('Välj år', min_value=int(min_value), max_value=int(max_value), value=(2016, 2023))
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
    
st.header('Överblick')
# Skapa kolumner    
outer_col1, outer_col2 = st.columns([1, 1], gap="medium")

with outer_col1:
    # Sektion för dåliga ord
    st.subheader('Missgynnande ord: ')
    bad_words = bad_word_count(job_ads)
    st.table(bad_words)
    ##############################
    
with outer_col2:
    # Sektion för Total inom IT    
    st.subheader('Urval:')
    bad_ads = bad_ads_and_words(job_ads)
    st.table(bad_ads)

    #Visa bar chart via stremlit istället för matplotlib
    green, yellow, red = bar_chart_st(job_ads)
    chart_data = pd.DataFrame({'Antal annonser': [green, yellow, red]}, index=['Förekommer aldrig', 'Förekommer sällan', 'Förekommer ofta'])
    colors = ['#32CD32', '#FFC107', '#FF0000']
    bars = alt.Chart(chart_data.reset_index()).mark_bar().encode(x='index', y='Antal annonser', color=alt.Color('index', scale=alt.Scale(domain=['Förekommer aldrig', 'Förekommer sällan', 'Förekommer ofta'], range=colors))).properties(width=400, height=350)

    st.altair_chart(bars)

st.divider()
##########################

st.header('Dataanalys')

# Display the bubble chart
fig = bubble_chart(job_ads)
st.plotly_chart(fig)

#kod för att köra chatgpt funktionen
# Load CSV file into DataFrame
df_gpt = pd.read_csv('Data/keyword_sentence_similarity.csv')
# Get unique values from the "keyword" column
keywords = df_gpt["Keyword"].unique()

# Create select box
selected_keyword = st.selectbox("Välj ord:", keywords)

filtered_df_gpt = df_gpt[df_gpt['Keyword'] ==  selected_keyword].reset_index(drop=True)

st.header('De tre vanligaste kontexterna där ordet "' + str(selected_keyword) + '" förekommer:')

if not st.button("Generera omformulerade meningsförslag"):
    for index, row in filtered_df_gpt.iterrows():
        st.markdown(f"<span style='color:orange'>{index+1}: {row['Sentence']}</span>", unsafe_allow_html=True)
else:
    if len(filtered_df_gpt) > 0:
        # Get rephrased sentences for all rows
        rephrased_sentences = [generate_rephrased_sentences(row['Sentence'], selected_keyword) for _, row in filtered_df_gpt.iterrows()]
            
        for index, row in filtered_df_gpt.iterrows():
            st.markdown(f"<span style='color:orange'>{index+1}: {row['Sentence']}</span>", unsafe_allow_html=True)

            # Check if the current row index is within the rephrased sentences range
            if index < len(rephrased_sentences):
                # Iterate over rephrased sentences for the current row
                for rephrased_sentence in rephrased_sentences[index]:
                    st.markdown(f"<span style='color:green'>{rephrased_sentence}</span>", unsafe_allow_html=True)
    else:
        st.text("No rows found.")

######################################
st.divider()

#Länkar till fornötter från syftestext
st.write ("Länkar till fotnoter: ")

markdown_text = "[¹Streamlit](https://streamlit.io/) [²Github](https://github.com/) [³Negativ](https://www.synonymer.se/sv-syn/negativ)"

st.markdown(markdown_text)