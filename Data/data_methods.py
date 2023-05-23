import re
import pandas as pd
import altair as alt
import plotly.express as px
import squarify
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sb
from wordcloud import WordCloud
import random


import streamlit as st


def bad_word_count(job_ads):
    '''Summerar antal dåliga ord i datasetet och skapar en sorterad df med antal förekomster av 
    respektive ord'''

    # List of words to count occurrences for
    target_words = []

    with open("Data/ordlista.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        words = line.split()
        for word in words:
            target_words.append(word)

    # Count occurrences of target words
    word_counts = {}
    for index, ad in job_ads.iterrows():
        ad_text = ad['description_text'].lower().replace('.', ' ')
        for target_word in target_words:
            count = len(re.findall(r'\b{}\b'.format(target_word), ad_text))
            if target_word in word_counts:
                word_counts[target_word] += count
            else:
                word_counts[target_word] = count

    # Create a dictionary with the counts of target words
    target_word_counts = {target_word: count for target_word, count in word_counts.items()}

    # Sort the dictionary by its values in descending order
    sorted_dict = dict(sorted(target_word_counts.items(), key=lambda x: x[1], reverse=True))

    df = pd.DataFrame.from_dict(sorted_dict, orient='index', columns=['Count'])
    df = df.reset_index()
    df.columns = ['Ord', 'Antal']
    '''
    df.set_index('Ord', inplace=True)'''

    return df



###########################################################

def bad_ads_and_words(job_ads):
    '''Räknar antal annonser som innehåller dåliga ord, summerar antalet dåliga ord
    och räknar ut ett genomsnitt på antal dåliga ord per dålig annons samt procentsats'''
    bad_ads = 0
    total_bad_words = 0

    for index, ad in job_ads.iterrows():
        if ad['Bad_words'] != 0:
            bad_ads += 1
            total_bad_words += ad['Bad_words']
        else:
            continue

    # Count the average amount of bad words for each job ad
    average_bad_words = total_bad_words / bad_ads
    # Count the percentage of bad ads from total ads
    percentage_bad_ads = str(int(bad_ads / len(job_ads) * 100)) + '%'

    # Create a Pandas DataFrame with the results
    df2 = pd.DataFrame({
        "Snitt negativa ord per annons": [average_bad_words],
        "Andel negativa annonser": [percentage_bad_ads]
    })

    return df2

###########################################################

def filter_years_and_occ_group(df):
    '''funktion för filtrering av data enligt de interaktiva element vi har'''
    return

###########################################################

def sentiment_df(job_ads):
        # Load keyword and sentiment data from CSV
    keyword_df = pd.read_csv("Data/keyword_sentiment.csv")

    # Count occurrences of target words in description_text
    word_counts = {}
    for index, ad in job_ads.iterrows():
        ad_text = ad['description_text'].lower().replace('.', ' ')
        for target_word in keyword_df['Keyword']:
            count = len(re.findall(r'\b{}\b'.format(target_word), ad_text))
            if target_word in word_counts:
                word_counts[target_word] += count
            else:
                word_counts[target_word] = count

    # Create a dataframe with the counts of target words
    df_counts = pd.DataFrame({'Keyword': list(word_counts.keys()), 'Count': list(word_counts.values())})
    
   # Merge keyword_df with the count dataframe on the 'Keyword' column
    merged_df = keyword_df.merge(df_counts, on='Keyword')

    return merged_df

def bubble_chart(data):

    merged_df = sentiment_df(data)

    color_map = {'missgynnande ord': 'red', 'gynnande ord': 'green'}


    # Create bubble chart using Plotly
    fig = px.scatter(merged_df, x='Sentiment', y='Count', size='Count', color='Wordtype', color_discrete_map=color_map, hover_data=['Keyword'])

    # Update layout
    fig.update_layout(
        xaxis=dict(title='Sentiment'),
        yaxis=dict(title='Antal'),
        legend=dict(title='Ordtyp')
    )

    return fig

###########################################################

# Function to generate rephrased sentences using ChatGPT
def generate_rephrased_sentences(sentence, undvik):
    import openai
    # Set up OpenAI API credentials
    openai.api_key = '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'

    ordlista = ['stark','drivkraft','chef', 'analys', 'analytisk', 'driven', 'individer', 'beslut', 'kompetent','självständig']

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Skriv om följande mening och ersätt ordet {undvik}: '{sentence}'. Skriv inte mer än en mening, och du får absolut inte använda orden {ordlista}",
        max_tokens=100,
        temperature=0.9,
        n=3,  # Generate 3 rephrased sentences
        stop=None
    )
    rephrased_sentences = [choice.text.strip() for choice in response.choices]
    return rephrased_sentences

######################
def create_wordcloud(data):
    '''skapar wordcloud figur baserat på bad_words df'''
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

    # Define a color mapping for each word
    color_map = color_mapping()

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        
        if word in color_map:
            return color_map[word]
        
        # Generate a random color for each word
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        # Return the RGB color as a string
        return f'rgb({r}, {g}, {b})'

    wordcloud.recolor(color_func=color_func)

    # Display the word cloud using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    #ax.set_title('Word Cloud') # titeltext för wordcloud
    fig.set_frameon(False)
    return fig

#############################
######## Line chart #########



#############################

def color_mapping():
    '''väljer färg för orden i wordcloud och line chart'''
    '''color_mapping = {
    'analytisk': '#FF0000',  # Red
    'driven': '#00FF00',  # Green
    'stark': '#0000FF',  # Blue
    'analys': '#FFA500',  # Orange
    'drivkraft': '#FFFF00',  # Yellow
    'kompetent': '#800080',  # Purple
    'chef': '#FFC0CB',  # Pink
    'beslut': '#008080',  # Teal
    'individer': '#FF6347',  # Tomato
    'självständig': '#808080'  # Gray
}'''

    color_mapping = {
        'analytisk': '#91bcdd', 
        'driven': '#b60033',  
        'stark': '#b6b975',  
        'analys': '#b65d54',  
        'drivkraft': '#f8cc1b',  
        'kompetent': '#72b043', 
        'chef': '#a662a8',  
        'beslut': '#f37324',  
        'individer': '#057dcd',  
        'självständig': '#cac7ff'  
    }

    return color_mapping


def rgy_bar_chart(job_ads, occupation_group):
    '''visar andel av förekomst av missgynnande ord som aldrig 0 sällan 1 ofta > 1'''
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

    def sort_occ_labels(kolumn, df_combined):
        '''sorterar y axeln från lägsta till högsta andel grönt, dvs förekomst aldrig'''


        # Sort the DataFrame by the percentage of green bars in descending order
        df_combined = df_combined.sort_values(by='Förekomst', ascending=False)


        # Calculate the percentage of greens relative to reds and yellows within each occupation_group_label
        df_combined['green_percentage'] = df_combined.groupby(kolumn)['Förekomst'].transform(
            lambda x: (x == 'Aldrig').mean())

        # Sort the DataFrame based on the green_percentage in descending order
        df_sorted = df_combined.sort_values(by='green_percentage', ascending=True)

        # Extract the list of values in the occupation_group_label column
        result = df_sorted[kolumn].unique().tolist()

        return result
    
    def generate_tooltip_config(kolumn):
        '''skapar tooltip för respektive filtrering på yrkesgrupp och jobbtitel'''
        tooltips = [
            alt.Tooltip('frac:Q', title='Andel', format=' .0%'),
            alt.Tooltip('count:Q', title='Antal'),
            alt.Tooltip(kolumn, title='Jobbtitel') if kolumn == 'occupation_label' else alt.Tooltip(kolumn, title='Yrkesgrupp') ,
            alt.Tooltip('Förekomst', title='Förekomst')
        ]
        return tooltips
    

    # Define the desired order of colors
    color_order = ['Aldrig', 'Ibland', 'Ofta']  # sets color of bars
    bar_order = ['Ofta', 'Ibland', 'Aldrig'] # sätter ordning på färger i bars. Är av någon anledning reversed.


    # Determine the field to use for the y-axis label and the tooltip based on the occupation grouping
    if 'Alla' in occupation_group:
        y_field = 'occupation_group_label'
        custom_tooltip = generate_tooltip_config(y_field)

    else:
        y_field = 'occupation_label'
        tooltip_fields = ['frac:Q', 'count:Q', 'occupation_label', 'Förekomst']
        custom_tooltip = generate_tooltip_config(y_field)

    # Create the Altair chart
    chart2 = alt.Chart(df_combined).transform_aggregate(
        count='count()',
        groupby=['Förekomst', y_field]
    ).transform_joinaggregate(
        total='sum(count)',
        groupby=[y_field]
    ).transform_calculate(
        order=f"-indexof({bar_order}, datum.Förekomst)",
        frac=alt.datum.count / alt.datum.total
    ).mark_bar().encode(
        y=alt.Y(y_field,
                sort=sort_occ_labels(y_field, df_combined),
                axis=alt.Axis(title='Yrkesgrupp', labelLimit=200)),
        x=alt.X('count:Q', stack='normalize', axis=alt.Axis(format='%', title='Andel')),
        color=alt.Color('Förekomst',
                        scale=alt.Scale(domain=color_order,
                                        range=[green_color, yellow_color, red_color]),
                        sort=bar_order),
        order="order:Q",
        tooltip=custom_tooltip
    ).properties(height=500,
                title='Ordens förekomst').interactive()

    combined_chart = chart2

    return combined_chart