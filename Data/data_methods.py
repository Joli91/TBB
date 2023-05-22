import re
import pandas as pd
import altair as alt
import plotly.express as px
import squarify
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sb
from wordcloud import WordCloud

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

def bad_word_count_adv(job_ads):
    '''en mer avancerad bad word count som behåller job_ads as is och lägger till 
    kolumner för varje ord med count på respektive rad'''
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

    return job_ads

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

def bar_chart_st(job_ads):
    red_ads = 0
    yellow_ads = 0
    green_ads = 0

    for index, ad in job_ads.iterrows():
        if ad['Bad_words'] == 0:
            green_ads += 1
        elif ad['Bad_words'] == 1:
            yellow_ads += 1
        elif ad['Bad_words'] > 1:
            red_ads += 1
        else:
            continue

    return green_ads, yellow_ads, red_ads

###########################################################

def bubble_chart(job_ads):
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
    color_map = {'missgynnande ord': 'red', 'gynnande ord': 'green'}
   # Merge keyword_df with the count dataframe on the 'Keyword' column
    merged_df = keyword_df.merge(df_counts, on='Keyword')

    # Calculate the average count
    avg_count = merged_df['Count'].mean()

    # Calculate the scaled size column
    scaling_factor = 25  # Adjust the scaling factor to control the difference in sizes
    merged_df['ScaledSize'] = merged_df['Count'].apply(lambda x: scaling_factor * x if x > avg_count else scaling_factor * avg_count)

    # Create bubble chart using Plotly
    fig = px.scatter(merged_df, x='Sentiment', y='Count', size='ScaledSize', color='Color', color_discrete_map=color_map, hover_data=['Keyword'])

    # Update layout
    fig.update_layout(
        xaxis=dict(title='Sentiment'),
        yaxis=dict(title='Antal'),
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
    # Display the word cloud using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    #ax.set_title('Word Cloud') # titeltext för wordcloud
    fig.set_frameon(False)
    return fig

#############################

def bad_word_line_chart(job_ads):
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