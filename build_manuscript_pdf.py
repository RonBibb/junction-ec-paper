#!/usr/bin/env python3
"""Convert the controlled Markdown manuscript to journal-style XeLaTeX."""

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "MANUSCRIPT_DRAFT_2026-08-07.md"
TMP = ROOT / "tmp" / "pdfs"
OUT = ROOT / "output" / "pdf"
TEX = TMP / "ks_schwarzschild_manuscript.tex"
PDF = OUT / "KS_SCHWARZSCHILD_MANUSCRIPT_SUBMISSION_READY_2026-08-08.pdf"


def text_escape(value: str) -> str:
    value = value.replace("–", "--").replace("—", "---").replace("−", "-")
    parts = re.split(r"(\\\(.*?\\\))", value)
    for i in range(0, len(parts), 2):
        s = parts[i]
        s = s.replace("\\", r"\textbackslash{}")
        for old, new in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")]:
            s = s.replace(old, new)
        s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
        s = re.sub(r"`(.+?)`", r"\\texttt{\1}", s)
        s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"\\emph{\1}", s)
        parts[i] = s
    return "".join(parts)


def table_to_tex(rows, caption=""):
    def split_row(row):
        row = row.strip().strip("|")
        cells, current, in_math = [], [], False
        i = 0
        while i < len(row):
            if row.startswith(r"\(", i):
                in_math = True
                current.extend(["\\", "("])
                i += 2
                continue
            if row.startswith(r"\)", i):
                in_math = False
                current.extend(["\\", ")"])
                i += 2
                continue
            if row[i] == "|" and not in_math:
                cells.append("".join(current).strip())
                current = []
            else:
                current.append(row[i])
            i += 1
        cells.append("".join(current).strip())
        return cells

    cells = [[text_escape(c) for c in split_row(row)] for row in rows]
    n = len(cells[0])
    spec = "@{}" + "X" * n + "@{}"
    out = [r"\begin{table}[H]", r"\centering"]
    if caption:
        out.append(r"\caption{" + text_escape(caption) + "}")
    out += [r"\small", rf"\begin{{tabularx}}{{\textwidth}}{{{spec}}}", r"\toprule"]
    out.append(" & ".join(cells[0]) + r" \\")
    out.append(r"\midrule")
    for row in cells[2:]:
        out.append(" & ".join(row) + r" \\")
    out += [r"\bottomrule", r"\end{tabularx}", r"\end{table}"]
    return out


def convert(lines):
    body = []
    title = ""
    author_lines = []
    i = 0
    in_refs = False
    appendix_started = False
    pending_table_caption = ""
    while i < len(lines):
        line = lines[i].rstrip("\n")
        if i == 0 and line.startswith("# "):
            title = line[2:].strip()
            i += 1
            continue
        if (line.startswith("**Ron Bibb**") or line.startswith("Independent Researcher")
                or line.startswith("Email:") or line.startswith("ORCID:")):
            author_lines.append(re.sub(r"\*\*", "", line).strip())
            i += 1
            continue
        if line.startswith("**Status:") or line.startswith("**Author work map:") or line.startswith("**Remaining scientific gate:"):
            i += 1
            continue
        if line.startswith("**Keywords:"):
            keywords = re.sub(r"^\*\*Keywords:\*\*\s*", "", line)
            body.append(r"\noindent\textbf{Keywords:} " + text_escape(keywords) + r"\par\medskip")
            i += 1
            continue
        if line.startswith("!["):
            match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            if match:
                figure_path = (ROOT / match.group(2)).resolve()
                vector_pdf = figure_path.with_suffix(".pdf")
                if vector_pdf.exists():
                    figure_path = vector_pdf
                body += [r"\begin{figure}[htbp]", r"\centering", rf"\includegraphics[width=\textwidth]{{{figure_path}}}"]
                i += 1
                while i < len(lines) and not lines[i].strip():
                    i += 1
                if i < len(lines) and lines[i].startswith("**Figure"):
                    cap = re.sub(r"^\*\*Figure\s+\d+\.\*\*\s*", "", lines[i].strip())
                    body.append(r"\caption{" + text_escape(cap) + "}")
                body += [r"\end{figure}"]
                i += 1
                continue
        if line == r"\[":
            eq = []
            i += 1
            while i < len(lines) and lines[i].strip() != r"\]":
                eq.append(lines[i].rstrip("\n"))
                i += 1
            content = "\n".join(eq)
            if r"\tag{" in content:
                body += [r"\begin{equation}", content, r"\end{equation}"]
            else:
                body += [r"\[", content, r"\]"]
            i += 1
            continue
        if re.match(r"^\*\*Table\s+\d+\.", line):
            pending_table_caption = re.sub(r"^\*\*Table\s+\d+\.\s*", "", line).strip()
            pending_table_caption = re.sub(r"\*\*$", "", pending_table_caption).strip()
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-|: ]+\|$", lines[i + 1].strip()):
            rows = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i].rstrip("\n"))
                i += 1
            body += table_to_tex(rows, pending_table_caption)
            pending_table_caption = ""
            continue
        if line.startswith("## References"):
            body += [r"\section*{References}", r"\begin{enumerate}[label={[\arabic*]},leftmargin=*]"]
            in_refs = True
            i += 1
            continue
        if in_refs and re.match(r"^\[\d+\]", line):
            body.append(r"\item " + text_escape(re.sub(r"^\[\d+\]\s*", "", line)))
            i += 1
            continue
        if in_refs and not line.strip():
            i += 1
            continue
        if line.startswith("## "):
            appendix_match = re.match(r"^## Appendix [A-Z]\.\s*(.*)$", line)
            if appendix_match:
                if not appendix_started:
                    body.append(r"\appendix")
                    appendix_started = True
                body.append(r"\section{" + text_escape(appendix_match.group(1)) + "}")
            elif line in ("## Acknowledgments", "## Data and code availability"):
                body.append(r"\section*{" + text_escape(line[3:]) + "}")
            else:
                body.append(r"\section{" + text_escape(re.sub(r"^\d+\.\s*", "", line[3:])) + "}")
            i += 1
            continue
        if line.startswith("### "):
            body.append(r"\subsection{" + text_escape(re.sub(r"^\d+(?:\.\d+)*\s*", "", line[4:])) + "}")
            i += 1
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(r"\item " + text_escape(lines[i][2:].strip()))
                i += 1
            body += [r"\begin{itemize}"] + items + [r"\end{itemize}"]
            continue
        if not line.strip():
            body.append("")
            i += 1
            continue
        if line.startswith("> "):
            body += [r"\begin{quote}", text_escape(line[2:]), r"\end{quote}"]
            i += 1
            continue
        para = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |\\\[|!\[|> )", lines[i]):
            para.append(lines[i].strip())
            i += 1
        body.append(text_escape(" ".join(para)) + "\n")
    if in_refs:
        body.append(r"\end{enumerate}")
    author = author_lines[0] if author_lines else "Ron Bibb"
    author_details = r"\\\small ".join(text_escape(line) for line in author_lines[1:])
    preamble = rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{amsmath,amssymb}}
\usepackage{{graphicx}}
\usepackage{{booktabs,tabularx,array}}
\usepackage{{float}}
\usepackage{{enumitem}}
\usepackage{{microtype}}
\usepackage[hidelinks]{{hyperref}}
\usepackage{{fancyhdr}}
\usepackage{{titlesec}}
\setlength{{\parindent}}{{1.2em}}
\setlength{{\parskip}}{{0.25em}}
\setlength{{\emergencystretch}}{{3em}}
\setlength{{\headheight}}{{14pt}}
\pagestyle{{fancy}}
\fancyhf{{}}
\fancyhead[L]{{Bibb}}
\fancyhead[R]{{Kantowski--Sachs/Schwarzschild Junctions}}
\fancyfoot[C]{{\thepage}}
\titleformat{{\section}}{{\large\bfseries}}{{\thesection.}}{{0.6em}}{{}}
\titleformat{{\subsection}}{{\normalsize\bfseries}}{{\thesubsection}}{{0.6em}}{{}}
\titlespacing*{{\section}}{{0pt}}{{2.2ex plus .8ex minus .2ex}}{{1.1ex}}
\title{{{text_escape(title)}}}
\author{{{text_escape(author)}\\\small {author_details}}}
\date{{8 August 2026}}
\begin{{document}}
\maketitle
\begin{{abstract}}
"""
    # Move abstract body inside abstract environment.
    try:
        abstract_start = body.index(r"\section{Abstract}")
        intro_start = body.index(r"\section{Introduction}")
        abstract = body[abstract_start + 1:intro_start]
        rest = body[:abstract_start] + body[intro_start:]
    except ValueError:
        abstract, rest = [], body
    return preamble + "\n".join(abstract) + "\n" + r"\end{abstract}" + "\n" + "\n".join(rest) + "\n" + r"\end{document}" + "\n"


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    tex = convert(SOURCE.read_text(encoding="utf-8").splitlines(True))
    TEX.write_text(tex, encoding="utf-8")
    env = dict(**__import__("os").environ)
    for _ in range(2):
        proc = subprocess.run(
            ["/Library/TeX/texbin/xelatex", "-shell-escape", "-interaction=nonstopmode", "-halt-on-error", TEX.name],
            cwd=TMP,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if proc.returncode:
            print(proc.stdout)
            return proc.returncode
    built = TEX.with_suffix(".pdf")
    PDF.write_bytes(built.read_bytes())
    print(PDF)
    return 0


if __name__ == "__main__":
    sys.exit(main())
