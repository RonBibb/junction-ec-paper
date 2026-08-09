#!/usr/bin/env python3
"""Build the GRG submission cover letter as a one-page PDF."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
TMP = ROOT / "tmp" / "pdfs"
OUT = ROOT / "output" / "pdf"
TEX = TMP / "grg_cover_letter.tex"
PDF = OUT / "GRG_COVER_LETTER_KS_SCHWARZSCHILD_2026-08-08.pdf"


TEX_SOURCE = r"""\documentclass[11pt]{letter}
\usepackage[margin=1in]{geometry}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}
\setlength{\parskip}{0.65em}
\setlength{\parindent}{0pt}
\signature{Ron Bibb\\Independent Researcher\\Lilburn, Georgia, USA\\\href{mailto:ronbibb@gmail.com}{ronbibb@gmail.com}\\ORCID: 0009-0004-1153-2464}
\address{Ron Bibb\\Independent Researcher\\Lilburn, Georgia, USA\\\href{mailto:ronbibb@gmail.com}{ronbibb@gmail.com}}
\date{8 August 2026}
\begin{document}
\begin{letter}{Editors\\\textit{General Relativity and Gravitation}}
\opening{Dear Editors,}

Please consider the manuscript ``A Strict Surface-Energy Obstruction for Timelike Kantowski--Sachs--Schwarzschild Junctions'' for publication in \textit{General Relativity and Gravitation}. We prove that a homogeneous Kantowski--Sachs region cannot be joined to the retained ordinary asymptotically flat Schwarzschild exterior across a timelike shell without negative surface energy density, for every finite shell rapidity and either admissible child-side orientation. For an exact static comoving family, the null energy condition additionally fails precisely outside the Schwarzschild photon sphere, with saturation at $R_0=3m$, and the paper supplies an explicit Nariai realization.

The significance of the result is that it separates an invariant obstruction caused by the Kantowski--Sachs product geometry from coordinate, trajectory, and orientation artifacts. It also supplies a classical boundary diagnostic for proposed black-hole-to-cosmology completions and for effective black-hole interiors formulated in Kantowski--Sachs variables. This combination of exact junction analysis, global branch bookkeeping, and energy-condition classification is well aligned with the scope of \textit{General Relativity and Gravitation}.

The manuscript is original, is not under consideration elsewhere, and has been prepared independently without institutional or grant support. Supporting symbolic derivations, numerical checks, and figure sources are available from the corresponding author upon reasonable request.

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
