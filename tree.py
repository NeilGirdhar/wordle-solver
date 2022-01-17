from collections import defaultdict
import numpy as np
from dataclasses import dataclass
from functools import cache
from typing import Type, TypeVar

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

    @cache
    def steps_to_solve(self) -> tuple[int, str]:
        "Worst case number of possible steps after guess."
        if len(self.possible_solutions) <= 1:
            # print("Running/returning 1 from", self.possible_solutions)
            return 1, ""
        # print("Running", self.possible_solutions)
        best_guess_steps = int_inf
        best_guess = ""
        info = self.generate_info()
        # print(self.possible_guesses)
        for guess in self.possible_guesses:
            s = set[Info]()
            worst_case_for_guess = 0
            for solution in self.possible_solutions:
                new_info = info.add_guess(guess, solution)
                if new_info in s:
                    continue
                s.add(new_info)
                new_tree = Tree(self.hard_mode,
                                (new_info.trim(self.possible_guesses)
                                 if self.hard_mode else self.possible_guesses),
                                new_info.trim(self.possible_solutions))
                if set(new_tree.possible_solutions) == set(self.possible_solutions):
                    # Guess gives no new information with this solution.
                    worst_case_for_guess = int_inf
                    break
                # if len(new_tree.possible_solutions) == 1:
                #     steps_to_solve = 2
                steps_to_solve = new_tree.steps_to_solve()[0] + 1
                worst_case_for_guess = max(worst_case_for_guess, steps_to_solve)
            if worst_case_for_guess < best_guess_steps:
                best_guess = guess
                best_guess_steps = worst_case_for_guess
        assert best_guess_steps != int_inf
        print("Returning", best_guess_steps, "with guess", best_guess, "from",
              self.possible_solutions)
        return best_guess_steps, best_guess

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
            average_case = np.average(a, weights=a)
            worst_case_for_guess[guess] = (worst_case, average_case)
        return sorted(worst_case_for_guess.items(), key=lambda x_y: x_y[1])
