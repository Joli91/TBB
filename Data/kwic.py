import matplotlib.pyplot as plt
from wordcloud import WordCloud

def extract_context(text, keyword, window_size=5):
    """
    Extract the context of the keyword from the text.
    The context is defined as the words within a certain window size (default is 5)
    of the keyword.
    """
    words = text.split()
    for i, word in enumerate(words):
        if word == keyword:
            start = max(0, i - window_size)
            end = min(len(words), i + window_size + 1)
            context_words = words[start:end]
            context = ' '.join(context_words)
            return context
    return None

def generate_wordcloud(text):
    """
    Generate a WordCloud object from the input text.
    """
    wordcloud = WordCloud(width=500, height=500, background_color='white', colormap='Dark2', stopwords=None, max_words=50).generate(text)
    return wordcloud


def visualize_wordcloud_with_context(text, keyword, window_size=5):
    """
    Generate a word cloud with the context of the keyword highlighted.
    """
    context = extract_context(text, keyword, window_size)
    wordcloud = generate_wordcloud(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    if context is not None:
        bbox = {'facecolor': 'white', 'edgecolor': 'none', 'alpha': 0.8, 'boxstyle': 'round,pad=0.3'}
        ax.text(0.5, 0.5, context, ha='center', va='center', transform=ax.transAxes, bbox=bbox)
    ax.axis('off')
    return fig



text = "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human languages. In particular, it focuses on programming computers to process and analyze large amounts of natural language data. NLP is used in a wide range of applications, such as chatbots, language translation, sentiment analysis, and text summarization."
keyword = 'data'

fig = visualize_wordcloud_with_context(text, keyword)

plt.show()
