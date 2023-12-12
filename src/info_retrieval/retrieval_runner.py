import pandas as pd
from nltk import FreqDist, corpus

from src.info_retrieval.retrieval import LegoSet
# from src.info_retrieval.retrieval import preprocess_and_tokenize
from src.text_processing.freq_counter import compute_word_freq
from src.text_processing.freq_models import Frequency


def get_user_input(prompt: str) -> str:
    """Helper function to get user input with a prompt."""
    return input(prompt)


def main() -> None:
    # User input #1: Lego set type based on prod_long_desc
    query_desc = get_user_input("What type of Lego set are you looking for? ")
    query_document = LegoSet(set_name="Query Set", list_price=0.0, piece_count=0,
                             prod_long_desc=query_desc, review_difficulty="Unknown")

    # Compute TF-IDF vector for the query
    query_vector = corpus.compute_tf_idf_vector(query_document)

    # Compute query relevance scores
    query_result = corpus.compute_query_relevance(query_vector)

    # Get the top 5 LegoSets with the highest relevance scores
    top_sets = corpus.get_top_k_sets(query_result, k=5)

    # User input #2: Lego set difficulty
    query_difficulty = get_user_input("What difficulty of Lego set are you looking for? ")
    # Filter results based on exact match to difficulty
    filtered_sets = [l_set for l_set in top_sets if l_set.review_difficulty.lower() == query_difficulty.lower()]

    # User input #3: Maximum price
    max_price = float(get_user_input("What is your maximum price for a Lego set? "))
    # Filter results based on price less than or equal to max_price
    final_sets = [l_set for l_set in filtered_sets if l_set.list_price <= max_price]

    # Print the final list of LegoSets
    print("Final List of Lego Sets:")
    for l_set in final_sets:
        print(l_set)