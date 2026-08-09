# Kantowski–Sachs–Schwarzschild junction paper

This repository contains the manuscript, figures, production scripts, cover letter, and
submission records for *A Strict Surface-Energy Obstruction for Timelike
Kantowski–Sachs–Schwarzschild Junctions*.

Reusable verification and provenance packages are linked as Git submodules under `modules/`.
Clone with submodules enabled:

```sh
git clone --recurse-submodules https://github.com/RonBibb/junction-ec-paper.git
```

To initialize modules after an ordinary clone:

```sh
git submodule update --init --recursive
```

The principal verification entry point is:

```sh
cd modules/junction-ec-paper-audit
./verify.sh
```

The paper repository pins every shared module to an exact commit. Updating a shared test or
provenance package does not alter the paper until its submodule pointer is intentionally updated.

