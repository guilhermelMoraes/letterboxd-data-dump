import csv
import time
from datetime import datetime
from fetch_tmdb_data import request_tmdb_data


def import_letterboxd_diary():
    with open("../diary.csv", newline="") as watched_movies:
        csv_reader = csv.reader(watched_movies, delimiter=";", quotechar='"')

        counter = 0

        movies = []
        repeated_movies = {}

        next(csv_reader)

        for row in csv_reader:
            movie = {}

            try:
                date_obj = datetime.strptime(row[0], "%Y-%m-%d")

                movie["watch_date"] = date_obj.strftime("%d/%m/%Y")
                movie["name"] = row[1]
                movie["release_year"] = row[2]

                repeated_movies[row[1]] = repeated_movies.get(row[1], 0) + 1

                if row[5] != "":
                    movie["rewatched"] = repeated_movies[row[1]]

                if row[4] != "":
                    movie["rating"] = float(row[4])

                if row[6] != "":
                    movie["tags"] = row[6]

                tmdb_data = request_tmdb_data(movie["name"], movie["release_year"])

                if tmdb_data["poster_path"]:
                    movie["poster"] = (
                        f"http://image.tmdb.org/t/p/w300{tmdb_data['poster_path']}"
                    )

                if tmdb_data["id"]:
                    movie["url"] = (
                        f"https://www.themoviedb.org/movie/{tmdb_data['id']}-{tmdb_data['title'].lower()}"
                    )

                movie_already_in_list = next(
                    (m for m in movies if m["name"] == movie["name"]), None
                )

                if movie_already_in_list:
                    movie_already_in_list["rewatched"] = (
                        movie_already_in_list.get("rewatched", 0) + 1
                    )
                else:
                    movies.append(movie)

                counter += 1
                print(f"Rows succesfully processed {counter} | {row[1]}")
            except Exception as error:
                print(f"Error processing movie {row[1]}")
                print(error)
            finally:
                time.sleep(0.3)

    print(movies)


import_letterboxd_diary()
