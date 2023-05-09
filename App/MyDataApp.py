import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

syftestext = 'et pharetra pharetra massa massa ultricies mi quis hendrerit dolor magna eget est lorem ipsum dolor sit amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas integer eget aliquet nibh praesent tristique magna sit amet purus gravida quis blandit turpis cursus in hac habitasse platea dictumst quisque sagittis purus sit amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus mauris a diam maecenas sed enim ut sem viverra aliquet eget sit amet tellus cras adipiscing enim eu turpis egestas pretium aenean pharetra magna ac placerat vestibulum lectus mauris ultrices eros in cursus turpis massa tincidunt dui ut ornare lectus sit amet est placerat in egestas erat imperdiet sed euismod nisi porta lorem mollis aliquam ut porttitor leo a diam sollicitudin tempor id eu nisl nunc mi ipsum faucibus vitae aliquet nec ullamcorper sit amet risus nullam eget felis eget nunc lobortis mattis aliquam faucibus purus in massa tempor nec feugiat nisl pretium fusce id velit ut tortor pretium viverra suspendisse potenti nullam ac tortor vitae purus faucibus ornare suspendisse sed nisi lacus sed viverra tellus in hac habitasse platea dictumst vestibulum rhoncus est pellentesque elit ullamcorper dignissim cras tincidunt lobortis feugiat'

# Load data
data = pd.read_json('Data/Testfil_samtliga.json')

# Title
st.title('Titeltext',)

# Show data
#st.write(data)

# Kolumner 
col1, col2 = st.columns([2,1])
with col1:
    #st.set_option('max-width', 0)
    st.header('Syfte')
    # Syftestext
    st.markdown(f'<span style="word-wrap:break-word;">{syftestext}</span>', unsafe_allow_html=True)

with col2:
    st.header('Total inom IT')
    st.header('Dåliga ord:')




# Create scatter plot
