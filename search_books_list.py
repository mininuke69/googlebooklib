

from googlebooklib import get_book_info
from icecream import ic
from typing import List
from googlebooklib import Book
from statistics import mean
from json import dump

"""
required:
folder "input" with kindle_collection.txt
folder "output"
googlebooklib.py


instructions:
- put your list in kindle_collection.txt
- run and wait for result
- results will appear inside /output/
"""



with open("input/kindle_collection.txt", "r") as file:
    lines = file.read().split("\n")

    lines_rm_extention = [title.removesuffix(".mobi") for title in lines]


    book_ratings = []
    errors = []

    for idx, query in enumerate(lines_rm_extention):
        #ic(f'query = {query}')
        results: List[Book] = []
        for result in get_book_info(book_name=query):
            #ic(result.title, result.averageRating)
            if result.averageRating:
                results.append(result)

        if not results:
            print(f'no results for {query}')
            errors.append({"query": query, "problem": "no results"})
            continue

        ratings = [book.averageRating for book in results]

        if not ratings:
            print(f'no ratings for {query}')
            errors.append({"quert": query, "problem": "no ratings"})
            continue
        
        rating_avg = mean(ratings)
        rating_top_result = ratings[0]

        progress = round(idx / len(lines) * 100, 2)
        ic(query, rating_avg, rating_top_result, progress)

        book_ratings.append({"query": query, "top": rating_top_result, "avg": rating_avg})




with open("output/ratings.json", "w") as output_ratings:
    dump(book_ratings, output_ratings)

with open("output/not_found.json", "w") as output_not_found:
    dump(errors, output_not_found)
