import os
import csv
import time
import requests
from datetime import datetime

tmdb_token = os.getenv('TMDB_BEARER_TOKEN')

def get_repeated_movies(item):
    _, value = item
    return value > 1

def import_letterboxd_csv():
    with open('./diary.csv', newline='') as watched_movies:
        csv_reader = csv.reader(watched_movies, delimiter=';', quotechar='"')

        counter = 0

        movies = []
        repeated_movies = {}

        next(csv_reader)

        for row in csv_reader:
            movie = {}
            
            try:
                date_obj = datetime.strptime(row[0], "%Y-%m-%d")

                movie['watch_date'] = date_obj.strftime("%d/%m/%Y")
                movie['name'] = row[1]
                movie['release_date'] = row[2]
                movie['url'] = row[3]

                repeated_movies[row[1]] = repeated_movies.get(row[1], 0) + 1

                if (row[5] != ''):
                    movie['rewatch'] = row[5]

                if (row[4] != ''):
                    movie['rating'] = float(row[4])

                if (row[6] != ''):
                    movie['tags'] = row[6]

                
                # tmdb_request = requests.get('https://api.themoviedb.org/3/search/movie', params = { 'query': row[1], 'primary_release_year': row[2] }, headers={
                #     'Authorization': 'Bearer ' + token
                # })

                counter += 1
                print('Rows succesfully processed ' + counter)

                movies.append(movie)
            except Exception as error:
                print('Error processing movie ' + row[1])
                print(error)
            finally:
                time.sleep(0.3)

    repeated_movies = dict(filter(get_repeated_movies, repeated_movies.items()))

    print(repeated_movies)

import_letterboxd_csv()


# tmdb_request = requests.get(
#     'https://api.themoviedb.org/3/search/movie',
#     params = { 'query': 'Interstellar', 'primary_release_year': '2014' },
#     headers={
#         'Authorization': 'Bearer ' + token
#     }
# )

# teste = tmdb_request.json();

# print(teste['results'][0])