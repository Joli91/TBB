import streamlit as st
import pandas as pd
from data_methods import bad_word_count, bad_ads_and_words, bar_chart_st, generate_rephrased_sentences, bubble_chart, bad_word_count2, create_treemap
import altair as alt
import plotly.express as px
import re
import squarify
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sb
from wordcloud import WordCloud

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
    #Länkar till fornötter från syftestext
    st.write ("Länkar till fotnoter: ")
    markdown_text = "[¹JobTech](https://jobtechdev.se/sv) [²Gaucher,Friesen,Kay-2011](https://ideas.wharton.upenn.edu/wp-content/uploads/2018/07/Gaucher-Friesen-Kay-2011.pdf?fbclid=IwAR0JFSPgZP3olTZG5d-_B4KvOI5msLjxaE9wH_fiKY8nQHtXlVNRzh940DE) [³Tietoevry](https://www.tietoevry.com/se/nyhetsrum/alla-nyheter-och-pressmeddelanden/pressmeddelande/2021/06/ordval-i-jobbannonser-star-i-vagen-for-kvinnor-i-it-branschen--sa-okade-tietoevry-antalet-kvinnliga-sokanden/?fbclid=IwAR0wdO3vI1KfTr7aqq7-7p3QhiW4UkSbszoUBWqEexzMwmtK43SgL0KMCOY)"
    st.markdown(markdown_text)

    ##############################
    
st.header('Överblick')
# Skapa kolumner    
outer_col1, outer_col2 = st.columns([1, 1], gap="medium")

with outer_col1:
    # Sektion för dåliga ord
    st.subheader('Missgynnande ord: ')

    # Wordcloud 
    def create_wordcloud(data):
        # Combine all words into a single string
        words = ' '.join(data['Ord'])

        # Create a word cloud object with custom attributes
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color=None,
            mode='RGBA',
            colormap='Spectral',
            max_words=100,
            max_font_size=150
        )

        # Generate the word cloud
        wordcloud.generate(words)

        # Display the word cloud using matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        #ax.set_title('Word Cloud') # titeltext för wordcloud

        fig.set_frameon(False)

        # Display the plot within Streamlit
        st.pyplot(fig)

    # Call the function to create the word cloud
    create_wordcloud(bad_words)


    ## Gamla dataframe som innehåller count av missgynnande ord
    #st.dataframe(bad_words)

    
    treemap_fig = create_treemap(bad_words) # kallar treemap metoden
    st.pyplot(treemap_fig) # plot treemap

    bad_words2 = bad_word_count2(job_ads)

    ######################################
    ######## BAR CHART FOR BAD WORDS########
    def bad_word_count_2(job_ads):
        target_words = []

        with open("Data/ordlista.txt", "r", encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            words = line.split()
            for word in words:
                target_words.append(word)

        word_counts = {}
        for index, ad in job_ads.iterrows():
            ad_text = ad['description_text'].lower().replace('.', ' ')
            for target_word in target_words:
                count = len(re.findall(r'\b{}\b'.format(target_word), ad_text))
                if target_word in word_counts:
                    word_counts[target_word] += count
                else:
                    word_counts[target_word] = count

        word_counts_df = pd.DataFrame.from_dict(word_counts, orient='index', columns=['Count'])
        word_counts_df.reset_index(inplace=True)
        word_counts_df.columns = ['Word', 'Count']

        # Melt the DataFrame to convert it to long format
        melted_df = pd.melt(job_ads, id_vars='occupation_group_label', value_vars=target_words, var_name='Word', value_name='Count')
        summed_df = melted_df.groupby(['occupation_group_label', 'Word']).sum().reset_index()

        # Merge word counts with summed counts
        merged_df = pd.merge(summed_df, word_counts_df, on='Word')

        # Create the Altair chart
        chart = alt.Chart(merged_df).mark_bar().encode(
            y='occupation_group_label',
            x=alt.X('sum(Count_x)', stack='normalize'),
            color=alt.Color('Word', scale=alt.Scale(scheme='category20'))
        ).properties(
            width=600
        )

        return chart
    
    bad_words_bar_chart = bad_word_count_2(job_ads)
    st.altair_chart(bad_words_bar_chart, use_container_width=True)

    ##############################
 
    

    ##############################
    
with outer_col2:
    # Sektion för Total inom IT    
    st.subheader('Urval:')
    bad_ads = bad_ads_and_words(job_ads)
    st.table(bad_ads)
    gammal_bar_chart_placeholder = ('''
    #Visa bar chart via stremlit istället för matplotlib
    green, yellow, red = bar_chart_st(job_ads)
    chart_data = pd.DataFrame({'Antal annonser': [green, yellow, red]}, index=['Aldrig', 'Sällan', 'Ofta'])
    colors = ['#32CD32', '#FFC107', '#FF0000']
    
    bars = alt.Chart(chart_data.reset_index()).mark_bar().encode(
        x=alt.X('index', title='Ordens förekomst'), y=alt.Y('Antal annonser', title='Antal annonser'), 
        color=alt.Color('index', title= 'Ordens förekomst', scale=alt.Scale(domain=['Aldrig', 'Sällan', 'Ofta'], range=colors))
        ).properties(width=400, height=350)

    st.altair_chart(bars)''')
    

    ## Stackad bar chart grön gul röd

        # Custom color mapping function
    def get_color(value):
        if value == 0:
            return 'green'
        elif value == 1:
            return 'yellow'
        elif value > 1:
            return 'red'

    # Apply color mapping function to create a new 'color' column
    job_ads['color'] = job_ads['Bad_words'].apply(get_color)

    # Calculate the count of rows with bad words
    job_ads['Row_count'] = job_ads['Bad_words'].apply(lambda x: 1 if x > 0 else 0)

    # Clone the DataFrame and select specific columns
    df_total = job_ads[['Bad_words', 'color', 'Row_count']].copy() 

    # Replace values in the 'occupation_group_label' column with 'Total'
    df_total['occupation_group_label'] = 'Totalt'

    # Concatenate the total DataFrame with the original DataFrame
    df_combined = pd.concat([job_ads, df_total])

    
    legend_values = ['green', 'yellow', 'red']
    # Sort the DataFrame by the percentage of green bars in descending order
    df_combined = df_combined.sort_values(by='color', ascending=False)

    chart1 = alt.Chart(df_combined).mark_bar().encode( #Chart 1 endast för att visa customizable legend
        y=alt.Y('occupation_group_label', sort=alt.EncodingSortField(field='color', op='count', order='descending'), axis=alt.Axis(title='Yrkesgrupp')),
        x=alt.X('count(Row_count)',stack='normalize', axis=alt.Axis(format='%', title='Andel')),
        color=alt.Color('color',
            scale=alt.Scale(domain=['Aldrig     0', 'Sällan    1', 'Ofta      >1'],
                range=['Green', 'Yellow', 'Red']),
            sort=['yellow', 'red', 'green'],
            legend=alt.Legend(title='Förekomst per annons', labelFontSize=12, titleFontSize=14, symbolType='square', symbolSize=300))  # Set custom color scale and legend
        ).properties(height=400, title='Ordens förekomst').interactive()

    chart2 = alt.Chart(df_combined).mark_bar().encode(
        y=alt.Y('occupation_group_label', sort=alt.EncodingSortField(field='color', op='count', order='descending'), axis=alt.Axis(title='Yrkesgrupp')),
        x=alt.X('count(Row_count)',stack='normalize', axis=alt.Axis(format='%', title='Andel')),
        color=alt.Color('color',
            scale=None)
         # tooltip placeholder. Fungerar inte med procentandel atm
        #tooltip=[
        #    alt.Tooltip('occupation_group_label', title='Ykesgrupp'),
        #    alt.Tooltip('count(Row_count)', title='Andel', format='.2%'),
        #    alt.Tooltip('color', title='Förekomst')
        #]
        ).properties(height=400, title='Ordens förekomst').interactive()

    # Layera charts
    combined_chart = chart1 + chart2
    
    # Display the chart
    st.altair_chart(combined_chart, use_container_width=True)

   ###### LINE CHART#############

def line_chart_func(job_ads):
    target_words = []
    with open("Data/ordlista.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        words = line.split()
        for word in words:
            target_words.append(word)
    word_counts = {}
    for index, ad in job_ads.iterrows():
        ad_text = ad['description_text'].lower().replace('.', ' ')
        for target_word in target_words:
            count = len(re.findall(r'\b{}\b'.format(target_word), ad_text))
            if target_word in word_counts:
                word_counts[target_word].append(count)
            else:
                word_counts[target_word] = [count]
    for target_word, counts in word_counts.items():
        job_ads[target_word] = counts
    # Convert the 'publication_date' column to datetime
    job_ads['publication_date'] = pd.to_datetime(job_ads['publication_date'], format='%Y')
    # Melt the DataFrame to convert it to long format
    melted_df = pd.melt(job_ads, id_vars=['publication_date'], value_vars=target_words, var_name='Word', value_name='Count')
    summed_df = melted_df.groupby(['publication_date', 'Word']).sum().reset_index()
    # Create the Altair line chart
    chart = alt.Chart(summed_df).mark_line().encode(
        x=alt.X('year(publication_date):O', axis=alt.Axis(format='%Y', title='Publication Year')),
        y=alt.Y('sum(Count):Q', title='Count'),
        color='Word:N'
    ).properties(
        width=600
    )
    return chart

st.divider()
##### Visa line chart
line_chart = line_chart_func(job_ads)
st.altair_chart(line_chart, use_container_width=True)
##########################
st.divider()
##########################

st.header('Dataanalys')

st.write ("Sentiment är en analys som visar negativ, neutral och positiv inverkan på kontexten som ordet befinner sig i. Där av stärker vi studierna i att visa att dessa ord påverkar arbetsannonsernas uppfattning.")

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