from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from typing import Type, TypeVar

import numpy as np

from info import Info, _set_lower

T = TypeVar('T', bound='Tree')
int_inf = 1000000


@dataclass(frozen=True)
class Tree:
    hard_mode: bool
    possible_guesses: frozenset[str]
    possible_solutions: frozenset[str]

    @classmethod
    def create(cls: Type[T], info: Info, hard_mode: bool, extended: bool) -> T:
        # Read word lists.
        def read_and_strip(filename: str) -> list[str]:
            with open(filename) as f:
                return [word.rstrip() for word in f.readlines()]

        words = read_and_strip('words.txt')
        solutions = read_and_strip('words.txt' if extended else 'solutions.txt')
        possible_guesses = info.trim(words) if hard_mode else frozenset(words)
        possible_solutions = info.trim(solutions)
        return cls(hard_mode, possible_guesses, possible_solutions)

    def generate_info(self) -> Info:
        word_list = self.possible_guesses if self.hard_mode else self.possible_solutions
        discovered = frozenset.intersection(*[frozenset(w) for w in word_list])
        blocked = [set(_set_lower)] * 5
        for word in word_list:
            for c, b in zip(word, blocked):
                b &= (_set_lower - set(c))
        return Info(discovered, tuple(frozenset(b) for b in blocked))

    def _steps_for_each_solution(self, info: Info, guess: str) -> int:
        """
        Returns:
            A list of entries for each possible solution of the number of steps to solve the problem
            assuming that solution is correct.
        """
        steps = []
        seen_info = set[Info]()
        for solution in self.possible_solutions:
            new_info = info.add_guess(guess, solution)
            if new_info in seen_info:
                continue
            seen_info.add(new_info)
            new_tree = Tree(self.hard_mode,
                            (new_info.trim(self.possible_guesses)
                                if self.hard_mode else self.possible_guesses),
                            new_info.trim(self.possible_solutions))
            if set(new_tree.possible_solutions) == set(self.possible_solutions):
                # Guess gives no new information with this solution.
                return int_inf
            worst = new_tree.steps_to_solve()[0]
            steps.append(worst + 1)
        return max(steps)

    @cache
    def steps_to_solve(self) -> tuple[int, str]:
        "Worst case number of possible steps after guess."
        if len(self.possible_solutions) <= 1:
            return 1, next(iter(self.possible_solutions))
        info = self.generate_info()
        best_steps, best_guess = min((self._steps_for_each_solution(info, guess), guess)
                                     for guess in self.possible_guesses)
        print(".", end="", flush=True)
        # print("With possible solutions", sorted(self.possible_solutions),
        #       f"it takes {best_steps} steps using the guess '{best_guess}'")
        return best_steps, best_guess

    def reduce_space(self, info: Info) -> list[tuple[str, tuple[int, float]]]:
        # Map from guess to tuple of
        # * worst case number of possible solutions after guess
        # * average case number of possible solutions after guess
        worst_case_for_guess = {}
        for guess in self.possible_guesses:
            c = defaultdict[Info, int](int)
            for solution in self.possible_solutions:
                c[info.add_guess(guess, solution)] += 1
            a = np.array(list(c.values()))
            worst_case = np.amax(a)
            average_case = np.average(a, weights=a)  # type: ignore[no-untyped-call]
            worst_case_for_guess[guess] = (worst_case, average_case)
        return sorted(worst_case_for_guess.items(), key=lambda x_y: x_y[1])
