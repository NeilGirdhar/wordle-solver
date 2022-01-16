from dataclasses import dataclass
from collections import defaultdict
from functools import cache

# toeas
# trained

# (8419, 'solei'), (8424, 'amies'), (8427, 'eyras'), (8427, 'osier'), (8427, 'resay'),
# (8427, 'sayer'), (8427, 'years'), (8450, 'saice'), (8454, 'anise'), (8465, 'paseo'),
# (8465, 'psoae'), (8466, 'aisle'), (8509, 'arise'), (8509, 'raise'), (8509, 'serai'),
# (8514, 'arose'), (8521, 'aeons'), (8529, 'aloes'), (8536, 'stoae'), (8536, 'toeas')

length = 5
discovered: str = ''
placed: str = 'sola '
history: list[str] = ['toeas', 'solan']
hard_mode = True

with open('twl06.txt') as f:
    words = f.readlines()

words = [word.strip()
         for word in words]
words = [word
         for word in words
         if len(word) == length]
print(f"Loaded {len(words)} words")

placed += ' ' * (length - len(placed))
discovered = set(discovered) | set(placed) - set(' ')
undiscovered = sorted(set(''.join(history)) - set(discovered))
possible_solutions = [word
                      for word in words
                      if (all(d in word for d in discovered)
                          and not any(u in word for u in undiscovered)
                          and all(all(w != h[i]
                                      for h in history)
                                  if p == ' '
                                  else w == p
                                  for i, (w, p) in enumerate(zip(word, placed, strict=True))))]
possible_guesses = possible_solutions if hard_mode else words
print(f"Trimmed down to {len(possible_solutions)} possible solutions")
if len(possible_solutions) < 10:
    print(*possible_solutions)

def most_new_info():
    def new_information(guess, solution):
        new_discovered = any(s in guess
                             for s in solution
                             if s not in discovered)
        if new_discovered:
            return True
        return any(p == ' ' and g == s and all(g != h[i] for h in history)
                   for i, (g, s, p) in enumerate(zip(guess, solution, placed)))

    c = []
    for guess in possible_guesses:
        s = sum(new_information(guess, solution)
                for solution in possible_solutions)
        c.append((guess, s))
    best = sorted(c, key=(lambda x_y: x_y[1]), reverse=True)
    print("Guesses that maximize information:", *[f"{a}: {b}" for a, b in best[:10]], sep='\n')

def best_gesses():
    def evaluate(guess, solution):
        new_discovered = frozenset(s
                                   for s in solution
                                   if s not in discovered
                                   if s in guess)
        new_placed = tuple(p == ' ' and g == s
                           for g, s, p in zip(guess, solution, placed))
        return new_discovered, new_placed

    bg = {}
    for guess in possible_guesses:
        c = defaultdict(int)
        for solution in possible_solutions:
            c[evaluate(guess, solution)] += 1
        bg[guess] = max(c.values())
    best = sorted(bg.items(), key=lambda x_y: x_y[1])
    print("Ideal guesses:", *[f"{a}: {b}" for a, b in best[:10]], sep='\n')

if len(possible_solutions) == 0:
    print("Error")
elif len(possible_solutions) == 1:
    pass
elif len(possible_solutions) < 800:
    best_gesses()
else:
    most_new_info()
