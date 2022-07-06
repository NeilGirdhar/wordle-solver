from collections import defaultdict

import numpy as np
from scipy.stats import entropy


def read_and_strip(filename: str) -> list[str]:
    with open(filename) as f:
        return [word.rstrip() for word in f.readlines()]

words = read_and_strip('words.txt')
solutions = read_and_strip('solutions.txt')


def pattern(solution, word):
    retval = []
    for s, w in zip(solution, word):
        retval.append(1 if s > w else -1 if s < w else 0)
    return tuple(retval)


entropies = {}
for word in words:
    patterns = defaultdict(int)
    for solution in solutions:
        patterns[pattern(solution, word)] += 1
    bins = np.array(list(patterns.values()))
    entropies[word] = entropy(bins / len(solutions), base=2)

sorted_pairs = sorted((entropy_, word) for word, entropy_ in entropies.items())
print("\n".join(f"{word}: {entropy_}" for entropy_, word in sorted_pairs))
