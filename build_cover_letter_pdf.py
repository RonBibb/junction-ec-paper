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

Please consider my manuscript, ``Surface-Energy Sign Classification for Timelike Kantowski--Sachs--Schwarzschild Junctions on the Ordinary Branch,'' for publication in \textit{General Relativity and Gravitation}. The manuscript identifies an invariant causal-sector split. Under the ordinary orientation, every compatible finite-rapidity junction from homogeneous Kantowski--Sachs geometry to the retained Schwarzschild $F>0$ exterior requires negative Israel surface density, and that ordering persists for a timelike crossing at $F=0$. In the complementary $F<0$ sector, with $\epsilon_P=+1$ and the increasing-$R$ Schwarzschild side retained, the ordering becomes sign-indefinite: two distinct future-infalling local embeddings through the same bulk event realize opposite density signs, and an exact compatible choice has $p_s=\sigma/2$, strictly satisfying NEC, WEC, DEC, and the intrinsic shell SEC.

The contribution is the combined causal-sector classification, exact positive-density interval, and explicit regular-chart witness construction, rather than the underlying general BKT junction formula. The Schwarzschild horizon is the invariant boundary between the classified open sectors, while sign indeterminacy begins strictly at $F<0$. The interior result is local and does not claim a global gluing, dynamics, or validation of generally spacelike transition layers. This combination of exact junction analysis, branch control, and energy-condition analysis is well aligned with the scope of \textit{General Relativity and Gravitation}.

The manuscript is original, is not under consideration elsewhere, and has been prepared independently without institutional or grant support. The archived manuscript source, figure-generation scripts, and verification suite are available through the stable Zenodo archive at \href{https://doi.org/10.5281/zenodo.21872425}{doi:10.5281/zenodo.21872425}; development history remains public at \href{https://github.com/RonBibb/junction-ec-paper}{github.com/RonBibb/junction-ec-paper}.

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
