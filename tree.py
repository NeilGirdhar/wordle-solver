from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from typing import Type, TypeVar

from info import Info, _set_lower

T = TypeVar('T', bound='Tree')


@dataclass(frozen=True)
class Tree:
    hard_mode: bool
    possible_guesses: tuple[str, ...]
    possible_solutions: tuple[str, ...]

    @classmethod
    def create(cls: Type[T], hard_mode: bool, info: Info) -> T:
        # Read word lists.
        def read_and_strip(filename: str) -> list[str]:
            with open(filename) as f:
                return [word.rstrip() for word in f.readlines()]

        words = read_and_strip('words.txt')
        solutions = read_and_strip('solutions.txt')
        possible_guesses = info.trim(words) if hard_mode else tuple(words)
        possible_solutions = info.trim(solutions)
        return cls(hard_mode, possible_guesses, possible_solutions)

    def generate_info(self) -> Info:
        word_list = self.possible_guesses if self.hard_mode else self.possible_solutions
        discovered = frozenset("".join(word_list))
        blocked = [set(_set_lower)] * 5
        for word in word_list:
            for c, b in zip(word, blocked):
                b &= (_set_lower - set(c))
        return Info(discovered, tuple(frozenset(b) for b in blocked))

    @cache
    def steps_to_solve(self) -> tuple[int, str]:
        "Worst case number of possible steps after guess."
        print("Running", hash(self), self.possible_solutions)
        if len(self.possible_solutions) <= 1:
            return 0, ""
        best_guess_steps = 1000000
        best_guess = ""
        info = self.generate_info()
        for guess in self.possible_guesses:
            s = set[Info]()
            worst_case_for_guess = 1000000
            for solution in self.possible_solutions:
                new_info = info.add_guess(guess, solution)
                if new_info in s:
                    continue
                s.add(new_info)
                new_tree = Tree(self.hard_mode,
                                (new_info.trim(self.possible_guesses)
                                 if self.hard_mode else self.possible_guesses),
                                new_info.trim(self.possible_solutions))
                if len(new_tree.possible_solutions) == 1:
                    steps_to_solve = 0
                elif set(new_tree.possible_solutions) == set(self.possible_solutions):
                    worst_case_for_guess = 1000000
                    break
                else:
                    steps_to_solve = new_tree.steps_to_solve()[0]
                worst_case_for_guess = min(worst_case_for_guess, steps_to_solve)
            if worst_case_for_guess < best_guess_steps:
                best_guess = guess
                best_guess_steps = worst_case_for_guess
        print("Returning", best_guess_steps, best_guess, self.possible_solutions)
        return best_guess_steps, best_guess

    def reduce_space(self, info: Info) -> None:
        worst_case_for_guess = {}  # Worst case number of possible solutions after guess.
        for guess in self.possible_guesses:
            c = defaultdict[Info, int](int)
            for solution in self.possible_solutions:
                c[info.add_guess(guess, solution)] += 1
            worst_case_for_guess[guess] = max(c.values())
        best = sorted(worst_case_for_guess.items(), key=lambda x_y: x_y[1])
        print("Ideal guesses:", *[f"{a}: {b}" for a, b in best[:10]], sep='\n')