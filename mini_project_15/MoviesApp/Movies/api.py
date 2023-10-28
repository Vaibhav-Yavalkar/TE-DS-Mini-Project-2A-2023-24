import requests

# Replace 'YOUR_API_KEY' with your actual OMDb API key.
api_key = 'eb39e71b'

def get_movie_poster(imdb_id):
    #url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
    url= f"http://www.omdbapi.com/?t={imdb_id}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'Poster' in data:
            return data['Poster']
        return 

imdb_id = 'Avatar'  # Replace with the IMDb ID of the movie you want to get the poster for.
poster_url = get_movie_poster(imdb_id)

if poster_url:
    print(f"Poster URL: {poster_url}")
else:
    print("Poster not found.")

