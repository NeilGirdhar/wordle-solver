from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from string import ascii_lowercase
from typing import TypeVar

_set_lower = frozenset(ascii_lowercase)
T = TypeVar('T', bound='Info')


@dataclass(frozen=True)
class Info:
    discovered: frozenset[str]  # A set of characters.
    blocked: tuple[frozenset[str], ...]  # Five sets of characters blocked.

    @classmethod
    def create(cls: type[T],
               history: Sequence[str],
               placed: str,
               extra_discovered: str) -> T:
        """
        Args:
            history: Old guesses.
            placed: Five characters marking known characters at these positions, or space otherwise.
            extra_discovered: Besides the placed characters, these characters were discovered.
        """
        if len(placed) != 5:
            raise ValueError
        placed_set = frozenset(placed) - frozenset(' ')
        if placed_set - _set_lower:
            raise ValueError("Non-letters placed.")

        history_set = frozenset(''.join(history))
        if history_set - _set_lower:
            raise ValueError("Non-letters in history.")

        discovered = frozenset(extra_discovered) | placed_set
        if discovered - _set_lower:
            raise ValueError("Non-letters discovered.")

        if discovered - history_set:
            raise ValueError("You must be psychic.")

        blocked: list[frozenset[str]] = []
        # These characters were in the history, but not marked as discovered.  They can't be
        # anywhere.
        blocked_everywhere = history_set - discovered
        for i, p in enumerate(placed):
            if p != ' ':
                blocked.append(frozenset(_set_lower - set(p)))
                continue
            this_block = set(blocked_everywhere)  # Copy.
            for history_word in history:
                h = history_word[i]
                this_block.add(h)
            blocked.append(frozenset(this_block))
        return cls(frozenset(discovered), tuple(blocked))

    def trim(self, word_list: Iterable[str]) -> frozenset[str]:
        return frozenset(word
                         for word in word_list
                         if (all(d in word for d in self.discovered)
                             and not any(w in b
                                         for (w, b) in zip(word, self.blocked))))

    def add_guess(self, guess: str, solution: str) -> 'Info':
        discovered = self.discovered | frozenset(guess) & frozenset(solution)
        blocked_everywhere = frozenset(guess) - frozenset(solution)
        blocked = tuple(_set_lower - frozenset(g)
                        if g == s else
                        b | blocked_everywhere | {g}
                        for b, g, s in zip(self.blocked, guess, solution))
        assert not any(b == _set_lower
                       for b in blocked)
        return Info(discovered, blocked)
