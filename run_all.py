from itertools import count

from info import Info
from tree import Tree

hard_mode = False
original_info = Info.create(history=[],
                            placed=' ' * 5,
                            extra_discovered='')
tree = Tree.create(original_info, hard_mode, False)

total_i = 0
worst = 0
for n, solution in enumerate(tree.possible_solutions):
    info = original_info
    guess = 'raise'
    # print("Solution:", solution)
    for i in count(1):
        # print("  Guessing:", guess)
        info = info.add_guess(guess, solution)
        if guess == solution:
            break
        other_tree = Tree.create(info, hard_mode, False)
        guess = other_tree.best_guess(info)
    total_i += i
    if 5 < i:
        print(i, solution)
    worst = max(worst, i)
    print(n + 1, total_i / (n + 1), worst)
