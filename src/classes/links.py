import os
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from classes.movies import Movies

class Links:

    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file, path_to_movie):
        if os.path.exists(path_to_the_file) and os.path.exists(path_to_movie):
            self.path = path_to_the_file
            file = self.read_file()
            self.movieId = self.select_movieId(file)
            self.imdbId = self.select_imdbId(file)
            self.tmdbId = self.select_tmdbId(file)
            self.dict_title = self.select_title(path_to_movie)
        else:
            raise FileNotFoundError(f"File did not exist: {path_to_the_file} or {path_to_movie}")


    def read_file(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            lines = []
            line_number = -1
                
            for line in file:
                line_number += 1
                line = line.strip()

                if line_number == 0 and line != "movieId,imdbId,tmdbId":
                    raise Exception(f"Incorrect file header")
                
                if line_number == 0:
                    continue

                if len(lines) >= 1000:
                    break
                    
                data = line.split(',')
                    
                if len(data) != 3:
                    raise Exception(f"Invalid type of string in the file")
                    
                if not data[0].strip().isdigit():
                    raise Exception(f"Invalid data type in the first column")
                    
                if not data[1].strip().isdigit():
                    raise Exception(f"Invalid data type in the second column")
                    
                # if not data[2].strip().isdigit():
                #     raise Exception(f"Invalid data type in the third column")
                    
                lines.append(line)
            if len(lines) == 0:
                raise Exception("File contains no data or only header")              
        return lines

    def select_title(self, path_to_movie):
        movies = Movies(path_to_movie)
        movieId = [line[0] for line in movies.data]
        titles = [line[1] for line in movies.data]
        dict_title = dict(zip(movieId, titles))
        return dict_title

    def select_movieId(self, lines):
        movieId = [line.split(',')[0] for line in lines]
        return movieId
    
    def select_imdbId(self, lines):
        imdbId = [line.split(',')[1] for line in lines]
        return imdbId
    
    def select_tmdbId(self, lines):
        tmdbId = [line.split(',')[2] for line in lines]
        return tmdbId


    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.

        Метод возвращает список списков [movieId, field1, field2, field3, ...] для списка фильмов, переданного в качестве аргумента (movieId).
        Например, [movieId, режиссёр, бюджет, совокупные мировые кассовые сборы, продолжительность].
        Значения должны быть получены с веб-страниц фильмов на IMDB.
        Отсортируйте список по убыванию movieId.
        """
        imdb_info = []
        for i in range(len(list_of_movies)):
            film_info = []
            film_info.append(list_of_movies[i])
            imdbId_index = (self.movieId).index(list_of_movies[i])
            imdbId = self.imdbId[imdbId_index]
            for field in list_of_fields:
                film_info.append(self.imdb_parsing(imdbId, field))
            imdb_info.append(film_info)
        imdb_info.sort(key=lambda x: int(x[0]), reverse=True)
        return imdb_info
    

    def imdb_parsing(self, imdbId, field):
        url = f'https://www.imdb.com/title/tt{imdbId}/'
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "ru,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://finance.yahoo.com/",
        "Sec-Ch-Ua": '"Chromium";v="142", "YaBrowser";v="25.12", "Not_A Brand";v="99", "Yowser";v="2.5"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Site returnes {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        target = False

        match field.lower():
            case 'director':
                # Director
                director_label = soup.find('span', class_='ipc-metadata-list-item__label', string=lambda t: t and 'Director' in t)
                if director_label:
                    parent_li = director_label.find_parent('li')           
                    if parent_li:
                        director_links = parent_li.find_all('a', class_='ipc-metadata-list-item__list-content-item')
                        directors = [link.text.strip() for link in director_links]
                        target = directors
            case 'budget':
                # Budget
                budget_label = soup.find('span', class_='ipc-metadata-list-item__label', string=lambda t: t and 'Budget' in t)
                if budget_label:
                    parent_li = budget_label.find_parent('li')           
                    if parent_li:
                        budget_links = parent_li.find('span', class_='ipc-metadata-list-item__list-content-item')
                        budget = int(re.findall(r'[\d,]+', budget_links.text.strip())[0].replace(',',''))
                        target = budget
            case 'gross worldwide':
                # Gross worldwide
                gross_worldwide_label = soup.find('span', class_='ipc-metadata-list-item__label', string=lambda t: t and 'Gross worldwide' in t)
                if gross_worldwide_label:
                    parent_li = gross_worldwide_label.find_parent('li')           
                    if parent_li:
                        gross_worldwide_links = parent_li.find('span', class_='ipc-metadata-list-item__list-content-item')
                        gross_worldwide = int(re.findall(r'[\d,]+', gross_worldwide_links.text.strip())[0].replace(',',''))
                        target = gross_worldwide
            case 'runtime':
                # Runtime
                runtime_label = soup.find('span', class_='ipc-metadata-list-item__label', string=lambda t: t and 'Runtime' in t)
                if runtime_label:
                    parent_li = runtime_label.find_parent('li')           
                    if parent_li:
                        runtime_links = parent_li.find('span', class_='ipc-metadata-list-item__list-content-item--subText')
                        runtime = int(re.findall(r'[\d,]+', runtime_links.text.strip())[0])
                        target = runtime
            case 'title':
                # Title
                title_tag = soup.find('title')
                if title_tag:
                    title_text = title_tag.text.strip()
                    if title_text.endswith(' - IMDb'):
                        title_text = title_text[:-7] 
                    target = title_text
            case _:
                # Other
                other_label = soup.find(['span','a'], class_='ipc-metadata-list-item__label', string=lambda t: t and field in t)
                if other_label:
                    parent_li = other_label.find_parent('li')           
                    if parent_li:
                        other_links = parent_li.find_all(['span','a'], class_='ipc-metadata-list-item__list-content-item')
                        other = [link.text.strip() for link in other_links]
                        target = other
        return target


    def top_directors(self, n, list_of_movies):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.

        Метод возвращает словарь с n лучшими режиссёрами, где ключи — это режиссёры, 
        а значения — количество созданных ими фильмов.  
        Отсортируйте его по убыванию значений.
        """
        movieId_directors = self.get_imdb(list_of_movies, ['Director'])
        all_directors = []
        for _, directors in movieId_directors:
            if directors and directors != False:
                all_directors.extend(directors)

        directors_counter = Counter(all_directors)
        directors_top = sorted(directors_counter.items(), key=lambda x: (-x[1], x[0]))[:n]
        return dict(directors_top)


    def most_expensive(self, n, list_of_movies):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.

        Метод возвращает словарь с n самыми популярными фильмами, где ключи — это названия фильмов, 
        а значения — их бюджеты. Отсортируйте его по убыванию бюджета.
        """
        movieTitle_budget = self.get_imdb(list_of_movies, ['Budget'])
        budget_dict = {}
        for item in movieTitle_budget:
            movie_id = item[0]
            budget = item[1]
            budget_dict[movie_id] = budget
        
        title = [self.dict_title[int(movie_id)] for movie_id in list_of_movies]
        budget = [budget_dict[movie_id] for movie_id in list_of_movies]
        
        most_budgets = dict(zip(title, budget))
        most_budgets = sorted(most_budgets.items(), key=lambda x: (-x[1], x[0]))[:n]
        return dict(most_budgets)


    def most_profitable(self, n, list_of_movies):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.

        Метод возвращает словарь с n самыми популярными фильмами, где ключами являются названия фильмов, 
        а значениями — разница между совокупным доходом от проката по всему миру и бюджетом. 
        Отсортируйте словарь по убыванию разницы.
        """
        movie_data = self.get_imdb(list_of_movies, ['Gross worldwide', 'Budget'])
    
        gross_dict = {}
        budget_dict = {}
        
        for item in movie_data:
            movie_id = item[0]
            gross_worldwide = item[1]
            budget = item[2]
            gross_dict[movie_id] = gross_worldwide
            budget_dict[movie_id] = budget
        
        profit_dict = {}
        for movie_id in list_of_movies:
            if movie_id in gross_dict and movie_id in budget_dict:
                profit = gross_dict[movie_id] - budget_dict[movie_id]
                profit_dict[movie_id] = profit
        
        title_profit_pairs = []
        for movie_id in list_of_movies:
            if movie_id in profit_dict:
                title = self.dict_title[int(movie_id)]
                profit = profit_dict[movie_id]
                title_profit_pairs.append((title, profit))
        
        title_profit_pairs.sort(key=lambda x: (-x[1], x[0]))
        result = dict(title_profit_pairs[:n])
        
        return result


    def longest(self, n, list_of_movies):
        # в минутах
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.

        Метод возвращает словарь с n лучшими фильмами, где ключами являются названия фильмов, 
        а значениями — их продолжительность. Если есть несколько версий, выберите любую.
        Отсортируйте по убыванию продолжительности.
        """
        movie_data = self.get_imdb(list_of_movies, ['Runtime'])
    
        runtime_dict = {}
        for item in movie_data:
            movie_id = item[0]
            runtime = item[1]
            runtime_dict[movie_id] = runtime

        title_runtime_pairs = []
        for movie_id in list_of_movies:
            if movie_id in runtime_dict:
                title = self.dict_title[int(movie_id)]
                runtime = runtime_dict[movie_id]
                title_runtime_pairs.append((title, runtime))
        
        title_runtime_pairs.sort(key=lambda x: (-x[1], x[0]))
        result = dict(title_runtime_pairs[:n])
        
        return result
        

    def top_cost_per_minute(self, n, list_of_movies):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.

        Метод возвращает словарь с n лучшими фильмами, где ключи — это названия фильмов, 
        а значения — это бюджеты, делённые на продолжительность фильма. 
        Бюджеты могут быть в разных валютах — не обращайте на это внимания. 
        Значения должны быть округлены до двух знаков после запятой. Отсортируйте их по убыванию.
        """
        movie_data = self.get_imdb(list_of_movies, ['Budget', 'Runtime'])
        budget_dict = {}
        runtime_dict = {}
        
        for item in movie_data:
            movie_id = item[0]
            budget_dict[movie_id] = item[1]
            runtime_dict[movie_id] = item[2]
        
        cost_per_minute_dict = {}
        for movie_id in list_of_movies:
            if movie_id in budget_dict and movie_id in runtime_dict:
                cost = budget_dict[movie_id] / runtime_dict[movie_id]
                cost_per_minute_dict[movie_id] = round(cost, 2)
        
        title_cost_pairs = []
        for movie_id in list_of_movies:
            if movie_id in cost_per_minute_dict:
                title = self.dict_title[int(movie_id)]
                cost = cost_per_minute_dict[movie_id]
                title_cost_pairs.append((title, cost))
        
        title_cost_pairs.sort(key=lambda x: (-x[1], x[0]))
        result = dict(title_cost_pairs[:n])
        
        return result

   