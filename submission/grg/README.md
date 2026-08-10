# GRG LaTeX submission package

This directory uses the official Springer Nature journal class, version 3.1
(December 2024), with the numbered mathematics-and-physics reference style.

Main file: `KS_SCHWARZSCHILD_GRG.tex`

Compile locally with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error KS_SCHWARZSCHILD_GRG.tex
```

For Overleaf, upload the files in this directory together. Keep the manuscript,
`sn-jnl.cls`, `sn-mathphys-num.bst`, and both figure PDFs at the project root;
Springer Nature's submission guidance recommends avoiding figure subdirectories.

The static LaTeX manuscript is generated from the controlling Markdown source by
running `python3 build_grg_tex.py` from the repository root. Regenerate after any
scientific-content edit, then recompile and visually inspect the PDF.
