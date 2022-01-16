from collections import defaultdict

from info import Info
from reduce_space import reduce_space

# toeas
# retain
# trained

# Settings.
hard_mode = False

# Set constants for settings and past guesses.
history: list[str] = ['toeas']
placed: str = '  ea '
extra_discovered: str = 's'

# Convert constants into known information.
info = Info.create(history=history,
                   placed=placed + ' ' * (5 - len(placed)),
                   extra_discovered=extra_discovered)

# Read word lists.
def read_and_strip(filename: str) -> list[str]:
    with open(filename) as f:
        return [word.rstrip() for word in f.readlines()]

words = read_and_strip('words.txt')
solutions = read_and_strip('solutions.txt')
possible_solutions = info.trim(solutions)
possible_guesses = info.trim(words) if hard_mode else words

print(f"Trimmed down to {len(possible_solutions)} possible solutions")
if len(possible_solutions) < 10:
    print(*possible_solutions)

if len(possible_solutions) == 0:
    print("Error")
elif len(possible_solutions) == 1:
    pass
elif len(possible_solutions) < 800:
    reduce_space(info, possible_guesses, possible_solutions)
else:
    print("Fail for now")
