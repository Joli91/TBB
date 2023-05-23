import streamlit as st
import pandas as pd
from data_methods import *
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sb
import streamlit as st

ordlista = ['stark', 'drivkraft', 'chef', 'analys', 'analytisk', 'driven', 'individer', 'beslut', 'kompetent', 'självständig']

st.set_page_config(layout="wide")

#Kort intro text
with open('Data/intro.txt', 'r', encoding='utf-8') as g:
    intro = g.read()

# Load data
df = pd.read_csv('Data/Hela_datan.csv')


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
st.title('- Mångfald och jämställdhet inom IT-branschen')
# Introtext
st.markdown(f'<span style="word-wrap:break-word;">{intro}</span>', unsafe_allow_html=True)

st.divider()

#Sidebar för filtrering
with st.sidebar:    
    st.write('Ett verktyg av:  The Bouncing Benjamins 🏀')
    
    # Interatkivitet
    # Slider för år
    min_value = df['publication_date'].min()
    max_value = df['publication_date'].max()

    year_interval = st.slider('Välj år', min_value=int(min_value), max_value=int(max_value), value=(2016, 2023))
    st.write('Vald tidsintervall:', year_interval[0],'-',year_interval[1])

    # Selectbox för yrkesroll
    occupation_group_list = df['occupation_group_label'].unique().tolist()
    occupation_group_list.insert(0, 'Alla')
    occupation_group = st.selectbox('Välj yrkesgrupp:', occupation_group_list, )

    # Konverterar valet av yrkesroll till en lista för att fungera med filtret
    if occupation_group == 'Alla':
        occupation_group = occupation_group_list
    else:
        occupation_group = [occupation_group]

    # Filter appliceras innan datan skickas in i metoder
    filter = (df['publication_date'] >= year_interval[0]) & (df['publication_date'] <= year_interval[1]) & (df['occupation_group_label'].isin(occupation_group))

    # Filtrerar datasetet enligt interaktiva val i appen
    job_ads = df[filter]
    #count av missgynnande ord returnerar df 
    bad_words = bad_word_count(job_ads, ordlista)

    st.divider()


    #Tom text för att flytta ner fotnoter
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')


    st.divider()
    
    #Länkar till fornötter från syftestext
    st.write ("Länkar till fotnoter: ")
    markdown_text = "[¹Tietoevry](https://www.tietoevry.com/se/nyhetsrum/alla-nyheter-och-pressmeddelanden/pressmeddelande/2021/06/ordval-i-jobbannonser-star-i-vagen-for-kvinnor-i-it-branschen--sa-okade-tietoevry-antalet-kvinnliga-sokanden/) [²JobTech](https://jobtechdev.se/sv) [³Gaucher et al (2011)](https://ideas.wharton.upenn.edu/wp-content/uploads/2018/07/Gaucher-Friesen-Kay-2011.pdf)"
    st.markdown(markdown_text)
    ##############################
    
st.header('Förekomst av orden ')
st.title('')

# Skapa kolumner 
outer_col3, outer_col4, outer_col5 = st.columns([2, 1, 1], gap="medium")
outer_col1, outer_col2 = st.columns([1, 1], gap="medium")

with outer_col3:
    st.write('Verktyget visualiserar data från ett öppet dataset, tillgängliggjort av JobTech², angående arbetsannonser under perioden 2016-2023.')

with outer_col4:
    

    def calculate_bad_words_percentage(df):
        '''ersätter gamla bad_ads_and_words :) '''
        total_rows = len(df)
        bad_words_rows = len(df[df['Bad_words'] > 0])
        percentage = (bad_words_rows / total_rows) * 100
        filtered_df = df[df['Bad_words'] > 0]  # Filter rows with values greater than 0
        mean_number = round(filtered_df['Bad_words'].mean(), 1)  # Calculate mean number
        return int(percentage), mean_number

        
    percentage, mean_number = calculate_bad_words_percentage(job_ads)

    snitt_procent = 45 # snitt på totala datan används för att visa skillnader i metric vid filtrering
    snitt_bad_words = 1.5 # snitt på totala datan används för att visa skillnader i metric vid filtrering
    
    ##### KPI ######
    delta_color = 'inverse' if percentage != snitt_procent else 'off'
    st.metric(label='Annonser med missgynnande ord', 
              value=(f"{percentage}%"), 
              delta=f"{percentage-snitt_procent}%",
              delta_color=delta_color)
with outer_col5:
    delta_color = 'inverse' if mean_number != snitt_bad_words else 'off'
    st.metric(label='Snitt ord / annons', 
              value=mean_number,
              delta=f"{round(mean_number-snitt_bad_words, 1)}",
              delta_color=delta_color)

with outer_col1:
    # Sektion för dåliga ord
    st.subheader('Missgynnande ord ')

    ##############################
    # Wordcloud 
    # Call the function to create the word cloud
    wordcloud_fig = create_wordcloud(bad_words)
    st.pyplot(wordcloud_fig)
    ##############################
    
with outer_col2:
    # Sektion för Total inom IT    
    st.subheader('Fördelning inom yrke ')
    

    ###### RGY CHART ######
    # Display the chart
    red_green_yellow_chart = rgy_bar_chart(job_ads, occupation_group)
    st.altair_chart(red_green_yellow_chart, use_container_width=True)

######### LINE CHART ########
line_chart = bad_word_line_chart(job_ads, ordlista)
st.altair_chart(line_chart, use_container_width=True)
##########################
st.divider()
##########################

st.header('Kontextanalys ')

#Sentiment förklaringstext
with open('Data/sentiment.txt', 'r', encoding='utf-8') as g:
    sentimenttext = g.read()

# Sentiment text
st.markdown(f'<span style="word-wrap:break-word;">{sentimenttext}</span>', unsafe_allow_html=True)

# Display the bubble chart
fig = bubble_chart(job_ads)
st.plotly_chart(fig, use_container_width=True)



bar_chart_data = sentiment_df(job_ads)
bar_chart_sum = bar_chart_data.groupby('Ordval')['Count'].sum().reset_index()

color_map = {'missgynnande ord': 'darkred', 'positiva ord': 'green'}

# Create the Altair chart
chart = alt.Chart(bar_chart_sum).mark_bar().encode(
    x=alt.X('Count', title='Förekomst'),
    y=alt.Y('Ordval', title='Ordtyp'),
    color=alt.Color('Ordval', scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values())))
#).configure_legend(title=None, labelFontSize=0, symbolOpacity=0 # behåller legend men döljer dess innehåll
).configure_legend(disable=True # tar bort legend helt
).properties(width=600) # bredd på chart

# Display the chart using Streamlit
st.altair_chart(chart)


##############
st.divider()

st.header('Förbättringsförslag genom AI')

#kod för att köra chatgpt funktionen
# Load CSV file into DataFrame
df_gpt = pd.read_csv('Data/keyword_sentence_similarity.csv')
# Get unique values from the "keyword" column
keywords = df_gpt["Keyword"].unique()

# Create select box
selected_keyword = st.selectbox("Välj ord:", keywords, key='ordval')
st.title('')

#################

filtered_df_gpt = df_gpt[df_gpt['Keyword'] ==  selected_keyword].reset_index(drop=True)

st.subheader('De tre vanligaste kontexterna där ordet "' + str(selected_keyword) + '" förekommer:')

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

st.header('Verktygets bakgrund ')

#Avslutande syftestext
with open('Data/syftestext.txt', 'r', encoding='utf-8') as g:
    syftestext = g.read()

# Syftestext
st.markdown(f'<span style="word-wrap:break-word;">{syftestext}</span>', unsafe_allow_html=True)

