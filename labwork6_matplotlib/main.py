"""Labwork 6a: plot the assigned function and save po.pdf."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save figures without requiring a graphical desktop.
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIRECTORY = Path(__file__).resolve().parent


def create_plot():
    x = np.linspace(-5, 5, 1001)
    y = 2 * x + np.sin(x) ** 2 + 3
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(x, y)
    axis.set(title="hello, po!", xlabel="x", ylabel="y", xlim=(-5, 5))
    axis.grid(True)
    figure.tight_layout()
    return figure


def main():
    figure = create_plot()
    output = OUTPUT_DIRECTORY / "po.pdf"
    figure.savefig(output)
    plt.close(figure)
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
