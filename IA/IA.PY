# IA.py
import json
import os
import random
import math
import time
from typing import List, Optional, Sequence, Any, Dict
import pathlib

def _rand():
    return random.uniform(-1.0, 1.0)

def _tanh(x: float) -> float:
    return math.tanh(x)

class Genetic_IA:
    def __init__(self, layers_size: Sequence[int], seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.layers_size = list(layers_size)
        if len(self.layers_size) < 2:
            raise ValueError("layers_size debe contener al menos input y output")

        self.layers = []  # cada elemento: {"weights": List[List[float]], "bias": List[float]}
        for i in range(len(self.layers_size) - 1):
            n_in = self.layers_size[i]
            n_out = self.layers_size[i + 1]
            weights = [[_rand() for _ in range(n_in)] for _ in range(n_out)]
            bias = [_rand() for _ in range(n_out)]
            self.layers.append({"weights": weights, "bias": bias})


    def load_from_path(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No existe el archivo: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        layers_data = data.get("layers", [])
        
        for idx, layer_data in enumerate(layers_data):
            if idx >= len(self.layers):
                break
            weights_data = layer_data.get("weights", [])
            bias_data = layer_data.get("bias", [])

            n_out = len(self.layers[idx]["bias"])
            n_in = len(self.layers[idx]["weights"][0]) if self.layers[idx]["weights"] else 0

            for r in range(min(n_out, len(weights_data))):
                row = weights_data[r]
                for c in range(min(n_in, len(row))):
                    self.layers[idx]["weights"][r][c] = float(row[c])

            for b in range(min(n_out, len(bias_data))):
                self.layers[idx]["bias"][b] = float(bias_data[b])

    def save_to_path(self, path: str):
        dirp = os.path.dirname(path)
        if dirp:
            os.makedirs(dirp, exist_ok=True)
        data = {"layers": self.layers}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def forward(self, inputs: Sequence[float]) -> List[float]:
        x = list(inputs)
        if len(x) != self.layers_size[0]:
            raise ValueError(f"inputs length {len(x)} != expected {self.layers_size[0]}")
        for layer in self.layers:
            n_out = len(layer["bias"])
            next_x = []
            for neuron_idx in range(n_out):
                weights = layer["weights"][neuron_idx]
                s = sum(w * xi for w, xi in zip(weights, x)) + layer["bias"][neuron_idx]
                next_x.append(_tanh(s))
            x = next_x
        return x

    def query(self, inputs: Sequence[float], threshold: float = 0.3) -> int:
        out = self.forward(inputs)
        if len(out) == 1:
            val = out[0]
            if val > threshold:
                return 1
            if val < -threshold:
                return -1
            return 0
        up = out[0]
        down = out[1]
        if down > up and down > threshold:
            return 1
        if up > down and up > threshold:
            return -1
        return 0