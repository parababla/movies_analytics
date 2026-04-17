import re
from collections import Counter


class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.data = self.read_file()
        """
        Put here any fields that you think you will need.
        """   

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
    

    def extract_genres(self, row):
        genres = [genre.strip() for genre in row.split('|') if genre.strip() != '']

        return genres
    

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
        
        try:
            new_string[2] = self.extract_genres(new_string[2])
        except:
            raise Exception("Invalid data types in the line!")
            
        return new_string


    def extract_year(self):
        years = []
        for row in self.data:
            title = row[1]
            if '(' in title and ')' in title:
                match = re.search(r'\(\s*(\d{4})\s*\)', title)
                if match:
                    try:
                        years.append(int(match.group(1)))
                    except:
                        raise Exception("Can't handle year!")
        
        return years

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        return dict(sorted(Counter(self.extract_year()).items(), key=lambda item: item[1], reverse=True))
    
    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """
        all_genres = []
        for row in self.data:
            genres = row[2]
            all_genres.extend(genres)

        return dict(sorted(Counter(all_genres).items(), key=lambda item: item[1], reverse=True))

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        future_dict = []
        for row in self.data:
            title = row[1]
            genres = row[2]
            genre_count = len(genres)
            future_dict.append((title, genre_count))
        
        future_dict.sort(key=lambda x: x[1], reverse=True)
        return dict(future_dict[:n])   