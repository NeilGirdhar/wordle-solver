from info import Info
from tree import Tree
from itertools import count

original_info = Info.create(history=[],
                            placed=' ' * 5,
                            extra_discovered='')
tree = Tree.create(original_info, False, False)

for solution in tree.possible_solutions:
    info = original_info
    guess = 'raise'
    print("Solution:", solution)
    for i in count(1):
        print("  Guessing:", guess)
        info = info.add_guess(guess, solution)
        if guess == solution:
            break
        other_tree = Tree.create(info, False, False)
        guess = other_tree.best_guess(info)
