# Optimal Wedding Seating
## Introduction
On the 30th of December 2024 we are organising a small wedding ceremony to celebrate
the 8 wonderful years spent together, and the lifetime of years remaining.

As part of the preparation, we are tasked with seating our 50 guests around 5 (or at most 6) round tables.
Initially this seemed like a simple task, but I soon realised the Game-of-Thrones-esque politics involved
in such a dangerous endeavour.

I was not facing a simple problem after all, and advanced mathematical techniques need to be sought after
in order to find an end to this dilemma.
## Problem Definition
Let $`n`$ be the number of people invited to the wedding, and let $`k`$ be the number of available round tables.
task is to find the optimal tables to seat these people around these tables. Each table should seat at most 10 people,
and ideally not much less. Furthermore, once the tables are chosen, the seating arrangement _within_ table needs to be chosen.
## Solution
We represent the set of $`n`$ people as a fully connected graph, where each edge $`e_{ij}`$ represents the relationship
between node (i.e. person) $`i`$ and node $`j`$. For simplicity, we let $`e_{ij}\in\{1, 2, \cdots, 10\}`$.
A pair of guests, typically couples, who would like to sit next to each other above all else, would have
a rating of 10. On the other end of the spectrum, two people who do not know each other (or do not want to sit next 
to each other), would have a score of 1. *Note*: A score of 0 would cause a division-by-zero error.

Once this fully connected graph is constructed, choosing the best set of $`k`$ partitions which minimises the "lost"
relationship connections is precisely the [Minimum k-cut problem](https://en.wikipedia.org/wiki/Minimum_k-cut), 
a natural extension of the [Minimum Cut problem](https://en.wikipedia.org/wiki/Minimum_k-cut). In particular, a heuristic
approach using the beautiful [Karger's Algorithm](https://en.wikipedia.org/wiki/Karger%27s_algorithm) is used.  A more detailed explanation is given in the Appendix below.

Once a table is chosen, we will make the assumption that a person will only care and interact with their immediate
neighbours. Thus each person has exactly two neighbours (since the table is circular), and so the cycle with maximal
weight needs to be found from a fully connected graph. This is another beautifully natural application
for the [Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)! We can seat the first person
and then choose (or travel to) another person, ideally who are friendly. This process is repeated until we arrive back
to the first person. Again, a more detailed explanation is given in the Appendix.
## Results
## Appendix
### Min k-cut Algorithm
### Travelling Salesman Problem