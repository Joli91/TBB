import streamlit as st
import pandas as pd
import json
import matplotlib
from data_methods import bad_word_count, bad_ads_and_words, bar_chart, bar_chart_st
import altair as alt


# Syftestext input
syftestext = 'et pharetra pharetra massa massa ultricies mi quis hendrerit dolor magna eget est lorem ipsum dolor sit amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas integer eget aliquet nibh praesent tristique magna sit amet purus gravida quis blandit turpis cursus in hac habitasse platea dictumst quisque sagittis purus sit amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus mauris a diam maecenas sed enim ut sem viverra aliquet eget sit amet tellus cras adipiscing enim eu turpis egestas pretium aenean pharetra magna ac placerat vestibulum lectus mauris ultrices eros in cursus turpis massa tincidunt dui ut ornare lectus sit amet est placerat in egestas erat imperdiet sed euismod nisi porta lorem mollis aliquam ut porttitor leo a diam sollicitudin tempor id eu nisl nunc mi ipsum faucibus vitae aliquet nec ullamcorper sit amet risus nullam eget felis eget nunc lobortis mattis aliquam faucibus purus in massa tempor nec feugiat nisl pretium fusce id velit ut tortor pretium viverra suspendisse potenti nullam ac tortor vitae purus faucibus ornare suspendisse sed nisi lacus sed viverra tellus in hac habitasse platea dictumst vestibulum rhoncus est pellentesque elit ullamcorper dignissim cras tincidunt lobortis feugiat'

# Load data
df = pd.read_json('Data/Testfil_FINAL.json')

with open('Data/Testfil_FINAL.json', 'r', encoding='utf-8') as f:
    job_ads = json.load(f)

# Koden nedan hämtar bara 3 variabler från JSON-filen (förhoppningsvis snabbare vid större JSON-fil)
#with open('Data/Testfil_FINAL.json', 'r', encoding='utf-8') as f:
#    job_ads = json.load(f, object_hook=lambda d: {k: v for k, v in d.items() if k in ('description.text', 'occupation_group.label', 'Bad_words')})

# Title
st.title('Titeltext',)

# Kolumner 
col1, col2 = st.columns([2,1])
with col1:
    st.header('Syfte')
    # Syftestext
    st.markdown(f'<span style="word-wrap:break-word;">{syftestext}</span>', unsafe_allow_html=True)
    # Create the bar chart using the function
    #fig = bar_chart(job_ads)

   #Visa bar chart via stremlit istället för matplotlib
    green, yellow, red = bar_chart_st(job_ads)
    chart_data = pd.DataFrame({'Antal annonser': [green, yellow, red]}, 
                          index=['Green', 'Yellow', 'Red'])
    colors = ['#32CD32', '#FFC107', '#FF0000']
    bars = alt.Chart(chart_data.reset_index()).mark_bar().encode(x='index', y='Antal annonser', color=alt.Color('index', scale=alt.Scale(domain=['Green', 'Yellow', 'Red'], range=colors))).properties(width=400, height=300)

    st.altair_chart(bars)

    # Display the chart in Streamlit
    #st.pyplot(fig)

with col2:
        # Slider för år
    min_value = df['publication_date'].min()
    max_value = df['publication_date'].max()

    variable_1 = st.slider('Välj år', min_value=int(min_value), max_value=int(max_value), value=2017)
    st.write('Valt år:', variable_1)

    # Selectbox för yrkesroll
    occupation_group_list = df['occupation_group.label'].unique().tolist()
    option = st.selectbox('Välj yrkesroll:', occupation_group_list)
    
    st.header('Total inom IT')
    bad_ads = bad_ads_and_words(job_ads)
    st.table(bad_ads)
    
    st.header('Dåliga ord:')
    bad_words = bad_word_count(option, job_ads)
    st.table(bad_words)


    


    


st.header('AI analys')







