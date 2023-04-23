# Book Recommender System

This is a simple book recommender system that recommends similar books based on either the summary or genre of a given book. It uses a dataset of over 10,000 books from [Goodreads](https://www.goodreads.com/), a popular book review and recommendation website.

## Installation

To run this code, you will need to install the following Python libraries:

- pandas
- scikit-learn
- pillow

You can install them using pip, like so:
    pip install pandas scikit-learn pillow


## Usage

To use this recommender system, simply run the `recommend_books` function in the `book_recommender.ipynb` notebook. This function takes the following parameters:

- `book_name`: A string representing the name of the book to recommend similar books for.
- `type`: A string representing the type of similarity to use ('summary' or 'genres'; default = None).
- `k`: An integer representing the number of similar books to recommend (default = 5).

For example, to recommend 10 books similar to "The Hobbit" based on their summary, you can run the following code:

```python
    recommend_books('Pride and Prejudice', type='summary', k=3)
```

This will display the book details and cover images of the 3 most similar books based on their summaries.

## Sample Output

<div class="table-center">
  <table>
    <tr>
        <td>Recommendation 1</td>
        <td>Recommendation 2</td>
        <td>Recommendation 3</td>
    </tr>
      <td><img src="https://imgur.com/FeU1T9H.jpg" width="100" height="150"></td>
      <td><img src="https://i.imgur.com/fXtnEFh.png" width="100" height="150"></td>
      <td><img src="https://i.imgur.com/ioG5AD0.jpg" width="100" height="150"></td>
    </tr>
    <tr>
      <td>Dating Mr Darcy</td>
      <td>Mr Darcy Presents His Bride</td>
      <td>Pride And Prejudice And Zombies</td>
    </tr>
    <tr>
      <td>Rating: 3.56</td>
      <td>Rating: 3.79</td>
      <td>Rating: 3.3</td>
    </tr>
    <tr>
      <td> Kate O'Keeffe</td>
      <td> Helen Halstead</td>
      <td> Seth Grahame-Smith</td>
    </tr>
  </table>
</div>

## Credits
The dataset used in this project was scraped from Goodreads. The original dataset can be found [here](https://zenodo.org/record/4265096).

Dataset From:
Lorena Casanova Lozano and Sergio Costa Planells, “Best Books Ever Dataset”.
Zenodo, Nov. 09, 2020.
doi: 10.5281/zenodo.4265096.
