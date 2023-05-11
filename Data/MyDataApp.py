import streamlit as st
import pandas as pd
import json
from data_methods import bad_word_count, bad_ads_and_words



# Syftestext input
syftestext = 'et pharetra pharetra massa massa ultricies mi quis hendrerit dolor magna eget est lorem ipsum dolor sit amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas integer eget aliquet nibh praesent tristique magna sit amet purus gravida quis blandit turpis cursus in hac habitasse platea dictumst quisque sagittis purus sit amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus mauris a diam maecenas sed enim ut sem viverra aliquet eget sit amet tellus cras adipiscing enim eu turpis egestas pretium aenean pharetra magna ac placerat vestibulum lectus mauris ultrices eros in cursus turpis massa tincidunt dui ut ornare lectus sit amet est placerat in egestas erat imperdiet sed euismod nisi porta lorem mollis aliquam ut porttitor leo a diam sollicitudin tempor id eu nisl nunc mi ipsum faucibus vitae aliquet nec ullamcorper sit amet risus nullam eget felis eget nunc lobortis mattis aliquam faucibus purus in massa tempor nec feugiat nisl pretium fusce id velit ut tortor pretium viverra suspendisse potenti nullam ac tortor vitae purus faucibus ornare suspendisse sed nisi lacus sed viverra tellus in hac habitasse platea dictumst vestibulum rhoncus est pellentesque elit ullamcorper dignissim cras tincidunt lobortis feugiat'

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
st.title('Titeltext',)

# Kolumner 
col1, col2 = st.columns([1,1])
with col1:
    st.header('Syfte')
    # Syftestext
    st.markdown(f'<span style="word-wrap:break-word;">{syftestext}</span>', unsafe_allow_html=True)

with col2:

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
    
    # Sektion för Total inom IT
    st.header('Total inom IT')
    bad_ads = bad_ads_and_words(job_ads)
    st.table(bad_ads)
    ##############################
    
    # Sektion för dåliga ord
    st.header('Dåliga ord:')
    bad_words = bad_word_count(job_ads)
    st.table(bad_words)
    ##############################

    


    


st.header('AI analys')







