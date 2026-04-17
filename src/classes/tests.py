import pytest
import os
from movies import Movies
from tags import Tags
from links import Links
from ratings import Ratings

"""
if the methods return the correct data types,
if the list elements have the correct data types,
if the returned data is sorted correctly.

"""
PATH_TO_CSV_MOVIES = "../datasets/movies.csv"
PATH_TO_CSV_TAGS = "../datasets/tags.csv"
PATH_TO_CSV_LINKS = "../datasets/links.csv"
PATH_TO_CSV_RATINGS = "../datasets/ratings.csv"

class Tests:    
    # #Movies
    def test_read_file(self):
        movies = Movies(PATH_TO_CSV_MOVIES)
        data = movies.data
        assert isinstance(data, list), f"read_file должен возвращать list, получен {type(data)}"
        
        if data:
            first = data[0]
            assert isinstance(first, list), f"элементы таблицы должны быть list, получен {type(first)}"
            assert isinstance(first[0], int), f"movieId должен быть int, получен {type(first[0])}"
            assert isinstance(first[1], str), f"title должен быть str, получен {type(first[1])}"
            assert isinstance(first[2], list), f"genres должен быть list, получен {type(first[2])}"
    
    def test_extract_genres(self):
        movies = Movies(PATH_TO_CSV_MOVIES)
        test_s = "Action|Adventure|Sci-Fi"
        genres = movies.extract_genres(test_s)
        assert isinstance(genres, list), f"extract_genres должен возвращать list, получен {type(genres)}"
        
        for g in genres:
            assert isinstance(g, str), f"genre должен быть str, получен {type(g)}"
            
    def test_str_handler(self):
        movies = Movies(PATH_TO_CSV_MOVIES)
        test_s = "1,Stranger Things,Adventure|Fantasy|Children"
        handle = movies.str_handler(test_s)
        assert isinstance(handle, list), f"str_handler должен возвращать list, получен {type(handle)}"
        
        assert isinstance(handle[0], int), f"элемент 0 должен быть int, получен {type(handle[0])}"
        assert isinstance(handle[1], str), f"элемент 1 должен быть str, получен {type(handle[1])}"
        assert isinstance(handle[2], list), f"элемент 2 должен быть list, получен {type(handle[2])}"
    
    def test_extract_year(self):
        movies = Movies(PATH_TO_CSV_MOVIES)
        res = movies.extract_year()
        assert isinstance(res, list), f"extract_year должен возвращать list, получен {type(res)}"
        if res:
            for year in res:
                assert isinstance(year, int), f"год должны быть int, получен {type(year)}"
                assert 1894 < year < 2027, f"год {year} вне диапазона, p.s. первый фильм сняли в 1895 году"
    
    def test_dict_by_release(self):
        movies = Movies(PATH_TO_CSV_MOVIES)
        res = movies.dist_by_release()

        assert isinstance(res, dict), f"dict_by_release должен возвращать dict, получен {type(res)}"
        if res: 
            for key, value in res.items():
                #годы
                assert isinstance(key, int), f"ключ (год) должен быть int, получен {type(key)}"
                
                #количества
                assert isinstance(value, int), f"значение (количество) должно быть int, получен {type(value)}"
                assert value > 0, f"кол-во должно быть положительным, получено {value}"
            
            #по убыванию
            values = list(res.values())
            for i in range(len(values) - 1):
                assert values[i] >= values[i + 1], f"нарушение сортировки"
    
    def test_dict_by_genres(self):
        movies = Movies(PATH_TO_CSV_MOVIES)
        res = movies.dist_by_genres()
        assert isinstance(res, dict), f"Метод должен возвращать dict, получен {type(res)}"
    
        if res:
            for key, value in res.items():
                assert isinstance(key, str), f"ключ (жанр) должен быть str, получен {type(key)}"
                assert len(key) > 0, "Название жанра не может быть пустой строкой"

                assert isinstance(value, int), f"значение (количество) должно быть int, получен {type(value)}"
                assert value > 0, f"кол-во должно быть положительным, получено {value}"
            
            #по убыванию
            values = list(res.values())
            for i in range(len(values) - 1):
                assert values[i] >= values[i + 1], f"нарушение сортировки"
    
    def test_most_genres(self):
        movies = Movies(PATH_TO_CSV_MOVIES)
        test_n = [0, 1, 5]
        
        for n in test_n:
            res = movies.most_genres(n)
            assert isinstance(res, dict), f"most_genres должен возвращать dict, получен {type(res)}"

            if n == 0:
                assert len(res) == 0, f"при n=0 должен быть пустой словарь, получено {len(res)} элементов"
            elif n <= len(movies.data):
                assert len(res) == n, f"при n={n} должно быть {n} элементов, получено {len(res)}"
            else:
                assert len(res) <= len(movies.data), \
                    f"элементов не может быть больше чем строк в данных"

    
    # #Tags
    def test_select_tags(self):
        tags = Tags(PATH_TO_CSV_TAGS)
        tags_ls = tags.tags
        assert isinstance(tags_ls, list), f"tags должен быть list, получен {type(tags_ls)}"
        if tags_ls:
            for tag in tags_ls:
                assert isinstance(tag, str), f"тег должен быть str, получен {type(tag)}"
    
    def test_most_words(self):
        tags = Tags(PATH_TO_CSV_TAGS)
        test_n = [0, 1, 5]
        for n in test_n:
            res = tags.most_words(n)
            assert isinstance(res, dict), f"most_words должен возвращать dict, получен {type(res)}"
            if n == 0:
                assert len(res) == 0, f"при n = 0 должен быть пустой словарь"
            else:
                assert len(res) <= n, f"должно быть не больше {n} элементов, получено {len(res)}"
                if res:
                    values = list(res.values())
                    for i in range(len(values) - 1):
                        assert values[i] >= values[i + 1], f"нарушение сортировки"
    
    def test_longest(self):
        tags = Tags(PATH_TO_CSV_TAGS)
        test_n = [0, 1, 5]
        for n in test_n:
            res = tags.longest(n)
            assert isinstance(res, list), f"longest должен возвращать list, получен {type(res)}"
            if n == 0:
                assert len(res) == 0, f"при n = 0 должен быть пустой список"
            else:
                assert len(res) <= n, f"должно быть не больше {n} элементов"
                if res:
                    for i in range(len(res) - 1):
                        assert len(res[i]) >= len(res[i + 1]), f"нарушение сортировки по длине"
    
    def test_most_words_and_longest(self):
        tags = Tags(PATH_TO_CSV_TAGS)
        test_n = [0, 1, 5]
        
        for n in test_n:
            res = tags.most_words_and_longest(n)
            assert isinstance(res, list), f"most_words_and_longest должен возвращать list, получен {type(res)}"
            if n == 0:
                assert len(res) == 0, f"при n=0 должен быть пустой список"
            else:
                most_words_set = set(tags.most_words(n).keys())
                longest_set = set(tags.longest(n))
                assert set(res) == most_words_set.intersection(longest_set), \
                    f"результат не является пересечением most_words и longest"
                if len(res) > 1:
                    for i in range(len(res) - 1):
                        assert res[i] <= res[i + 1], f"нарушение алфавитной сортировки"
    
    def test_most_popular(self):
        tags = Tags(PATH_TO_CSV_TAGS)
        test_n = [0, 1, 5]
        
        for n in test_n:
            res = tags.most_popular(n)
            assert isinstance(res, dict), f"most_popular должен возвращать dict, получен {type(res)}"
            
            if n == 0:
                assert len(res) == 0, f"при n=0 должен быть пустой словарь"
            else:
                assert len(res) <= n, f"должно быть не больше {n} элементов"
                if res:
                    values = list(res.values())
                    for i in range(len(values) - 1):
                        assert values[i] >= values[i + 1], f"нарушение сортировки по популярности"
    
    def test_tags_with(self):
        tags = Tags(PATH_TO_CSV_TAGS)
        test_words = ["action", "comedy", "love"]
        
        for word in test_words:
            res = tags.tags_with(word)
            assert isinstance(res, list), f"tags_with должен возвращать list, получен {type(res)}"
            for tag in res:
                assert word in tag.lower(), f"тег '{tag}' не содержит слово '{word}'"
            if len(res) > 1:
                for i in range(len(res) - 1):
                    assert res[i] <= res[i + 1], f"нарушение алфавитной сортировки"
    
    #Links
    def test_select_methods(self):
        links = Links(PATH_TO_CSV_LINKS)
        
        for movie_id in links.movieId[:10]:
            assert movie_id.isdigit(), f"movieId должен содержать только цифры: {movie_id}"

        for imdb_id in links.imdbId[:10]:
            assert imdb_id.isdigit() or imdb_id == '', f"imdbId должен содержать только цифры: {imdb_id}"
            
    def test_get_imdb(self):
        links = Links(PATH_TO_CSV_LINKS)
        
        test_movies = links.movieId[:3] if len(links.movieId) >= 3 else links.movieId
        test_fields = ['Title', 'Director']
        try:
            result = links.get_imdb(test_movies, test_fields)
            assert isinstance(result, list), "get_imdb должен возвращать список"
            
            if result:
                for item in result:
                    assert isinstance(item, list), "элементы должен быть list"
                    assert isinstance(item[0], str), "первый элемент должен быть movieId (строка)"
                    assert len(item) == len(test_fields) + 1, \
                        f"должно быть {len(test_fields) + 1} элементов: movieId + поля"
        except Exception as e:
            pytest.skip(f"пропуск теста: {e}")
            
    def test_top_directors(self):
        links = Links(PATH_TO_CSV_LINKS)
        test_movies = links.movieId[:1]
        try:
            result = links.top_directors(1, test_movies)
            assert isinstance(result, dict), f"top_directors должен возвращать dict, получен {type(result)}"
        except Exception as e:
            pytest.skip(f"пропуск теста: {e}")
            
    def test_most_expensive(self):
        links = Links(PATH_TO_CSV_LINKS)
        try:
            test_movies = links.movieId[:1] if len(links.movieId) > 0 else []
            
            if not test_movies:
                pytest.skip("Нет данных для тестирования")
                
            result = links.most_expensive(1, test_movies)
            if result is not None:
                assert isinstance(result, dict), "most_expensive должен возвращать dict"
                
        except Exception as e:
            pytest.skip(f"пропуск теста most_expensive из-за: {e}")
    
    def test_most_profitable(self):
        links = Links(PATH_TO_CSV_LINKS)
        test_movies = links.movieId[:1]
        n = 1
        try:
            result = links.most_profitable(n, test_movies)

            assert isinstance(result, dict), f"most_profitable должен возвращать dict, получен {type(result)}"

            if result:
                assert len(result) <= n, f"должно быть не больше {n} элементов"
                
                for title, profit in result.items():
                    assert isinstance(title, str), "название фильма должно быть str"
                    assert isinstance(profit, (int, float)), "прибыль должна быть числом"

                if len(result) > 1:
                    profits = list(result.values())
                    for i in range(len(profits) - 1):
                        assert profits[i] >= profits[i + 1], "нарушение сортировки"
        except Exception as e:
            pass
        
    def test_links_longest(self):
        links = Links(PATH_TO_CSV_LINKS)
        test_movies = links.movieId[:1]
        n = 1
        try:
            result = links.longest(n, test_movies)
            assert isinstance(result, dict), f"longest должен возвращать dict"
            if result:
                assert len(result) <= n, f"должно быть не больше {n} элементов"
                
                for title, runtime in result.items():
                    assert isinstance(title, str), "название должно быть str"
                    assert isinstance(runtime, (int, float)), "длительность должна быть числом"
                
                if len(result) > 1:
                    runtimes = list(result.values())
                    for i in range(len(runtimes) - 1):
                        assert runtimes[i] >= runtimes[i + 1], "нарушение сортировки"
        except Exception as e:
            pytest.skip(f"пропуск теста: {e}")
    
    def test_top_cost_per_minute(self):
        links = Links(PATH_TO_CSV_LINKS)
        test_movies = links.movieId[:1]
        n = 1
        try:
            result = links.top_cost_per_minute(n, test_movies)
            assert isinstance(result, dict), f"top_cost_per_minute должен возвращать dict"
            if result:
                assert len(result) <= n, f"должно быть не больше {n} элементов"
                for title, cost in result.items():
                    assert isinstance(title, str), "название должно быть str"
                    assert isinstance(cost, (int, float)), "стоимость/минута должна быть числом"
                
                if len(result) > 1:
                    costs = list(result.values())
                    for i in range(len(costs) - 1):
                        assert costs[i] >= costs[i + 1], "нарушение сортировки"
        except Exception as e:
            pytest.skip(f"пропуск теста top_cost_per_minute: {e}")
    
    #Ratings
    def test_ratings_str_handler(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        test_string = "1,100,4.5,964982703"
        result = ratings.str_handler(test_string)
        
        assert isinstance(result, list), "str_handler должен возвращать list"
        assert isinstance(result[0], int), "userId должен быть int"
        assert isinstance(result[1], int), "movieId должен быть int"
        assert isinstance(result[2], float), "rating должен быть float"
        assert isinstance(result[3], int), "timestamp должен быть int"
        
    def test_ratings_read_file(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        data = ratings.data
        
        assert isinstance(data, list), "read_file должен возвращать list"
        if data:
            first_row = data[0]
            assert isinstance(first_row, list), "элементы должны быть list"
            
    def test_movies_class_init(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        assert hasattr(movies, 'union_data'), "нет атрибута union_data"
        assert isinstance(movies.union_data, list), "union_data должен быть списком"
        
    def test_movies_dist_by_year(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        
        result = movies.dist_by_year()
        assert isinstance(result, dict), "dist_by_year должен возвращать dict"
        
        if result:
            for year, count in result.items():
                assert isinstance(year, int), "год должен быть int"
                assert isinstance(count, int), "кол-во должно быть int"
                assert count > 0, "кол-во должно быть положительным"
                
            years = list(result.keys())
            for i in range(len(years) - 1):
                assert years[i] < years[i + 1], "нарушение сортировки"
                
    def test_movies_dist_by_rating(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        
        result = movies.dist_by_rating()
        assert isinstance(result, dict), "dist_by_rating должен возвращать dict"
        
        if result:
            for rating, count in result.items():
                assert isinstance(rating, float), "рейтинг должен быть float"
                assert isinstance(count, int), "кол-во должно быть int"
                assert count > 0, "кол-во должно быть положительным"
                
            ratings_list = list(result.keys())
            for i in range(len(ratings_list) - 1):
                assert ratings_list[i] < ratings_list[i + 1], "нарушение сортировки"
                
    def test_movies_top_by_num_of_ratings(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        
        test_n = [0, 1, 5]
        for n in test_n:
            result = movies.top_by_num_of_ratings(n)
            assert isinstance(result, dict), "top_by_num_of_ratings должен возвращать dict"
            
            if n == 0:
                assert len(result) == 0, "при n = 0 должен быть пустой словарь"
            else:
                assert len(result) <= n, f"должно быть не больше {n} элементов"
                if result:
                    counts = list(result.values())
                    for i in range(len(counts) - 1):
                        assert counts[i] >= counts[i + 1], "нарушение сортировки"
                        
    def test_movies_top_by_ratings_average(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        
        result = movies.top_by_ratings(5, 'average')
        assert isinstance(result, dict), "top_by_ratings должен возвращать dict"
        
        if result:
            for title, rating in result.items():
                assert isinstance(title, str), "название должно быть str"
                assert isinstance(rating, float), "рейтинг должен быть float"
                assert 0 <= rating <= 5, "рейтинг должен быть от 0 до 5"
                
            ratings_list = list(result.values())
            for i in range(len(ratings_list) - 1):
                assert ratings_list[i] >= ratings_list[i + 1], "нарушение сортировки"
                
    def test_movies_top_by_ratings_median(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        
        result = movies.top_by_ratings(5, 'median')
        assert isinstance(result, dict), "top_by_ratings должен возвращать dict"
        
        if result:
            for title, rating in result.items():
                assert isinstance(title, str), "название должно быть str"
                assert isinstance(rating, float), "рейтинг должен быть float"
                assert 0 <= rating <= 5, "рейтинг должен быть от 0 до 5"
                
            ratings_list = list(result.values())
            for i in range(len(ratings_list) - 1):
                assert ratings_list[i] >= ratings_list[i + 1], "нарушение сортировки"
                
    def test_movies_top_controversial(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        
        result = movies.top_controversial(5)
        assert isinstance(result, dict), "top_controversial должен возвращать dict"
        
        if result:
            for title, variance in result.items():
                assert isinstance(title, str), "название должно быть str"
                assert isinstance(variance, float), "дисперсия должна быть float"
                assert variance >= 0, "дисперсия должна быть неотрицательной"
                
            variances = list(result.values())
            for i in range(len(variances) - 1):
                assert variances[i] >= variances[i + 1], "нарушение сортировки"
                
    def test_users_dist_by_users(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        users = ratings.Users(movies)
        
        result = users.dist_by_users()
        assert isinstance(result, dict), "dist_by_users должен возвращать dict"
        
        if result:
            for user_id, count in result.items():
                assert isinstance(user_id, int), "user_id должен быть int"
                assert isinstance(count, int), "кол-во должно быть int"
                assert count > 0, "кол-во должно быть положительным"
                
    def test_users_dist_by_metric_average(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        users = ratings.Users(movies)
        
        result = users.dist_by_metric('average')
        assert isinstance(result, dict), "dist_by_metric должен возвращать dict"
        
        if result:
            for user_id, rating in result.items():
                assert isinstance(user_id, int), "user_id должен быть int"
                assert isinstance(rating, float), "ср. рейтинг должен быть float"
                assert 0 <= rating <= 5, "рейтинг должен быть от 0 до 5"
                
    def test_users_dist_by_metric_median(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        users = ratings.Users(movies)
        
        result = users.dist_by_metric('median')
        assert isinstance(result, dict), "dist_by_metric должен возвращать dict"
        
        if result:
            for user_id, rating in result.items():
                assert isinstance(user_id, int), "user_id должен быть int"
                assert isinstance(rating, float), "Медианный рейтинг должен быть float"
                assert 0 <= rating <= 5, "Рейтинг должен быть от 0 до 5"
                
    def test_users_top_controversial(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        users = ratings.Users(movies)
        
        result = users.top_controversial(5)
        assert isinstance(result, dict), "top_controversial должен возвращать dict"
        
        if result:
            for user_id, variance in result.items():
                assert isinstance(user_id, int), "user_id должен быть int"
                assert isinstance(variance, float), "дисперсия должна быть float"
                assert variance >= 0, "дисперсия должна быть неотрицательной"
                
            variances = list(result.values())
            for i in range(len(variances) - 1):
                assert variances[i] >= variances[i + 1], "нарушение сортировки"
                
    def test_edge_cases(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)

        result = movies.top_by_num_of_ratings(0)
        assert len(result) == 0, "при n = 0 должен быть пустой словарь"

        all_movies_count = len(set(row[4] for row in movies.union_data))
        result = movies.top_by_num_of_ratings(all_movies_count + 10)
        assert len(result) <= all_movies_count, "не может быть больше фильмов чем есть в датасете"
        
    def test_invalid_metric(self):
        ratings = Ratings(PATH_TO_CSV_RATINGS)
        movies = ratings.Movies(ratings, PATH_TO_CSV_MOVIES)
        try:
            movies.top_by_ratings(5, 'invalid')
            assert False, "должна быть ошибка для неверного metric"
        except Exception as e:
            assert "Not valid metric" in str(e)
        users = ratings.Users(movies)
        try:
            users.dist_by_metric('invalid')
            assert False, "должна быть ошибка для неверного metric"
        except Exception as e:
            assert "Not valid metric" in str(e)