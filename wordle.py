from info import Info
from tree import Tree

# toeas
# retain
# trained

# Settings.
hard_mode = False
extended = True

# Set constants for settings and past guesses.
history: list[str] = ['toeas', 'relit', 'wheft']
placed: str = 're   '
extra_discovered: str = 'ethet'

# Convert constants into known information.
info = Info.create(history=history,
                   placed=placed + ' ' * (5 - len(placed)),
                   extra_discovered=extra_discovered)
tree = Tree.create(info, hard_mode, extended)

print(f"Trimmed down to {len(tree.possible_solutions)} possible solutions")
if len(tree.possible_solutions) < 10:
    print(*tree.possible_solutions)


if len(tree.possible_solutions) == 0:
    print("Error")
elif len(tree.possible_solutions) == 1:
    pass
elif len(tree.possible_solutions) < 20:
    steps, guess = tree.steps_to_solve()
    print(f"Can be solved in {steps} by guessing '{guess}'")
elif len(tree.possible_solutions) < 800:
    tree.reduce_space(info)
else:
    print("Fail for now")
