# GRG LaTeX submission package

This directory uses the official Springer Nature journal class, version 3.1
(December 2024), with the numbered mathematics-and-physics reference style.

Main file: `KS_SCHWARZSCHILD_GRG.tex`

Verified outputs:

- `KS_SCHWARZSCHILD_GRG.pdf`: local `pdflatex` build.
- `GRG_COVER_LETTER_KS_SCHWARZSCHILD_2026-08-11.pdf`: separately uploaded cover letter.

The package has also been verified to compile on Overleaf. Re-export the
Overleaf PDF after uploading any source correction so that the rendered copy
contains the same archive DOI as the TeX source.

Compile locally with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error KS_SCHWARZSCHILD_GRG.tex
```

For Overleaf, upload the files in this directory together. Keep the manuscript,
`sn-jnl.cls`, `sn-mathphys-num.bst`, and both figure PDFs at the project root;
Springer Nature's submission guidance recommends avoiding figure subdirectories.
The cover letter is included for package completeness but should be uploaded in
the portal's separate cover-letter field rather than combined with the manuscript.

The static LaTeX manuscript is generated from the controlling Markdown source by
running `python3 build_grg_tex.py` from the repository root. Regenerate after any
scientific-content edit, then recompile and visually inspect the PDF.
