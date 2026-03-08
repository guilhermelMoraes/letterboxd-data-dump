import os
import requests

tmdb_token = os.getenv("TMDB_BEARER_TOKEN")


def request_tmdb_data(movie_name, movie_release_year):
    try:
        tmdb_request = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"query": movie_name, "primary_release_year": movie_release_year},
            headers={"Authorization": f"Bearer {tmdb_token}"},
        )

        return tmdb_request.json()["results"][0]
    except (requests.exceptions.RequestException, KeyError, IndexError) as error:
        print(f"Error fetching TMDB data for movie {movie_name}")
        print(error)
        return None
