import streamlit as st
import numpy as np
import joblib

# Set page config at the very beginning
st.set_page_config(page_title="Book Recommender System", layout="wide")

# Load the data
try:
    popular_df = joblib.load(open('popular.pkl', 'rb'))
    pt = joblib.load(open('pt.pkl', 'rb'))
    books = joblib.load(open('books.pkl', 'rb'))
    similarity_scores = joblib.load(open('similarity_scores.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {e}")
    popular_df = pt = books = similarity_scores = None

# Function to recommend books
def recommend_books(user_input):
    if pt is None or books is None or similarity_scores is None:
        st.error("Error loading data. Please try again later.")
        return []

    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
        return data

    except IndexError:
        st.warning("Book not found. Please try again with a different title.")
        return []
    except Exception as e:
        st.error(f"Error during recommendation: {e}")
        return []

# Custom CSS for card layout
st.markdown(
    """
    <style>
    .card-img-top {
    width: 100%;
    height: 50px;  /* Adjust height here */
    object-fit: contain;
  }
    .card-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
    .card {
        border: 1px solid #ddd;
        border-radius: 7px;
        padding: 10px;
        text-align: center;
        width: 100%;
    }
    .card-body {
        padding: 10px;
    }
    .card-title {
        font-size: 10px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .card-text {
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Content
st.title("What should I read next?")
st.write(
    """
    When we're looking for good books to read, we browse bestseller lists, click around Goodreads and Instagram, and ask friends for their recommendations. 
    But the usual blanket categories and genres can be a bit too broad, and often, we've found that we get the best recommendations when we choose books based on our mood or our interests. 
    If you're looking for interesting books to read, we've specific recommendations you won't be able to put down. 
    This list has you covered, no matter how you're feeling.
    """
)

# Search bar with dropdown
book_titles = pt.index.tolist() if pt is not None else []
user_input = st.selectbox("Enter a book title", options=book_titles)

if st.button("Recommend"):
    recommendations = recommend_books(user_input)
    if recommendations:
        st.subheader("Recommendations")
        cols = st.columns(4)
        for idx, rec in enumerate(recommendations):
            with cols[idx % 4]:
                st.image(rec[2], use_column_width=True)
                st.markdown(f"**{rec[0]}**")
                st.write(f"Author: {rec[1]}")
    else:
        st.write("No recommendations found.")

# Display top 50 books in cards, 4 cards per row
st.subheader("Top 50 Books")
if popular_df is not None:
    for i in range(0, len(popular_df), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(popular_df):
                book = popular_df.iloc[i + j]
                with cols[j]:
                    st.image(book['Image-URL-M'], use_column_width=True)
                    st.markdown(f"**{book['Book-Title']}**")
                    st.write(f"Author: {book['Book-Author']}")
                    st.write(f"Votes: {book['num_ratings']}")
                    st.write(f"Rating: {book['avg_rating']}")
else:
    st.write("Error loading popular books.")