import sys
import math
from typing import Dict, List
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import os
from src.vector_space.vector_space_models import Corpus, Document, Vector


class LegoSet:
    def __init__(self, set_name: str, list_price: float, piece_count: int,
                 prod_long_desc: str, review_difficulty: str):
        self.set_name = set_name
        self.list_price = list_price
        self.piece_count = piece_count
        self.prod_long_desc = prod_long_desc
        self.review_difficulty = review_difficulty

    def __str__(self):
        return f"LegoSet(set_name={self.set_name}, list_price={self.list_price}, " \
               f"piece_count={self.piece_count}, prod_long_desc={self.prod_long_desc}, " \
               f"review_difficulty={self.review_difficulty})"


class LegoCorpus(Corpus):
    def __init__(self, lego_sets: list[LegoSet], threads=1, debug=False):
        # Convert LegoSet instances to Document instances for the superclass
        lego_documents = [Document(title=l_set.set_name, words=[l_set.prod_long_desc], processors=None)
                          for l_set in lego_sets]

        super().__init__(lego_documents, threads, debug)

    def _compute_terms(self) -> dict[str, int]:
        """Override to compute terms based on prod_long_desc."""
        words = [word for doc in self.docs for word in doc.words]
        index_dict = self._build_index_dict(words)
        return index_dict

    def _compute_df(self, term) -> int:
        """Override to compute document frequency based on prod_long_desc."""
        if self._debug:
            print(f"Started working on DF for '{term}'")
            sys.stdout.flush()

        def check_membership(t: str, doc: Document) -> bool:
            """An efficient method to check if the term `t` occurs in a list of words `doc`."""
            return t in doc.words

        return sum([1 if check_membership(term, doc) else 0 for doc in self._docs])

    def _compute_tf_idf(self, term, doc=None, index=None):
        """Override to compute TF-IDF based on prod_long_desc."""
        dfs = self._dfs
        doc = self._get_doc(doc, index)

        df = dfs.get(term)
        if term in dfs.keys():
            tf = math.log10(1 + doc.tf(term))
            idf = math.log10(len(self.docs)/(1 + df))
            tf_idf = tf * idf

            if term in self._terms and len(self.docs) > 1:
                return tf_idf
        else:
            return 0.0

    def compute_tf_idf_vector(self, doc=None, index=None) -> Vector:
        """Override to compute TF-IDF vector based on prod_long_desc."""
        doc = self._get_doc(doc, index)
        all_tf_idfs = []

        for word in self._terms:
            tf_idf = self._compute_tf_idf(word, doc=doc)
            all_tf_idfs.append(tf_idf)

        vec = Vector(all_tf_idfs)
        return vec

    def _compute_term_scores(self) -> Dict[str, float]:
        """Compute scores for each term based on their IDF values."""
        term_scores = {}
        for term in self._terms:
            idf = math.log10(len(self.docs) / (1 + self._dfs.get(term, 0)))
            term_scores[term] = idf
        return term_scores

    def compute_query_relevance(self, query_vector: Vector) -> Dict[str, float]:
        """Compute relevance scores for each LegoSet based on the query vector."""
        query_result = {}
        term_scores = self._compute_term_scores()

        for title, doc_vector in self._tf_idf.items():
            relevance_score = doc_vector.cossim(query_vector)
            query_result[title] = relevance_score

        return query_result

    def get_top_k_sets(self, query_result: Dict[str, float], k: int = 5) -> List[LegoSet]:
        """Return the top k LegoSets with the highest relevance scores."""
        sorted_result = sorted([(title, score) for title, score in query_result.items()],
                               key=lambda item: item[1], reverse=True)[:k]

        top_k_sets = [set for set in self.docs if set.title in dict(sorted_result)]
        return top_k_sets


