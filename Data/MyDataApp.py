import streamlit as st
import pandas as pd
from data_methods import *
import altair as alt
import plotly.express as px
import re
import squarify
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sb



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
    #count av missgynnande ord returnerar df 
    bad_words = bad_word_count(job_ads)
    bad_words_adv = bad_word_count_adv(job_ads) # behövs för bad words bar och line chart 


    st.divider()

    # Navigeringslänkar:
    st.markdown('''
    Sektioner
    - [Syfte](#syfte)
    - [Överblick](#urval)
    - [Sentimentanalys](#dataanalys)
    - [Förslag](#mening)
    ''', unsafe_allow_html=True)


    
    #Tom text för att flytta ner fotnoter
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    st.title('')
    #Länkar till fornötter från syftestext
    st.write ("Länkar till fotnoter: ")
    markdown_text = "[¹JobTech](https://jobtechdev.se/sv) [²Gaucher et al (2011)](https://ideas.wharton.upenn.edu/wp-content/uploads/2018/07/Gaucher-Friesen-Kay-2011.pdf) [³Tietoevry](https://www.tietoevry.com/se/nyhetsrum/alla-nyheter-och-pressmeddelanden/pressmeddelande/2021/06/ordval-i-jobbannonser-star-i-vagen-for-kvinnor-i-it-branschen--sa-okade-tietoevry-antalet-kvinnliga-sokanden/)"
    st.markdown(markdown_text)

    ##############################
    
st.header('Överblick')




# Skapa kolumner    
outer_col1, outer_col2 = st.columns([1, 1], gap="medium")

with outer_col1:
    # Sektion för dåliga ord
    st.subheader('Missgynnande ord: ')



    ## Gamla dataframe som innehåller count av missgynnande ord
    #st.dataframe(bad_words)




    ##############################
    # Wordcloud 
    # Call the function to create the word cloud
    wordcloud_fig = create_wordcloud(bad_words)
    st.pyplot(wordcloud_fig)

    

    ##############################
    
with outer_col2:
    # Sektion för Total inom IT    
    st.subheader('Urval:')
    #bad_ads = bad_ads_and_words(job_ads) # gamla tabellen för snitt och andel dåliga annonser
    #st.table(bad_ads)

    

    ## Stackad bar chart grön gul röd
    def rgy_bar_chart(job_ads):
        '''flytta till data_methods när fixad'''
            # Custom color mapping function
        def get_color(value):
            if value == 0:
                return 'Aldrig'
            elif value == 1:
                return 'Ibland'
            elif value > 1:
                return 'Ofta'
            
        # Define custom color schemes
        red_color = "#8B0000"  # Dark red
        yellow_color = "#8B8B00"  # Dark yellow
        green_color = "#006400"  # Pleasing green

        # Apply color mapping function to create a new 'color' column
        job_ads['Förekomst'] = job_ads['Bad_words'].apply(get_color)

        # Calculate the count of rows with bad words
        job_ads['Row_count'] = job_ads['Bad_words'].apply(lambda x: 1 if x > 0 else 0)

        # Clone the DataFrame and select specific columns
        df_total = job_ads[['Bad_words', 'Förekomst', 'Row_count']].copy() 

        # Replace values in the 'occupation_group_label' column with 'Total'
        df_total['occupation_group_label'] = 'Totalt'
        df_total['occupation_label'] = 'Totalt' # Lade till för att se Totalt ist för null //Kim

        # Concatenate the total DataFrame with the original DataFrame
        df_combined = pd.concat([job_ads, df_total])

        
        legend_values = ['Aldrig', 'Ibland', 'Ofta']
        # Sort the DataFrame by the percentage of green bars in descending order
        df_combined = df_combined.sort_values(by='Förekomst', ascending=False)


        # Calculate the percentage of greens relative to reds and yellows within each occupation_group_label
        df_combined['green_percentage'] = df_combined.groupby('occupation_group_label')['Förekomst'].transform(
            lambda x: (x == 'Aldrig').mean())

        # Sort the DataFrame based on the green_percentage in descending order
        df_sorted = df_combined.sort_values(by='green_percentage', ascending=True)

        # Extract the list of values in the occupation_group_label column
        occupation_group_labels = df_sorted['occupation_group_label'].unique().tolist()


        #Chart 1 endast för att visa customizable legend
        chart1 = alt.Chart(df_combined).mark_bar().encode( 
            y=alt.Y('occupation_group_label', sort=alt.EncodingSortField(field='Förekomst', op='count', order='descending'), axis=alt.Axis(title='Yrkesgrupp')),
            x=alt.X('count(Row_count)',stack='normalize', axis=alt.Axis(format='%', title='Andel')),
            color=alt.Color('Förekomst',
                scale=alt.Scale(domain=['Aldrig     0', 'Ibland    1', 'Ofta      >1'],
                    range=['Aldrig', 'Ibland', 'Ofta']),
                sort=['Ibland', 'Ofta', 'Aldrig'],
                legend=alt.Legend(title='Förekomst per annons', labelFontSize=12, titleFontSize=14, symbolType='square', symbolSize=300))  # Set custom color scale and legend
            ).properties(height=400).interactive()


        # Define the desired order of colors
        color_order = ['Aldrig', 'Ibland', 'Ofta']  # sets color of bars
        bar_order = ['Ofta', 'Ibland', 'Aldrig'] # sätter ordning på färger i bars. Är av någon anledning reversed.


        # Chart 2 visar faktisk data
        if 'Alla' in occupation_group: # Lade till if statement för att se jobbtitlar //Kim
            chart2 = alt.Chart(df_combined).transform_calculate(
                order=f"-indexof({bar_order}, datum.Förekomst)"
            ).mark_bar().encode(
                y=alt.Y('occupation_group_label', 
                        sort=occupation_group_labels , # sorterar y axeln på count av ordens förekomst
                        axis=alt.Axis(title='Yrkesgrupp')),
                x=alt.X('count(Row_count)', stack='normalize', axis=alt.Axis(format='%', title='Andel')),
                color=alt.Color('Förekomst', 
                                scale=alt.Scale(domain=color_order, 
                                range=[green_color, yellow_color, red_color]),
                                sort=bar_order),
                                order="order:Q"
            ).properties(height=400, 
                         #title='Ordens förekomst'
                         ).interactive()
        else: # Lade till if statement för att se jobbtitlar //Kim
            chart2 = alt.Chart(df_combined).transform_calculate(
                order=f"-indexof({bar_order}, datum.Förekomst)"
            ).mark_bar().encode(
                y=alt.Y('occupation_label', 
                        sort=occupation_group_labels , # sorterar y axeln på count av ordens förekomst
                        axis=alt.Axis(title='Yrkesgrupp')),
                x=alt.X('count(Row_count)', stack='normalize', axis=alt.Axis(format='%', title='Andel')),
                color=alt.Color('Förekomst', 
                                scale=alt.Scale(domain=color_order, 
                                range=[green_color, yellow_color, red_color]),
                                sort=bar_order),
                                order="order:Q"
            ).properties(height=400, title='Ordens förekomst').interactive()

            # tooltip placeholder. Fungerar inte med procentandel atm
            # tooltip=[
            #     alt.Tooltip('occupation_group_label', title='Ykesgrupp'),
            #     alt.Tooltip('count(Row_count)', title='Andel', format='.2%'),
            #     alt.Tooltip('color', title='Förekomst')
            # ]

        # Layera charts
        #combined_chart = chart1 + chart2
        combined_chart = chart2

        return combined_chart
    
    # Display the chart
    red_green_yellow_chart = rgy_bar_chart(job_ads)
    st.altair_chart(red_green_yellow_chart, use_container_width=True)


    ######### LINE CHART ########
line_chart = bad_word_line_chart(job_ads)
st.altair_chart(line_chart, use_container_width=True)
##########################
st.divider()
##########################

st.header('Dataanalys')

st.write ("Sentiment är en analys som visar negativ, neutral och positiv inverkan på kontexten som ordet befinner sig i. Där av stärker vi studierna i att visa att dessa ord påverkar arbetsannonsernas uppfattning.")

# Display the bubble chart
fig = bubble_chart(job_ads)
st.plotly_chart(fig, use_container_width=True)

#kod för att köra chatgpt funktionen
# Load CSV file into DataFrame
df_gpt = pd.read_csv('Data/keyword_sentence_similarity.csv')
# Get unique values from the "keyword" column
keywords = df_gpt["Keyword"].unique()

# Create select box
selected_keyword = st.selectbox("Välj ord:", keywords, key='ordval')

filtered_df_gpt = df_gpt[df_gpt['Keyword'] ==  selected_keyword].reset_index(drop=True)
st.header('mening')
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