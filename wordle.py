from info import Info
from tree import Tree

# The best opening guesses are:
# Guess     Worst case  Average case
# raise     168          61.00086393088553
# arise     168          63.72570194384449
# aesir     168          69.8829373650108
# reais     168          71.61079913606912
# serai     168          72.92138228941684
# ayrie     171          78.98790496760259
# aiery     171          87.03542116630669
# raile     173          61.33088552915767
# ariel     173          65.28768898488121
# aloes     174          77.355939524838

# Settings.
hard_mode = False
extended = False

# Set constants for settings and past guesses.
history: list[str] = ['raise']
placed: str = '  i  '
extra_discovered: str = 'e'

# Convert constants into known information.
info = Info.create(history=history,
                   placed=placed + ' ' * (5 - len(placed)),
                   extra_discovered=extra_discovered)
tree = Tree.create(info, hard_mode, extended)

print(f"Trimmed down to {len(tree.possible_solutions)} possible solutions")


if len(tree.possible_solutions) == 0:
    print("Error")
elif len(tree.possible_solutions) == 1:
    print(f"The solution is '{next(iter(tree.possible_solutions))}'")
elif len(tree.possible_solutions) <= 10:
    print(*tree.possible_solutions)
    steps, guess = tree.steps_to_solve()
    print(f"Can be solved in {steps} by guessing '{guess}'")
else:
    best = tree.reduce_space(info)
    print("Guess     Worst case  Average case",
          *[f"{a}     {b}           {c:.2f}" for a, (b, c) in best[:12]], sep='\n')
