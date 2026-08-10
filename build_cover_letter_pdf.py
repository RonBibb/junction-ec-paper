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

Please consider my manuscript, ``Surface-Energy Sign Classification for Timelike Kantowski--Sachs--Schwarzschild Junctions,'' for publication in \textit{General Relativity and Gravitation}. The manuscript identifies an invariant causal-sector split and explains geometrically why proposed black-hole-to-cosmology constructions placed inside the horizon are not subject to the exterior obstruction. Under the ordinary orientation, every compatible finite-rapidity junction from homogeneous Kantowski--Sachs geometry to the retained Schwarzschild $F>0$ exterior requires negative Israel surface density. In the complementary $F<0$ sector the ordering becomes sign-indefinite: paired future-infalling timelike witnesses in a regular chart realize opposite density signs for the same local bulk geometry and retained-side gluing, and an exact compatible choice has $p_s=-\sigma/2$, satisfying NEC, WEC, DEC, and the intrinsic shell SEC.

The Schwarzschild horizon is thereby identified as the invariant boundary between a universal negative-density exterior regime and an interior regime admitting fully energy-condition-satisfying local surface data. The manuscript does not claim to validate the dynamics of proposed completions or their generally spacelike transition layers. This combination of exact junction analysis, causal-sector classification, global branch control, and energy-condition analysis is well aligned with the scope of \textit{General Relativity and Gravitation}.

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
