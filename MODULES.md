# Linked verification modules

The paper uses Git submodules so tests and provenance records can be shared with other papers
without copying or silently modifying them. Every module is pinned to an exact commit by the
paper repository.

| Module | Role in this paper |
|---|---|
| `modules/junction-ec-paper-audit` | Executable symbolic derivations, numerical reproductions, claim matrix, and 34 unit tests. |
| `modules/Arbiter` | Shared TEST 001–008 specifications and accepted reviews used by the audit provenance manifest. |
| `modules/parent-child-phase0` | Phase-zero equation-closure provenance. |
| `modules/parent-child-j0` | Kantowski–Sachs/Schwarzschild junction provenance. |
| `modules/parent-child-j1` | Einstein–Cartan boundary-analysis provenance. |
| `modules/parent-child-s1` | Spacelike-route analytic provenance. |
| `modules/parent-child-s1-evolution` | Short-time evolution provenance. |
| `modules/parent-child-s1-regularity` | Short-time regularity provenance. |
| `modules/parent-child-s1-numerical` | Bounded event-continuation output reproduced by the audit. |
| `modules/parent-child-s1-calibration` | Exact thermal-calibration output reproduced by the audit. |

## Verification

After cloning with `--recurse-submodules`, create the audit environment and run:

```sh
python3 -m venv modules/junction-ec-paper-audit/.venv
modules/junction-ec-paper-audit/.venv/bin/pip install -r modules/junction-ec-paper-audit/requirements.txt
modules/junction-ec-paper-audit/verify.sh
```

An existing compatible interpreter can be supplied without creating a module-local environment:

```sh
JUNCTION_AUDIT_PYTHON=/path/to/python modules/junction-ec-paper-audit/verify.sh
```

The verified 2026-08-09 linked-layout result is `JEC-A`, with JEC0–JEC8 passing and all 34 unit
tests passing.
