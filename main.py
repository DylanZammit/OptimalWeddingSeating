from typing import Tuple
from copy import deepcopy
import networkx as nx
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def karger(
        G: nx.Graph,
        k: int,
        n: int = 1_000,
        max_partition_size=None,
) -> Tuple[list[nx.Graph], float]:

    min_cut = np.inf
    min_partitions = None
    for i in range(1, n+1):
        if i % (n / 10) == 0:
            print(f'iteration {i} / {n}')
        partitions = {node: {node} for node in G.nodes()}
        G_contracted = nx.MultiGraph(deepcopy(G))
        while len(G_contracted) > k:
            weights = []
            edges = [
                (e1, e2) for e1, e2 in set(G_contracted.edges())
                if max_partition_size and len(partitions[e1].union(partitions[e2])) <= max_partition_size
            ]

            if len(edges) == 0:
                break

            for e in edges:
                weights.append(sum(w['weight'] for w in G_contracted.get_edge_data(*e).values()))

            weights = np.array(weights)
            p = weights / np.sum(weights)

            contracted_edge_idx = np.random.choice(len(p), p=p)
            u, v = edges[contracted_edge_idx]

            partitions[u] = partitions[u].union(partitions[v])
            partitions[v] = partitions[v].union(partitions[u])

            G_contracted = nx.contracted_nodes(G_contracted, u, v, self_loops=False)

        cut_edges = G_contracted.edges
        cut_value = sum(G_contracted.get_edge_data(*e)['weight'] for e in cut_edges)
        if cut_value < min_cut:
            min_cut = cut_value
            min_partitions = [v for k, v in partitions.items() if k in G_contracted.nodes]

            print(min_cut)

    return [G.subgraph(p) for p in min_partitions], min_cut


def load_data(fn: str) -> dict:
    df_rels = pd.read_csv(fn, index_col=0)

    guests = defaultdict(dict)
    for i, g1 in enumerate(df_rels.index):
        for j, g2 in enumerate(df_rels.columns):
            if i <= j:
                continue
            w = (df_rels[g1][g2] + 1) ** 2
            guests[g1][g2] = {'weight': w, 'weight_ts': 1000 - w}
    return guests


def main():

    guests = load_data('wedding_relationships.csv')

    G = nx.Graph(guests)
    min_partitions, min_cut = karger(G, 3, n=500, max_partition_size=4)

    optimal_tables = []
    for i, table in enumerate(min_partitions, start=1):
        if len(table) == 1:
            optimal_tables.append(table)
            continue

        print(f'Optimising seating of table {i}')

        seating = nx.approximation.greedy_tsp(table, weight='weight_ts')
        table_ts = table.edge_subgraph(list(nx.utils.pairwise(seating)))
        optimal_tables.append(table_ts)

    nx.draw_networkx(nx.union_all(optimal_tables))
    plt.show()


if __name__ == '__main__':
    main()
