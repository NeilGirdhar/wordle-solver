from info import Info
from tree import Tree

# The best opening guesses are:
# Guess     Worst case  Average case
# raise     168          61.00
# arise     168          63.72
# aesir     168          69.88
# reais     168          71.61
# serai     168          72.92
# ayrie     171          78.98
# aiery     171          87.03
# raile     173          61.33
# ariel     173          65.28
# aloes     174          77.35

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
n = len(tree.possible_solutions)

assert n > 0

def show() -> None:
    print(f"There are {n} possible solutions: {', '.join(tree.possible_solutions)}.")

if n == 1:
    print(f"The solution is '{next(iter(tree.possible_solutions))}'.")
elif n <= 10:
    show()
    steps, guess = tree.steps_to_solve()
    print(f"Guess '{guess}' to solve the problem in {steps} steps.")
else:
    if n < 30:
        show()
    else:
        print(f"There are {n} possible solutions.")
    best = tree.reduce_space(info)
    print("Guess     Worst case  Average case",
          *[f"{a}     {b}           {c:.2f}" for a, (b, c) in best[:12]], sep='\n')
