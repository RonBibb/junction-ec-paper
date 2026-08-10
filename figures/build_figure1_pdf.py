#!/usr/bin/env python3
"""Build the common-normal junction schematic as matching PDF and SVG files."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


HERE = Path(__file__).resolve().parent


def arrow(ax, start, end, *, filled=True, linewidth=1.6, color="black", scale=16):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>" if filled else "->",
            mutation_scale=scale,
            linewidth=linewidth,
            color=color,
        )
    )


def panel(ax, y0, case, retained, eps_c, chi_points_left):
    shell_x = 0.41
    height = 0.31
    ax.add_patch(Rectangle((0.04, y0), shell_x - 0.04, height,
                           facecolor="#e8eef5", edgecolor="black", linewidth=1.0))
    ax.add_patch(Rectangle((shell_x, y0), 0.55, height,
                           facecolor="#f4f1e7", edgecolor="black", linewidth=1.0))
    ax.plot([shell_x, shell_x], [y0, y0 + height], color="black", linewidth=4.0)

    ax.text(0.225, y0 + height - 0.045, case, ha="center", va="center",
            fontsize=12, fontweight="bold")
    ax.text(0.225, y0 + height - 0.090, retained, ha="center", va="center", fontsize=11)
    ax.text(0.685, y0 + height - 0.045, "retained Schwarzschild exterior",
            ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(0.685, y0 + height - 0.090, "contains spatial infinity",
            ha="center", va="center", fontsize=11)
    ax.text(shell_x + 0.012, y0 + 0.055, r"shell $\Sigma$",
            ha="left", va="center", fontsize=9.5, fontweight="bold", rotation=90)

    arrow(ax, (shell_x - 0.07, y0 + 0.155), (shell_x + 0.20, y0 + 0.155),
          linewidth=2.8, color="#8b1a1a", scale=20)
    ax.text(shell_x + 0.065, y0 + 0.188,
            r"one common $n=d\eta$, directed $M_C\to M_P$",
            ha="center", va="center", fontsize=10,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5})
    ax.text(0.235, y0 + 0.110, rf"$\epsilon_C={eps_c:+d}$",
            ha="center", fontsize=11, fontweight="bold")
    ax.text(0.68, y0 + 0.110, r"$\epsilon_P=+1$",
            ha="center", fontsize=11, fontweight="bold")

    chi_start, chi_end = ((0.33, 0.15) if chi_points_left else (0.15, 0.33))
    arrow(ax, (chi_start, y0 + 0.045), (chi_end, y0 + 0.045), filled=False)
    ax.text(0.24, y0 + 0.070, r"$+\chi$ coordinate direction", ha="center", fontsize=10)
    arrow(ax, (0.61, y0 + 0.045), (0.86, y0 + 0.045), filled=False)
    ax.text(0.735, y0 + 0.070, r"increasing $R$ toward infinity", ha="center", fontsize=10)


def main():
    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.5, 0.965, "One common normal and the two retained Kantowski–Sachs intervals",
            ha="center", va="center", fontsize=17, fontweight="bold")

    panel(ax, 0.54, "Case A", r"retain $\chi\leq\chi_\Sigma$", +1, False)
    panel(ax, 0.16, "Case B", r"retain $\chi\geq\chi_\Sigma$", -1, True)

    fig.savefig(HERE / "figure1_junction_orientation.pdf", bbox_inches="tight")
    fig.savefig(HERE / "figure1_junction_orientation.svg", bbox_inches="tight")
    plt.close(fig)
    print(HERE / "figure1_junction_orientation.pdf")
    print(HERE / "figure1_junction_orientation.svg")


if __name__ == "__main__":
    main()
