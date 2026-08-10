#!/usr/bin/env python3
"""Build the scaled static-family surface-stress plot as vector PDF."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).with_name("figure2_static_family.pdf")


def main():
    x = np.linspace(2.015, 8.0, 1601)
    root = np.sqrt(1 - 2 / x)
    sigma = -2 * root / x
    pressure = (x - 1) / (x * x * root)
    nec = (3 - x) / (x * x * root)
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    ax.plot(x, sigma, color="#1f4f7a", lw=2.4, label=r"$\widetilde{\sigma}_0$")
    ax.plot(x, pressure, color="#a64a29", lw=2.4, ls="--", label=r"$\widetilde{p}_{s0}$")
    ax.plot(x, nec, color="#2e7d32", lw=2.7,
            label=r"$\widetilde{\sigma}_0+\widetilde{p}_{s0}$")
    ax.axhline(0, color="black", lw=1.0)
    ax.axvline(3, color="0.35", lw=1.2, ls="--")
    ax.text(3.08, 1.80, r"photon sphere  $R_0=3m$", rotation=90,
            va="top", ha="left", fontsize=12, color="0.3")
    ax.annotate("NEC satisfied", xy=(2.63, 0.24), xytext=(2.18, 0.62),
                color="#2e7d32", fontsize=12, fontweight="bold",
                arrowprops={"arrowstyle": "-", "color": "#2e7d32"})
    ax.annotate("NEC violated", xy=(4.25, -0.09), xytext=(4.45, -0.63),
                color="#2e7d32", fontsize=12, fontweight="bold",
                arrowprops={"arrowstyle": "-", "color": "#2e7d32"})
    ax.set_xlim(2, 8)
    ax.set_ylim(-2, 2)
    ax.set_xlabel(r"Matched radius  $R_0/m$", fontsize=14)
    ax.set_ylabel("Scaled surface stress", fontsize=14)
    ax.grid(True, color="0.85", lw=0.7)
    ax.legend(loc="upper right", framealpha=0.95, fontsize=12)
    ax.tick_params(labelsize=12)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    plt.close(fig)
    print(OUT)


if __name__ == "__main__":
    main()
