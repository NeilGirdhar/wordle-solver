from dataclasses import dataclass
from string import ascii_lowercase
from typing import Any, Iterable, Sequence, TypeVar

import numpy as np
import numpy.typing as npt

IntegralArray = npt.NDArray[np.integer[Any]]
T = TypeVar('T', bound='Info')
U = TypeVar('U', bound='UnfrozenInfo')


def char_number(s: str) -> int:
    return ord(s) - ord('a')


@dataclass
class UnfrozenInfo:
    min_count: IntegralArray  # The minimum count of each character in the alphabet.
    max_count: IntegralArray  # The maximum count of each character in the alphabet.
    blocked: list[set[str]]  # Five sets of characters blocked.

    @classmethod
    def create(cls: type[U], history: Sequence[tuple[str, str]]) -> U:
        """
        Args:
            history: Pairs of guesses and results.  The result string is of the form:
                "g  y " where g are the placed letters and y are the misplaced ones.
        """
        assert all(len(h[i]) == 5 for h in history for i in range(2))
        guesses, results = zip(*history)

        retval = cls(min_count=np.zeros(26, dtype=np.int_),
                     max_count=5 * np.ones(26, dtype=np.int_),
                     blocked=[set[str]()] * 5)
        for guess, result in history:
            retval.update_min_max(guess, result)
        retval.polish()
        return retval

    def freeze(self) -> 'Info':
        return Info(tuple(self.min_count), tuple(self.max_count), tuple(frozenset(b)
                                                                        for b in self.blocked))

    def update_min_max(self, guess: str, result: str) -> None:
        seen = np.zeros(26, dtype=np.int_)
        for b, g, r in zip(self.blocked, guess, result):
            c = char_number(g)
            seen[c] += 1
            if r == " ":
                self.max_count[c] = min(self.max_count[c], seen[c] - 1)
            else:
                self.min_count[c] = max(self.min_count[c], seen[c])
            if r != 'g':
                b.add(g)

    def polish(self) -> None:
        for mc, letter in zip(self.max_count, ascii_lowercase):
            if mc == 0:
                for b in self.blocked:
                    if letter in b:
                        b.remove(letter)


@dataclass(frozen=True)
class Info:
    min_count: tuple[int, ...]  # The minimum count of each character in the alphabet.
    max_count: tuple[int, ...]  # The maximum count of each character in the alphabet.
    blocked: tuple[frozenset[str], ...]  # Five sets of characters blocked.

    @classmethod
    def create(cls, history: Sequence[tuple[str, str]]) -> 'Info':

        return UnfrozenInfo.create(history).freeze()

    def unfreeze(self) -> UnfrozenInfo:
        return UnfrozenInfo(np.array(self.min_count), np.array(self.max_count),
                            [set(b) for b in self.blocked])

    def trim(self, word_list: Iterable[str]) -> frozenset[str]:
        def counts(word: str) -> IntegralArray:
            return np.array(list(word.count(c) for c in ascii_lowercase))

        return frozenset(word
                         for word in word_list
                         for c in [counts(word)]
                         if np.all(self.min_count <= c)
                         if np.all(self.max_count >= c)
                         if not any(w in b
                                    for (w, b) in zip(word, self.blocked)))

    def add_guess(self, guess: str, solution: str) -> 'Info':
        u = self.unfreeze()
        result = [' '] * 5
        for c in ascii_lowercase:
            matches = sum(1
                          for g, s in zip(guess, solution)
                          if g == s == c)
            yellows = solution.count(c) - matches
            result = [r
                      if g != c else
                      'g'
                      if g == c == s else
                      'y' if (yellows := yellows - 1) > 0 else
                      ' '
                      for r, g, s in zip(result, guess, solution)]
        u.update_min_max(guess, "".join(result))
        return u.freeze()
