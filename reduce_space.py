from info import Info
from collections import defaultdict


def reduce_space(info: Info,
                 possible_guesses: list[str],
                 possible_solutions: list[str]) -> None:
    worst_case_for_guess = {}  # Worst case number of possible solutions after guess.
    for guess in possible_guesses:
        c = defaultdict[Info, int](int)
        for solution in possible_solutions:
            c[info.add_guess(guess, solution)] += 1
        worst_case_for_guess[guess] = max(c.values())
    best = sorted(worst_case_for_guess.items(), key=lambda x_y: x_y[1])
    print("Ideal guesses:", *[f"{a}: {b}" for a, b in best[:10]], sep='\n')
