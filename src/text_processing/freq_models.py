#!/usr/bin/env python
"""Provides `Pair`, `TwoGram`, and `Frequency` classes as data models for text processing.
"""

__author__ = "Carson Brase"
__copyright__ = "Copyright 2023, Westmont College"
__credits__ = ["Carson Brase",
               "Donald J. Patterson", "Mike Ryu", ]
__license__ = "MIT"
__email__ = "mryu@westmont.edu"


class Pair:
    """A simple `Pair` class that keeps two objects paired together.

    Attributes:
        _object1 (object): First object stored in the `Pair`, AKA `key`.
        _object2 (object): Second object stored in the `Pair`, AKA `value`.

    """

    def __init__(self, o1: object, o2: object) -> None:
        self._object1 = o1
        self._object2 = o2

    @property
    def object1(self) -> object:
        """Getter for `object1`."""
        return self._object1

    @object1.setter
    def object1(self, o1: object) -> None:
        """Setter for `object1`."""
        self._object1 = o1

    @property
    def object2(self) -> object:
        """Getter for `object2`."""
        return self._object2

    @object2.setter
    def object2(self, o2: object) -> None:
        """Setter for `object2`."""
        self._object2 = o2

    def __eq__(self, other: object) -> bool:
        """Compares `self` to `other` (object) given to return `True` if equal and `False` otherwise.

        Two `Pair`s are equal if both of their `key`s (`object1`s) and `value`s (`object2`s) are equal.

        Args:
            other: Object to compare to `self`. May be `None`.

        """
        # Check if null, check type, then check for same attributes
        if not isinstance(other, Pair):
            return False
        else:
            return self._object1 == other._object1 and self._object2 == other._object2

    def __str__(self) -> str:
        """Returns the string representation of `Pair` in this format: "<object1:object2>".

        If either `key` (`object1`) or `value` (`object2`) is `None`, "None" is used in their place.

        """
        if self._object1 == None:
            self._object1 = "None"
        if self._object2 == None:
            self._object2 = "None"

        return "<"+str(self._object1)+":"+str(self._object2)+">"

    def __hash__(self) -> int:
        """Returns the result of hashing both `key` and `value`.

        In other words, any `Pair` with the same `object1` and `object2` contents should have the same hash.

        """
        # This is provided for you to use as-is. No touchy!
        return hash((self._object1, self._object2))


class TwoGram(Pair):
    """An extension of the pair class that is specifically for a two-gram.
       The two tokens must be the same type, except `None` is allowed in any position.

    Attributes:
        _object1 (object): From superclass `Pair`. Represents the first token in a `TwoGram`.
        _object2 (object): From superclass `Pair`. Represents the second token in a `TwoGram`.

    """

    def __init__(self, token1: object, token2: object) -> None:
        if token1 is None or token2 is None or type(token1) == type(token2):
            super().__init__(token1, token2)
        else:
            raise ValueError("Two tokens must be of the same type.")

    @Pair.object1.setter
    def object1(self, o1) -> None:
        """Overriding setter for `object1` to enforce type symmetry."""
        if o1 is None or type(self._object2) == type(o1):
            self._object1 = o1
        else:
            raise ValueError("Two tokens must be of the same type.")

    @Pair.object2.setter
    def object2(self, o2) -> None:
        """Overriding setter for `object2` to enforce type symmetry."""
        if o2 is None or type(self._object1) == type(o2):
            self._object2 = o2
        else:
            raise ValueError("Two tokens must be of the same type.")

    def __eq__(self, other: object) -> bool:
        """Compares `self` to `other` (object) given to return `True` if equal and `False` otherwise.

        Two `TwoGram`s are equal if both of their `key`s (`object1`s) and `value`s (`object2`s) are equal.

        Args:
            other: Object to compare to `self`. May be `None`.

        """
        if other is not None and isinstance(other, TwoGram):
            return self._object1 == other._object1 and self._object2 == other._object2
        else:
            return False

    def __ne__(self, other: object) -> bool:
        """Complement of __eq__, used to support the `!=` (not equals) operation."""
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        """Returns `True` if `self` < `other`, `False` otherwise."""
        return self._compare_token_pairs(other) == -1

    def __le__(self, other: object) -> bool:
        """Returns `True` if `self` <= `other`, `False` otherwise."""
        return self._compare_token_pairs(other) <= 0

    def __gt__(self, other: object) -> bool:
        """Returns `True` if `self` > `other`, `False` otherwise."""
        return self._compare_token_pairs(other) == 1

    def __ge__(self, other: object) -> bool:
        """Returns `True` if `self` >= `other`, `False` otherwise."""
        return self._compare_token_pairs(other) >= 0

    def __hash__(self) -> int:
        """Reuses `Pair`'s hash method.

        This needs to be called explicitly because not doing so will implicitly set
         __hash___() to None because we are implementing __eq__ but not __hash__.

        """
        return super().__hash__()

    def _compare_token_pairs(self, other: object) -> int:
        """Java-style comparator method to make rich comparisons simpler.

        Returns -1 if self < other, 0 if self == other, and 1 if self > other.
        Types that do not match (including `NoneType`) are considered < any `TwoGram`.

        """
        if other is None or not isinstance(other, TwoGram):
            return 1
        else:
            first_tokens = _compare_tokens(self._object1, other._object1)
            if first_tokens:
                return first_tokens
            else:
                return _compare_tokens(self._object2, other._object2)


def _compare_tokens(t1: object, t2: object) -> int:
    """Helper function to deal with `NoneTypes`.

    Returns -1 if t1 < t2, 0 if t1 == t2, and 1 if t1 > t2.

    """
    if t1 is None and t2 is None:
        return 0
    else:
        if t1 is None:
            return -1
        elif t2 is None:
            return 1
        else:
            return 0 if t1 == t2 else -1 if t1 < t2 else 1


class Frequency:
    """Basic class for associating a word (`str`) or a `TwoGram` with its frequency.

    Attributes:
        _token (object): A word (`str`) or a `TwoGram` to associate with frequency.
        _freq (int): The number of occurrences for the associated `_token`.

    """
    def __init__(self, token: object, freq: int = 0) -> None:
        """Fully parameterized constructor to create a populated `Frequency`.

        Args:
            token (object): A word (`str`) or a `TwoGram` to associate with frequency.
            freq (int): The number of occurrences for the associated `_token`.
                the `freq` parameter should be > 1 for testing purposes ONLY.

        Raises:
             ValueError: If `token` parameter is not of type `str` or `TwoGram`.

        """
        self._token = token
        self._freq = freq

        if not isinstance(token, (str, TwoGram)):
            raise ValueError("A token must either be of type str or TwoGram.")
        if not isinstance(freq, int) or freq < 0:
            raise ValueError("Frequency must be an integer > 0")

    @property
    def token(self) -> object:
        """Getter for `token`."""
        return self._token

    @property
    def freq(self) -> int:
        """Getter for `freq`."""
        return self._freq

    def increment_freq(self) -> None:
        """Increments the freq by 1."""
        self._freq += 1

    def __eq__(self, other: object) -> bool:
        """Compares `self` to `other` (object) given to return `True` if equal and `False` otherwise.

        Two `Frequency`s are equal if both their `token`s and `freq`s are equal.

        Args:
            other: Object to compare to `self`. May be `None`.

        """
        return self._compare_frequency(other) == 0

    def __ne__(self, other: object) -> bool:
        """Complement of __eq__, used to support the `!=` (not equals) operation."""
        return self._compare_frequency(other) != 0

    def __lt__(self, other: object) -> bool:
        """Returns `True` if `self` < `other`, `False` otherwise."""
        return self._compare_frequency(other) == -1

    def __le__(self, other: object) -> bool:
        """Returns `True` if `self` <= `other`, `False` otherwise."""
        return self._compare_frequency(other) <= 0

    def __gt__(self, other: object) -> bool:
        """Returns `True` if `self` > `other`, `False` otherwise."""
        return self._compare_frequency(other) == 1

    def __ge__(self, other: object) -> bool:
        """Returns `True` if `self` >= `other`, `False` otherwise."""
        return self._compare_frequency(other) >= 0

    def __str__(self):
        """Returns the string representation of `Frequency` in this format: "token:freq"."""
        return f"{self._token}:{self._freq}"

    def __hash__(self) -> int:
        """Returns the result of hashing both `token` and `freq`.

        In other words, any `Frequency` with the same `token` and `freq` attributes should have the same hash.

        """
        return hash((self._token, self._freq))

    def _compare_frequency(self, other: object) -> int:
        """Java-style comparator method to make rich comparisons simpler.

        Returns -1 if self < other, 0 if self == other, and 1 if self > other.
        Types that do not match (including `NoneType`) are considered < any `Frequency`.

        """
        if other is None or not isinstance(other, Frequency):
            return 1
        else:
            if self._freq > other._freq:
                return -1
            elif self._freq == other._freq:
                if self._token == other._token:
                    return 0
                elif self._token < other._token:
                    return -1
                else:
                    return 1
            else:
                return 1
