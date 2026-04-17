import os
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter


class Links:

    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file):
        if os.path.exists(path_to_the_file):
            self.path = path_to_the_file
            file = self.read_file()
            self.movieId = self.select_movieId(file)
            self.imdbId = self.select_imdbId(file)
            self.tmdbId = self.select_tmdbId(file)
        else:
            raise FileNotFoundError(f"File did not exist: {path_to_the_file}")
    
    
    def read_file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:1001]
                lines = [line.strip() for line in lines]
            return lines
        except FileNotFoundError as e:
            print(e)
        

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
        movieTitle_budget = self.get_imdb(list_of_movies, ['Title', 'Budget'])
        title = [item[1] for item in movieTitle_budget]
        budget = [item[2] for item in movieTitle_budget]

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
        title_money_budget = self.get_imdb(list_of_movies, ['Title', 'Gross worldwide', 'Budget'])
        title = [item[1] for item in title_money_budget]
        money = [item[2] for item in title_money_budget]
        budget = [item[3] for item in title_money_budget]
        profit = [money[i] - budget[i] for i in range(len(title_money_budget))]
        most_profit = dict(zip(title, profit))
        most_profit = sorted(most_profit.items(), key=lambda x: (-x[1], x[0]))[:n]
        return dict(most_profit)


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
        title_time = self.get_imdb(list_of_movies, ['Title', 'Runtime'])
        title = [item[1] for item in title_time]
        time = [item[2] for item in title_time]
        most_long = dict(zip(title, time))
        most_long = sorted(most_long.items(), key=lambda x: (-x[1], x[0]))[:n]
        return dict(most_long)
        

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

        title_budget_time = self.get_imdb(list_of_movies, ['Title', 'Budget', 'Runtime'])
        title = [item[1] for item in title_budget_time]
        budget = [item[2] for item in title_budget_time]
        time = [item[3] for item in title_budget_time]
        cost = [round(budget[i] / time[i], 2) for i in range(len(title_budget_time))]
        most_cost = dict(zip(title, cost))
        most_cost = sorted(most_cost.items(), key=lambda x: (-x[1], x[0]))[:n]
        return dict(most_cost)