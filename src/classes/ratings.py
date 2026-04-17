import datetime
from collections import Counter

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path = path_to_the_file
        self.data = self.read_file()

    def str_handler(self,string):
        data = string.split(',')
        data = [i.strip() for i in data]

        if len(data) != 4:
            raise Exception("Invalid type of string in the file!")
    
        if not data[0].isdigit():
            raise Exception("Invalid data type in the first column")
        data[0] = int(data[0])
    
        if not data[1].isdigit():
            raise Exception("Invalid data type in the second column")
        data[1] = int(data[1])

        try:
            float(data[2])
        except ValueError:
            raise Exception("Invalid data type in the third column")
        data[2] = float(data[2])

        if not data[3].isdigit():
            raise Exception("Invalid data type in the fourth column")
        data[3] = int(data[3])
        
        return data
    
    def read_file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                next(file)
                data = []
                cnt = 0
                for line in file:
                    if cnt < 1000:
                        cnt += 1
                        try:
                            data.append(self.str_handler(line))
                        except:
                            raise Exception("Error of handling string.")
        except:
            raise Exception("File doesn't exist or it's uncorrect.")
        
        return data
    
    class Movies:
        def __init__(self, outer_instance, path_to_file):
            self.path = path_to_file
            self.outer = outer_instance
            self.ratings_data = outer_instance.data
            self.movies_data = self.read_file()
            self.union_data = self.tables_union() # [userId,movieId,rating,timestamp,title,genres]
        
        def str_handler(self,string):
            first_quote = False
            string = string + ','
            index = 0
            new_string = []
            i = 0
            while i < (len(string)):
                if (string[i] == '"' and not(first_quote)):
                    first_quote = True
                    index = i + 1
                    i+=1
                elif (string[i] == '"' and first_quote  and ((i+1) == len(string) or string[i+1]==',')):
                    first_quote = False
                    new_string.append(string[index:i].strip())
                    index = i + 2
                    i+=2
                elif (string[i] == ',' and not(first_quote)):
                    new_string.append(string[index:i].strip())
                    index = i + 1
                    i+=1
                else:
                    i+=1

            if len(new_string) != 3:
                raise Exception("Invalid type of string in the file!")
    
            if not new_string[0].isdigit():
                raise Exception("Invalid data type in the first column")
            new_string[0] = int(new_string[0])
            
            return new_string
    
        def read_file(self):
            try:
                with open(self.path, 'r', encoding='utf-8') as file:
                    next(file)
                    data = []
                    cnt = 0
                    for line in file:
                        if cnt < 1000:
                            cnt += 1
                            try:
                                data.append(self.str_handler(line.strip()))
                            except:
                                raise Exception("Error of handling string")
            except:
                raise Exception("File doesn't exist or it's uncorrect.")
            
            return data
    
        def tables_union(self):
            dict_movies = {}
            for row in self.movies_data:
                dict_movies[row[0]] = [row[1], row[2]]
                
            union_table = []
            for row in self.ratings_data:
                movie_info = dict_movies.get(row[1])
                if movie_info is not None:
                    new_row = row.copy()
                    new_row.extend(movie_info)
                    union_table.append(new_row)

            return union_table

        def extract_year_from_timestamps(self, time):
            try:
                dt_object = datetime.datetime.fromtimestamp(time)
                year = dt_object.year
            except:
                raise Exception("Can't handle time!")

            return year

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. (возрастание) You need to extract years from timestamps.!!!!!!!!!!!!!!!!!!!!!!!!
            """
            years = [self.extract_year_from_timestamps(row[3]) for row in self.union_data if row[3] != '']
            ratings_by_year = dict(sorted(Counter(years).items(), key=lambda item: item[0]))

            return ratings_by_year
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            rates = [row[2] for row in self.union_data if row[2] != '']
            ratings_distribution = dict(sorted(Counter(rates).items(), key=lambda item: item[0]))

            return ratings_distribution
        
        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            movies = [row[4] for row in self.union_data]
            top_movies = dict(sorted(Counter(movies).items(), key=lambda item: item[1], reverse=True)[:n])

            return top_movies
        
        
        def get_median(self, new_list):
            if not new_list:
                return 0.0
            
            new_list = sorted(new_list)
            length = len(new_list)
            half = length // 2
            median = 0

            if length % 2 == 0:
                median = (new_list[half] + new_list[half - 1]) / 2
            else:
                median = new_list[half]
            
            return round(median, 2)

        def get_average(self, new_list):
            if not new_list:
                return 0.0
            
            return round(sum(new_list) / len(new_list), 2)
        
        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            top_movies = {}
            
            if metric == 'average' or metric == 'median':

                values = {} # {title:[values for ratings]}
                for row in self.union_data:
                    if row[4] in values:
                        values[row[4]].append(row[2])
                    else:
                        values[row[4]] = [row[2]]

                if metric == 'average':
                    for key, value in values.items():
                        top_movies[key] = self.get_average(value)
                else:
                    for key, value in values.items():
                        top_movies[key] = self.get_median(value)
            else:
                raise Exception('Not valid metric')

            top_movies = dict(sorted(top_movies.items(), key=lambda item: item[1], reverse=True)[:n])

            return top_movies
        
        def get_variance(self, my_list):
            if not my_list:
                return 0.0
            
            aver = self.get_average(my_list)

            variance = sum([(x - aver)**2 for x in my_list]) / len(my_list)

            return round(variance, 2)

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance (дисперсия) of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            top_movies = {}
            values = {} # {title:[values for ratings]}

            for row in self.union_data:
                if row[4] in values:
                    values[row[4]].append(row[2])
                else:
                    values[row[4]] = [row[2]]

            for key, value in values.items():
                top_movies[key] = self.get_variance(value)

            top_movies = dict(sorted(top_movies.items(), key=lambda item: item[1], reverse=True)[:n])

            return top_movies

    class Users(Movies):
        """
        In this class, three methods should work. 
        The 1st returns the distribution (распределение) of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies :DDDDDDDDDDDDDDD. Several methods are similar to the methods from it.
        """
        def __init__(self, movies_instance):
            self.union_data = movies_instance.union_data

        def dist_by_users(self):
            users_distribution = dict(Counter([row[0] for row in self.union_data]))

            return users_distribution

        def dist_by_metric(self, metric='average'):
            users = {}
            
            if metric == 'average' or metric == 'median':

                values = {} # {title:[values for ratings]}
                for row in self.union_data:
                    if row[0] in values:
                        values[row[0]].append(row[2])
                    else:
                        values[row[0]] = [row[2]]

                if metric == 'average':
                    for key, value in values.items():
                        users[key] = self.get_average(value)
                else:
                    for key, value in values.items():
                        users[key] = self.get_median(value)
            else:
                raise Exception('Not valid metric')

            return users

        def top_controversial(self, n):
            top_users = {}
            values = {} # {userid:[values for ratings]}

            for row in self.union_data:
                if row[0] in values:
                    values[row[0]].append(row[2])
                else:
                    values[row[0]] = [row[2]]

            for key, value in values.items():
                top_users[key] = self.get_variance(value)

            top_users = dict(sorted(top_users.items(), key=lambda item: item[1], reverse=True)[:n])

            return top_users
 