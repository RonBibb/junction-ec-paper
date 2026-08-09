#!/usr/bin/env python3
"""Build the GRG submission cover letter as a one-page PDF."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
TMP = ROOT / "tmp" / "pdfs"
OUT = ROOT / "output" / "pdf"
TEX = TMP / "grg_cover_letter.tex"
PDF = OUT / "GRG_COVER_LETTER_KS_SCHWARZSCHILD_2026-08-09.pdf"


TEX_SOURCE = r"""\documentclass[11pt]{letter}
\usepackage[margin=1in]{geometry}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}
\setlength{\parskip}{0.65em}
\setlength{\parindent}{0pt}
\signature{Ron Bibb\\Independent Researcher\\Lilburn, Georgia, USA\\\href{mailto:ronbibb@gmail.com}{ronbibb@gmail.com}\\ORCID: 0009-0004-1153-2464}
\address{Ron Bibb\\Independent Researcher\\Lilburn, Georgia, USA\\\href{mailto:ronbibb@gmail.com}{ronbibb@gmail.com}}
\date{9 August 2026}
\begin{document}
\begin{letter}{Editors\\\textit{General Relativity and Gravitation}}
\opening{Dear Editors,}

Please consider my manuscript, ``A Strict Surface-Energy Obstruction for Timelike Kantowski--Sachs--Schwarzschild Junctions,'' for publication in \textit{General Relativity and Gravitation}. The manuscript extracts an invariant sufficient condition for negative Israel surface density: under the ordinary orientation, a timelike spherical shell joining a sector with $(\nabla R)^2\le0$ to one with $(\nabla R)^2>0$ must have $\sigma<0$. It then proves the strict Kantowski--Sachs/Schwarzschild realization: throughout the $F>0$ region outside the Schwarzschild horizon, every compatible finite-rapidity junction to the retained asymptotically flat exterior requires negative surface density for either explicitly retained Kantowski--Sachs interval. For an exact static comoving family, the null energy condition additionally fails precisely outside the Schwarzschild photon sphere, with saturation at $R_0=3m$, and an explicit Nariai product region supplies a local geometric witness.

The significance of the result is that it separates an invariant obstruction caused by the Kantowski--Sachs product geometry from coordinate, trajectory, and orientation artifacts. It also supplies a classical boundary diagnostic for proposed black-hole-to-cosmology completions and for effective black-hole interiors formulated in Kantowski--Sachs variables. This combination of exact junction analysis, global branch bookkeeping, and energy-condition classification is well aligned with the scope of \textit{General Relativity and Gravitation}.

The manuscript is original, is not under consideration elsewhere, and has been prepared independently without institutional or grant support. The manuscript source, figure-generation scripts, and verification suite are publicly available at \href{https://github.com/RonBibb/junction-ec-paper}{github.com/RonBibb/junction-ec-paper}.

Subject to the journal's conflict-of-interest checks, potential referees with relevant expertise include Jo\~ao L. Rosa, Sebastian Carloni, S. H. Mazharimousavi, Jos\'e M. M. Senovilla, and S. Khakshournia.

\closing{Sincerely,}
\end{letter}
\end{document}
"""


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    TEX.write_text(TEX_SOURCE, encoding="utf-8")
    proc = subprocess.run(
        ["/Library/TeX/texbin/xelatex", "-interaction=nonstopmode", "-halt-on-error", TEX.name],
        cwd=TMP,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if proc.returncode:
        print(proc.stdout)
        return proc.returncode
    PDF.write_bytes(TEX.with_suffix(".pdf").read_bytes())
    print(PDF)
    return 0


if __name__ == "__main__":
    sys.exit(main())
