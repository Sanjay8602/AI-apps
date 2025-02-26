import streamlit as st
import openai
import requests


OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
OMDB_API_KEY = "YOUR_OMDB_API_KEY"

openai.api_key = OPENAI_API_KEY


def get_movie_recommendations(genre, description):
    prompt = f"Suggest 5 movies based on genre '{genre}' and description: {description}. Provide only movie titles, comma-separated."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    movies = response['choices'][0]['message']['content'].split(", ")
    return movies


def get_movie_details(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    
    if response["Response"] == "True":
        return {
            "title": response["Title"],
            "year": response["Year"],
            "rating": response.get("imdbRating", "N/A"),
            "poster": response.get("Poster", "https://via.placeholder.com/300"),
            "plot": response.get("Plot", "No description available."),
            "trailer": f"https://www.youtube.com/results?search_query={movie_title}+trailer"
        }
    return None

st.set_page_config(page_title="🎬 AI Movie Recommender", layout="centered")

st.title("🎥 AI Movie Recommender")
st.write("Get AI-powered movie recommendations with ratings, posters, and trailers!")


genre = st.text_input("Enter Genre (e.g., Action, Comedy, Sci-Fi)")
description = st.text_area("Describe the type of movie you want to watch")

if st.button("Get Recommendations"):
    if genre and description:
        with st.spinner("Fetching recommendations..."):
            recommended_movies = get_movie_recommendations(genre, description)
            st.subheader("🎬 Recommended Movies:")
            
            # Display each movie with details
            for movie in recommended_movies:
                details = get_movie_details(movie)
                if details:
                    st.markdown(f"### {details['title']} ({details['year']})")
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(details["poster"], width=150)
                    with col2:
                        st.write(f"⭐ IMDb Rating: {details['rating']}")
                        st.write(f"📜 {details['plot']}")
                        st.markdown(f"[🎬 Watch Trailer]({details['trailer']})")
                    st.divider()
    else:
        st.warning("Please enter both genre and description.")


st.markdown("---")
st.write("Made with ❤️ using Streamlit, OpenAI & OMDb API")
