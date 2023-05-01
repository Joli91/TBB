import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('your_data.csv')

# Title
st.title('Data Visualization Template')

# Show data
st.write(data)

# Create bar chart
st.subheader('Bar Chart')
fig, ax = plt.subplots()
ax.bar(data['column1'], data['column2'])
st.pyplot(fig)

# Create line chart
st.subheader('Line Chart')
fig, ax = plt.subplots()
ax.plot(data['column1'], data['column2'])
st.pyplot(fig)

# Create scatter plot
st.subheader('Scatter Plot')
fig, ax = plt.subplots()
ax.scatter(data['column1'], data['column2'])
st.pyplot(fig)
