#!/usr/bin/env python3
"""Counts the total number of either words of `TwoGram`s in a text file.
"""

import sys
import argparse
from src.text_processing.freq_models import TwoGram, Frequency
from src.text_processing.freq_utils import tokenize_file, print_frequencies

__author__ = "Carson Brase"
__copyright__ = "Copyright 2023, Westmont College"
__credits__ = ["Carson Brase",
               "Donald J. Patterson", "Mike Ryu", ]
__license__ = "MIT"
__email__ = "mryu@westmont.edu"


def main() -> None:
    pars = setup_argument_parser()
    args = pars.parse_args()
    if args.processing_mode not in [1, 2]:
        pars.error("Processing mode must be either 1 (word) or 2 (twogram).")

    try:
        read = open(args.input_file_path, 'r', encoding='UTF-8')
        write = open(args.output_file_path, 'w', encoding='UTF-8')
        all_words = tokenize_file(read)

        if args.processing_mode == 1:
            word_freq_list = compute_word_freq(all_words)
        elif args.processing_mode == 2:
            word_freq_list = compute_twogram_freq(all_words)

        print_frequencies(word_freq_list, write)

        if args.verbose:  # DO NOT get rid of this -- this will be useful in debugging.
            pass
    except OSError as e:  # Leave this `except` block as-is.
        print("An error occurred while trying to open files:\n  ", e, file=sys.stderr)


def setup_argument_parser():
    pars = argparse.ArgumentParser()
    pars.add_argument("processing_mode", type=int,
                      help="required integer to select desired processing mode, either 1 (word) or 2 (twogram)")
    pars.add_argument("input_file_path", type=str,
                      help="required string containing the path to a text file to process")
    pars.add_argument("output_file_path", type=str,
                      help="required string containing the path to a text file to write the output to")
    pars.add_argument("-v", "--verbose", action="store_true",
                      help="switch to enable verbose mode to mirror (print) the output to console")
    return pars


def compute_word_freq(tokens: list[str]) -> list[Frequency]:
    """Takes the input list of words and processes it, returning a list of `Frequency`s.

    This function expects a list of lowercase alphanumeric strings (in any spoken language).
    If the input list is `None` or empty, an empty list is returned.

    There is one `Frequency` in the output list for every unique word in the original list.
    The frequency of each word is equal to the number of times that word occurs in the original list.

    Args:
        tokens (list[str]): list of lowercase words in any spoken language including numbers (e.g., 1, 123).
                            This list will not be modified.

    Yields:
        A list ordered by decreasing frequency, with tied words sorted lexicographically.

    Example:
        >>> word_freq = compute_word_freq(["this", "sentence", "repeats", "the", "word", "sentence"])
        >>> print(list(map(str, word_freq)))
        ["sentence:2", "repeats:1", "the:1", "this:1",  "word:1"]
    """
    # If input list is None or empty, an empty list is returned.
    if not tokens or tokens is None:
        return []

    freq_dict = {}

    # Count token frequencies and add them to dictionary
    for token in tokens:
        freq_dict[token] = freq_dict.get(token, 0) + 1
    
    freq_list = []
    for token in freq_dict:
        freq_list.append(Frequency(token, freq_dict.get(token)))

    freq_list.sort()

    return freq_list


def compute_twogram_freq(tokens: list[str]) -> list[Frequency]:
    """Takes the input list of words and processes it, returning a list of `Frequency`s.

    This function expects a list of tokens. If the input list is `None` or empty, an empty list is returned.

    There is one `Frequency` in the output list for every unique `TwoGram` in the original list.
    The frequency of each `TwoGram`s is equal to the number of times that `TwoGram` occurs in the original list.

    Args:
        tokens (list[str]): list of `TwoGrams`. This list will not be modified.

    Yields:
        A list ordered by decreasing frequency, with tied `TwoGram`s sorted lexicographically.

    Example:
        >>> import sys
        >>> from text_processing.freq_utils import print_frequencies
        >>> twogram_freq = compute_twogram_freq(["you", "think", "you", "know", "how", "you", "think"])
        >>> print_frequencies(twogram_freq, sys.stdout)
             6 total items
             5 unique items

             2 <you:think>
             1 <how:you>
             1 <know:how>
             1 <think:you>
             1 <you:know>
    """
    # If input list is 'None' or empty, an empty list is returned
    if tokens == [] or tokens is None:
        return []
    
    tgram_dict = {}

    for n in range(len(tokens) - 1):
        tgram = TwoGram(tokens[n],tokens[n+1])
        tgram_dict[tgram] = tgram_dict.get(tgram, 0) + 1

    tgram_list = []
    for tgram in tgram_dict:
        tgram_list.append(Frequency(tgram, tgram_dict.get(tgram)))
    
    tgram_list.sort()

    return tgram_list


if __name__ == '__main__':
    main()
