#!/usr/bin/env python
# coding: utf-8

# Dataset From: 
# Lorena Casanova Lozano and Sergio Costa Planells, “Best Books Ever Dataset”. 
# Zenodo, Nov. 09, 2020. 
# doi: 10.5281/zenodo.4265096.

# Import necessary libraries

# csv parsing
import pandas as pd

# NLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cover image display
from PIL import Image
from IPython.display import display
import requests
from io import BytesIO

# Reading in the CSV
cols = ['bookId', 'author', 'title', 'rating', 'description', 'isbn', 'genres', 'coverImg']
data = pd.read_csv("book_data.csv", index_col="bookId", usecols=cols).dropna()

# Major NLP generating term frequency-inverse document frequency matrix

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['description'].values.astype('U'))

# Get names possible to the given book; Handles misspelled, incorrect case and other minor deviations

def get_possible_books(book:str) -> list:
    """
    Get possible books.
    This function takes a book title as input and returns a list of possible books whose titles contain the given input as a substring. It performs a case-insensitive search by converting both the input and book titles to lowercase before comparing them.

    Args:
    - book: A string representing the book title to search for.

    Returns:
    - A list of strings representing the possible book titles that match the search criteria.
    """
    
    book = book.lower()
    possible_books = []
    for name in data['title']:
        if book in name.lower():
            possible_books.append(name)
    return possible_books

# Generates the correct book name to be used for bookId indexing
# Tries to fix the name as close as it can or prompts the user from the closest available matches
# If it fails it simply returns 0

def correct_name(book_name:str):
    """
    Correct book name.
    This function takes a book title as input and checks if it is present in the `data` dataframe containing book titles. 
    If it is not found, it uses the `get_possible_books()` function to find a list of possible book titles that match the input. 
    If there is only one possible match, it returns the corresponding book title. 
    If there are multiple possible matches, it prints them and returns 1. 
    If there are no possible matches, it prints an error message and returns 0.

    Args:
    - book_name: A string representing the book title to check.

    Returns:
    - If the book title is found in `data`, the function returns the input `book_name`. 
    Otherwise, it returns either the matching book title or 1 (if there are multiple matches) or 0 (if there are no matches).

    Note: This function assumes that the `data` dataframe contains a column named `title` representing book titles. 
    It also relies on the `get_possible_books()` function defined elsewhere in the code.
    """
    if book_name not in data['title'].str.lower().tolist():
        possible_books = get_possible_books(book_name)

        if len(possible_books) == 1:
            return possible_books[0]

        print("Book not found!")
        if not possible_books:
            return 0

        print("Did you mean: ")
        for book in possible_books:
            print(book)
        return 1

# Translate the book's name to it's bookID to then have a unique ID.
# Uses the correct_name function to ensure the name can be looked up against the DataFrame

def name_to_bookId(book_name = None) -> str:
    """
    Convert book name to book ID.
    This function takes a book title as input and returns the corresponding book ID as a string. 
    It prompts the user for a book title if one is not provided. 
    It then uses the `correct_name()` function to check if the title is valid and find any possible corrections. 
    If a valid book title is found, it returns the index of the corresponding book in the `data` dataframe. 
    If there is an error or the input is invalid, it prints an error message and returns None.

    Args:
    - book_name: A string representing the book title to convert to a book ID.

    Returns:
    - If the input is valid and a corresponding book is found in `data`, the function returns the book ID as a string. 
    Otherwise, it returns None.

    Note: This function assumes that the `data` dataframe contains a unique index representing each book. 
    It also relies on the `correct_name()` function defined elsewhere in the code.
    """
    try:
        # Prompt for name if not provided
        while not book_name:
            book_name = input("Book: ")

        book_name = book_name.lower()

        # Correct the name to nearest approximation by repeatedly asking or giving up
        print(book_name)
        if correct_name(book_name) == 0:
            return None
        elif correct_name(book_name) == 1:
            name_to_bookId()
        
        bookId = data[data['title'].str.contains(book_name, case=False)].index[0]
        return bookId
    except:
        print("Invalid input.")

# Print book relevant details and uses the coverImg url to print the coverpage

def print_book_details(bookId_list:list[str]) -> None:
    """
    Print book details.
    This function takes a list of book IDs as input and prints the corresponding book details. 
    For each book ID in the input list, it looks up the relevant details.

    Args:
    - bookId_list: A list of strings representing the book IDs to print details for.

    Returns:
    - None.
    """
    for bookId in bookId_list:
        book_title = data.loc[bookId]['title']
        book_author = data.loc[bookId]['author']
        book_rating = data.loc[bookId]['rating']
        book_genres = data.loc[bookId]['genres']
        cover_url = data.loc[bookId]['coverImg']
        response = requests.get(cover_url)
        img = Image.open(BytesIO(response.content))
        display(img)
        print(f"Title: {book_title}")
        print(f"Author: {book_author}")
        print(f"Rating: {book_rating}")
        print(f"Genres: {book_genres}")
        print("\n")


# NLP against the book summaries

def similar_summary(bookId:str, k = 5) -> list:
    """
    Get similar books based on summary.
    Takes a book ID as input and returns a list of the `k` most similar books based on the summary. 
    
    Args:
    - bookId: A string representing the book ID to find similar books for.
    - k: An integer representing the number of similar books to return (default = 5).

    Returns:
    - A list of `k` strings representing the book IDs of the most similar books.
    """
    
    similarity_scores = cosine_similarity(tfidf_matrix[data.index.get_loc(bookId)], tfidf_matrix)
    similar_books = list(enumerate(similarity_scores[0]))
    sorted_similar_books = sorted(similar_books, key=lambda x: x[1], reverse=True)
    recommended_books = []
    for i in range(1, k+1):
        book_bookId = data.iloc[sorted_similar_books[i][0]].name
        recommended_books.append(book_bookId)
    return recommended_books

# KNN against the book genres

def similar_genre(bookId: str, k: int = 5) -> str:
    """
    Get similar books based on genre.
    Takes a book ID as input and returns a list of the `k` most similar books based on the genre. 
    
    Args:
    - bookId: A string representing the book ID to find similar books for.
    - k: An integer representing the number of similar books to return (default = 5).

    Returns:
    - A list of `k` strings representing the book IDs of the most similar books.
    """

    similarity_scores = cosine_similarity(tfidf_matrix[data.index.get_loc(bookId)], tfidf_matrix)
    similar_books = list(enumerate(similarity_scores[0]))
    sorted_similar_books = sorted(similar_books, key=lambda x: x[1], reverse=True)
    recommended_books = []
    for i in range(k+1, 2*k+1):
        book_bookId = data.iloc[sorted_similar_books[i][0]].name
        recommended_books.append(book_bookId)
    return recommended_books

# Main interface to call similarity generation

def recommend_books(book_name = None, type = None, k = 5) -> None:
    """
    Recommend similar books based on name, type, and k.

    This function takes a book name, type, and number of recommendations `k` as input.
    If `type` is not provided or is `None`, it combines the results of both similarity methods. 
    Finally, it calls the `print_book_details` function to display the details of the recommended books.

    Args:
    - book_name: A string representing the name of the book to recommend similar books for.
    - type: A string representing the type of similarity to use ('summary' or 'genres'; default = None).
    - k: An integer representing the number of similar books to recommend (default = 5).

    Returns:
    - None.
    """
    bookId = name_to_bookId(book_name)

    if type == 'summary':
        books = similar_summary(bookId, k)
    elif type == 'genres':
        books = similar_genre(bookId, k)
    elif not type:
        books = set(similar_summary(bookId, k) + similar_genre(bookId, k))
    
    print_book_details(books)

# Sample Usage: 
# recommend_books(book_name, type('genres', 'summary', None:Both), number_of_recommendations)

recommend_books('Pride and Prejudice', type = 'genres', k = 5)

