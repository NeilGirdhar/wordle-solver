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
history: list[tuple[str, str]] = [('raise', '     ')]

# Convert constants into known information.
info = Info.create(history)
tree = Tree.create(info, hard_mode, extended)
tree.display_instructions(info)
