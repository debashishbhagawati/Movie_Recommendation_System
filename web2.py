import streamlit as st
import tempfile
import pickle
import requests


def main():
    st.set_page_config(layout='wide')
    st.sidebar.title("Dash Board")
    st.sidebar.markdown("_______________________________")

    app_mode = st.sidebar.selectbox('Choose the App Mode', ['About App', 'Get Recommendation', 'About The Developer'])
    st.sidebar.header("  ", divider=True)
    if app_mode == "About App":
        a,b,c = st.columns(3)
        with b:
            st.title("MOVIESPHERE\n\n")
        st.header("", divider=True)


        col8, col9 = st.columns([0.5, 0.5])
        with col8:
            st.image('media/poster.png')
        with col9:
            DEMO_VIDEO = "media/about_video.mp4"
            tffile = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            tffile.name = DEMO_VIDEO
            demo_vid = open(tffile.name, 'rb')
            demo_bytes = demo_vid.read()
            st.video(demo_bytes)
            st.markdown("""
                Welcome to our revolutionary Movie Recommendation System-"MOVIESPHERE", where cinematic exploration meets personalized enjoyment! 
                Our web app is designed to elevate your movie-watching experience by providing tailored recommendations based on 
                your unique tastes and preferences. Say goodbye to endless scrolling through generic lists and hello to a curated 
                selection of films that align with your cinematic interests.
                
                Whether you're a seasoned film buff or just embarking on your cinematic journey, our app caters to all tastes 
                and preferences. We understand that each movie enthusiast is unique, and our goal is to make your movie-watching 
                experience as individual as you are. From timeless classics to hidden gems, our recommendations cover a wide 
                spectrum of genres, ensuring there's something for everyone.
                
                Navigating our user-friendly interface is a breeze. Just type in the name of a movie that holds a special place 
                in your heart, and let the app guide you to a world of cinematic treasures. We believe that every movie has the 
                potential to create a memorable experience, and our Movie Recommendation System is here to help you discover those 
                gems that might have otherwise remained hidden.
                
                So, whether you're seeking heartwarming dramas, pulse-pounding thrillers, laugh-out-loud comedies, or mind-bending 
                mysteries, our web app is your go-to destination for tailored movie recommendations. Embrace the joy of discovering 
                new favorites, relishing in the art of storytelling, and creating lasting memories with our Movie Recommendation 
                System. Get ready to embark on a cinematic journey like never before!
                """)

    if app_mode == "Get Recommendation":
        def fetch_poster(movie_id):
            url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
            data = requests.get(url)
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path

        def recommend(movie):
            index = movies[movies['title'] == movie].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            recommended_movie_names = []
            recommended_movie_posters = []
            for i in distances[1:6]:
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movie_names.append(movies.iloc[i[0]].title)

            return recommended_movie_names,recommended_movie_posters


        st.header('Movie Recommender System', divider=True)
        movies = pickle.load(open('model/movie_list.pkl', 'rb'))
        similarity = pickle.load(open('model/similarity.pkl', 'rb'))

        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown",
            movie_list
        )

        if st.button('Show Recommendation'):
            recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
            col1, col2, col3, col4, col5 = st.columns(5, gap = 'medium')
            with col1:
                st.markdown(recommended_movie_names[0]+"\n")
                st.image(recommended_movie_posters[0])

            with col2:
                st.markdown(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])

            with col3:
                st.markdown(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
            with col4:
                st.markdown(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
            with col5:
                st.markdown(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])

    if app_mode == "About The Developer":
        st.header("About Me", divider=True)
        col1, col2 = st.columns([0.7,0.3])
        with col2:
            st.image('media/mypic.jpeg', width= 250)

        with col1:
            st.markdown('''\n\n
            Greetings! I'm Debashish Bhagawati, a passionate Computer Science and Machine Learning enthusiast currently pursuing my B.Tech at IIT Dhanbad. Hailing from the enchanting landscapes of Assam, I find immense joy in applying the principles of computer science to solve real-life problems through innovative technology.
            
            As the mind behind this app, I've strived to infuse my love for problem-solving and dedication to excellence into every line of code. This application is a testament to my belief in harnessing the capabilities of computer science to simplify, enhance, and enrich our lives.
            
            I invite you to explore the features and functionalities of this app, each carefully designed to reflect my commitment to user satisfaction and technological innovation. Your feedback is invaluable, and I look forward to evolving this project further based on the insights and suggestions from users like you.
            
            Thank you for joining me on this journey of exploration and creation. Let's embrace the exciting possibilities that the world of computer science has to offer.
            
            Warm regards,
            Debashish Bhagawati\n\n
            ''')

        st.header("Get in Touch", divider=True)
        st.markdown("Contact No: 6003928984")
        st.markdown("Email: debashishbhagawati2004@gmail.com")
        st.markdown("Address: Phukan-Nagar, Siavasagar, Assam, 785640")
        st.link_button(url = "https://www.linkedin.com/in/debashish-bhagawati-044b36263/", label="LinkedIn")
        st.link_button(url = "https://github.com/debashishbhagawati", label="GitHub")


if __name__ == '__main__':
    main()
