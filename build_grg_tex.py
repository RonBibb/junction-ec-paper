#!/usr/bin/env python3
"""Build the self-contained Springer Nature/GRG LaTeX submission source."""

from pathlib import Path
import re

from build_manuscript_pdf import ROOT, SOURCE, convert, text_escape


SUBMISSION = ROOT / "submission" / "grg"
TEX = SUBMISSION / "KS_SCHWARZSCHILD_GRG.tex"


def convert_citations(text: str) -> str:
    """Convert the manuscript's numeric citations to natbib commands."""

    pinpoint = re.compile(r"\[(\d+),\s*([^\]]+)\]")

    def pinpoint_repl(match: re.Match[str]) -> str:
        number, note = match.groups()
        if re.fullmatch(r"\d+(?:,\d+)+", f"{number},{note}"):
            return match.group(0)
        note = note.replace("p. ", r"p.~").replace("pp. ", r"pp.~")
        note = note.replace("Eq. ", r"Eq.~").replace("Eqs. ", r"Eqs.~")
        return rf"\cite[{note}]{{ref{number}}}"

    text = pinpoint.sub(pinpoint_repl, text)

    def numeric_repl(match: re.Match[str]) -> str:
        keys = ",".join(f"ref{item}" for item in match.group(1).split(","))
        return rf"\cite{{{keys}}}"

    return re.sub(r"\[(\d+(?:,\d+)*)\]", numeric_repl, text)


def bibliography() -> str:
    entries = []
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\[(\d+)\]\s+(.*)$", line)
        if match:
            number, entry = match.groups()
            entries.append(rf"\bibitem{{ref{number}}} {text_escape(entry)}")
    return "\n\n".join(entries)


def manuscript_parts() -> tuple[str, str]:
    generated = convert(SOURCE.read_text(encoding="utf-8").splitlines(True))
    abstract = generated.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0].strip()
    body = generated.split(r"\end{abstract}", 1)[1].rsplit(r"\end{document}", 1)[0]
    body = body.split(r"\section*{References}", 1)[0].strip()
    body = re.sub(
        r"\\noindent\\textbf\{Keywords:\}.*?\\par\\medskip\s*",
        "",
        body,
        count=1,
        flags=re.DOTALL,
    )
    body = body.replace(str((ROOT / "figures" / "figure1_junction_orientation.pdf").resolve()),
                        "figure1_junction_orientation.pdf")
    body = body.replace(str((ROOT / "figures" / "figure2_static_family.pdf").resolve()),
                        "figure2_static_family.pdf")
    body = body.replace(r"\begin{figure}[htbp]", r"\begin{figure}[t]")
    body = body.replace(r"\begin{table}[H]", r"\begin{table}[t]")
    return convert_citations(abstract), convert_citations(body)


def main() -> int:
    SUBMISSION.mkdir(parents=True, exist_ok=True)
    abstract, body = manuscript_parts()
    title = text_escape(SOURCE.read_text(encoding="utf-8").splitlines()[0][2:])
    tex = rf"""% Springer Nature journal template, version 3.1 (December 2024).
% Prepared for submission to General Relativity and Gravitation.
% Keep this manuscript, sn-jnl.cls, and both figure PDFs in one directory.
\documentclass[pdflatex,sn-mathphys-num]{{sn-jnl}}

\usepackage{{graphicx}}
\usepackage{{amsmath,amssymb,amsfonts}}
\usepackage{{amsthm}}
\usepackage{{booktabs,tabularx,array}}
\usepackage{{float}}
\usepackage{{microtype}}

\raggedbottom
\setlength{{\emergencystretch}}{{3em}}

\begin{{document}}

\title[KS--Schwarzschild surface-energy classification]{{{title}}}

\author*[1]{{\fnm{{Ron}} \sur{{Bibb}}}}\email{{ronbibb@gmail.com}}
\affil*[1]{{\orgname{{Independent Researcher}},
  \orgaddress{{\city{{Lilburn}}, \state{{Georgia}}, \country{{USA}}}}}}

\abstract{{{abstract}}}

\keywords{{junction conditions, thin shells, Kantowski--Sachs spacetime,
Schwarzschild spacetime, surface energy conditions}}

\maketitle

{body}

\begin{{thebibliography}}{{20}}

{bibliography()}

\end{{thebibliography}}

\end{{document}}
"""
    TEX.write_text(tex, encoding="utf-8")
    print(TEX)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
