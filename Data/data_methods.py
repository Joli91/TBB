import re
import json
import pandas as pd

def bad_word_count(roll):
    '''Summerar antal dåliga ord i datasetet och skapar en sorterad df med antal förekomster av 
    respektive ord'''
# Load the JSON file
    with open('Data/Testfil_FINAL.json', 'r', encoding='utf-8') as f:
        job_ads = json.load(f)
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
    for ad in job_ads:
        if ad['description.text'] is not None and ad['occupation_group.label'] == roll:
            ad_text = ad['description.text'].lower().replace('.', ' ')
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
    df.set_index('Ord', inplace=True)
    return df

def bad_ads_and_words(job_ads):
    '''Räknar antal annonser som innehåller dåliga ord, summerar antalet dåliga ord
    och räknar ut ett genomsnitt på antal dåliga ord per dålig annons samt procentsats'''
    bad_ads = 0
    total_bad_words = 0

    for ad in job_ads:
        if ad['Bad_words'] != 0:
            bad_ads += 1
            total_bad_words += ad['Bad_words']
        else:
            continue

    # Count the average amount of bad words for each job ad
    average_bad_words = total_bad_words / bad_ads
    # Count the percentage of bad ads from total ads
    percentage_bad_ads = bad_ads / len(job_ads) * 100

    #print('Amount of bad ads:', percentage_bad_ads, '%')
    #print('Total amount of bad words in bad ads:', total_bad_words)
    #print('Total amount of bad ads:', bad_ads)
    #print("Average bad words per bad ad:", average_bad_words)

    df2 = pd.DataFrame()
    df2 = df2.reset_index()
    df2.columns = ['Ord', 'Antal']
    df2.set_index('Ord', inplace=True)
    return df2

    #return average_bad_words, percentage_bad_ads