# Evolution.py
import random
from typing import List
from IA.IA import Genetic_IA
from settings import MUTATION_PROB, MUTATION_STRENGTH

def merge(i_list: List[Genetic_IA]) -> Genetic_IA:
    if not i_list:
        raise ValueError("Merge necesita al menos una IA")

    base = i_list[0]
    child = Genetic_IA(base.layers_size)

    for layer_idx, layer in enumerate(child.layers):
        for r, row in enumerate(layer["weights"]):
            for c in range(len(row)):
                chosen = random.choice(i_list)
                layer["weights"][r][c] = chosen.layers[layer_idx]["weights"][r][c]

        for b in range(len(layer["bias"])):
            chosen = random.choice(i_list)
            layer["bias"][b] = chosen.layers[layer_idx]["bias"][b]

    return child


def mutate(ia: Genetic_IA):
    nw_ia=ia
    for layer in nw_ia.layers:
        for r, row in enumerate(layer["weights"]):
            for c in range(len(row)):
                if random.random() < MUTATION_PROB:
                    row[c] += random.uniform(-MUTATION_STRENGTH, MUTATION_STRENGTH)

        for b in range(len(layer["bias"])):
            if random.random() < MUTATION_PROB:
                layer["bias"][b] += random.uniform(-MUTATION_STRENGTH, MUTATION_STRENGTH)
    return nw_ia
