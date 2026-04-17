import os
import re
from collections import Counter

class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        if os.path.exists(path_to_the_file):
            self.path = path_to_the_file
            self.tags = self.select_tags(self.read_file())
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
        

    def select_tags(self, lines):
        tags = [line.split(',')[2] for line in lines]
        return tags

    
    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        
        Метод возвращает n верхних тегов с наибольшим количеством слов внутри. 
        Это словарь, где ключи — теги, а значения — количество слов внутри тега.
        Удалите дубликаты. Отсортируйте по убыванию количества слов.
        """
        len_tags = [len(re.split(r'[ /:]+', tag)) for tag in self.tags]
        dict_len_tags = dict(zip(self.tags, len_tags))
        dict_len_tags = sorted(dict_len_tags.items(), key=lambda x: (-x[1], x[0]))[:n]
        big_tags = dict(dict_len_tags)
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.

        Метод возвращает n самых длинных тегов по количеству символов.
        Это список тегов. Удалите дубликаты. Отсортируйте по убыванию.
        """
        unique_tags = list(set(self.tags))
        big_tags = sorted(unique_tags, key=lambda x: (-len(x), x))

        return big_tags[:n]

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.

        Метод возвращает пересечение между n самыми популярными тегами с наибольшим 
        количеством слов внутри и n самыми длинными тегами по количеству символов.
        Удалите дубликаты. Это список тегов.
        """
        words = set(self.most_words(n).keys())
        longest = set(self.longest(n))
        big_tags = sorted(words.intersection(longest))
        return big_tags
        
    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.

        Метод возвращает наиболее популярные теги. 
        Это словарь, в котором ключи — это теги, а значения — их количество.
        Удалите дубликаты. Отсортируйте по убыванию количества.
        """
        tag_counter = Counter(self.tags)
        popular_tags = sorted(tag_counter.items(), key=lambda x: (-x[1], x[0]))[:n]

        return dict(popular_tags)
        
    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.

        Метод возвращает все уникальные теги, содержащие слово, указанное в качестве аргумента.
        Удалите дубликаты. Это список тегов. Отсортируйте его по названиям тегов в алфавитном порядке.
        """
        word = word.lower()
        tags_with_word = set()
        for tag in self.tags:
            if word in tag.lower():
                tags_with_word.add(tag)
        
        return sorted(tags_with_word)
