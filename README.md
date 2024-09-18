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
neighbours. Thus, each person has exactly two neighbours (since the table is circular), and so the cycle with maximal
weight needs to be found from a fully connected graph. This is another beautifully natural application
for the [Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)! We can seat the first person
and then choose (or travel to) another person, ideally who are friendly. This process is repeated until we arrive back
to the first person. Again, a more detailed explanation is given in the Appendix.
## Running the script
Firstly, make sure to have `conda` installed, and change directory to the root directory of this project and run the following command.
```bash
conda env create -n WeddingSeating -f environment.yaml
```
This should create the environment along with all the necessary libraries required, namely `pandas`, `numpy` and `netowrkx`.
The latter is used to create a Graph object with nodes and edges, allowing for easy manipulation of graphs. It is also used
to run a pre-built greedy Travelling Saleseman approximation algorithm for the second part of the problem.

Following these steps, we need to somehow supply the relationships between all pair of guests. This is done through a CSV file,
with an equivalent number of rows and columns containing names in the same order. The value at cell $`(i, j)`$ will correspond
to the relationship score between person $`i`$ and person $`j`$, in other words $`e_{ij}`$. Below is an example table.

|      | John | Paul   | George | Ringo | Eric | Bob  | Mick  | David | Keith |
| ------ | ---- | ---- | ------ | ----- | ---- | --- | ---- | ----- | ----- |
| John         |          | 8        | 7            | 7          | 3        | 5      | 4        | 2          | 4          |
| Paul         |          |          | 8            | 8          | 3        | 4      | 4        | 1          | 3          |
| George       |          |          |              | 8          | 9        | 3      | 4        | 2          | 4          |
| Ringo        |          |          |              |            | 6        | 5      | 5        | 3          | 5          |
| Eric         |          |          |              |            |          | 6      | 3        | 1          | 3          |
| Bob          |          |          |              |            |          |        | 5        | 5          | 4          |
| Mick         |          |          |              |            |          |        |          | 2          | 9          |
| David        |          |          |              |            |          |        |          |            | 3          |
| Keith        |          |          |              |            |          |        |          |            |            |

Notice how an upper-triangular matrix is enough to fully specify the matrix, since we are assuming a symmetric relationship.
The diagonals can obviously be neglected. Naming this `csv` file as `WeddingRelationships.csv` and saving it in the root directory
of the project means it will automatically be picked up and loaded as the relationship matrix.

Once this is done, we can run the following command by using the conda interpreted
```bash
/path/to/conda/env/python main.py
```
*TODO*: Include the relationship csv and number of tables as parameters to `main.py`.
## Results
Let us run the script to this dummy example shown above with just 9 people and 3 tables, each with at most 4 people.

Notice that these groups of people contain the full set of Beatles, Mick Jagger and Keith Richards, David Gilmour and Bob Dylan.
It seems natural that band member have a closer relationship than the others, and we would expect the model to place them
on the same tables.
![partition](https://github.com/DylanZammit/OptimalWeddingSeating/blob/master/img/toy_partition.png?raw=true)
From the results above we can see that the model indeed placed the Beatles on their own separate table, another table containing
both of the Stones members along with Eric and Bob. David Gilmour, however, was chosen to sit on a table alone. Cruel as this
may seem, the relationship matrix suggests that there is not much love between him and the rest of the guests.

Also notice how Mick Jagger and Keith Richards were placed right next to each other within the same table. This is the result
of the TSP optimisation problem. Ringo sits between George and Paul since he has a closer relationship with them than John.
## Appendix
### Min k-cut Algorithm
### Travelling Salesman Problem