# Reviewer's Guide — APF Paper 9 v3.7 companion

This repository is an **executable appendix**, not a proof surface. The formal
mathematics is in `Paper_9_..._v3.7.pdf` and `..._Technical_Supplement_v1.1.pdf`.
Here you can (a) run nine finite witnesses, (b) read the typed closure ledger,
and (c) check the release contract. Nothing here upgrades a conditional or open
gate to a proved physical theorem.

## 1. What to verify in five minutes

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
python run_checks.py --verbose   # 9 passed, 0 failed, 9 total
python release_gate.py           # RESULT: PASS
```

`run_checks.py` prints each check's **actual** grade. You should see
`P_structural`, `P_structural_instrument`, and `P_structural_reading` — never a
blanket `[P]`. If any check imported a canonical-only `apf.*` module the run
would fail in this clean environment; it does not, because the canonical-bank
introspection legs are frozen into `apf/_release_fixtures.py`.

## 2. The conditional theorem spine (not a five-step derivation)

Paper 9 is a **dependency-explicit route**, and most of it is conditional or
open. The `G9.1–G9.20` tree in the manuscript is reproduced, typed, in
`theorems.json` and drawn in `interactive_dag.html`. The spine, in order:

1. **G9.1** finite complete operational basis — *conditional* on the named
   joint-realizability package; the exact **atom-cover model** is Engine-certified
   (checks 1–3).
2. **G9.2** realization as finite separating precision channels — **open gate**.
3. **G9.3** record topology Hausdorff + second countable — proved **under** a
   countable-grammar / topology-generation gate.
4. **G9.4–G9.6** finite smooth generation, subcartesian orbits, and the boxed
   kernel identity `ker Dβ = N^ctx` — each **under** a named smooth-generation /
   factorization gate; standard Sikorski / subcartesian / constant-rank imports
   are typed as imports.
5. **G9.7** intrinsic response-orbit quotient gauge and length — **proved**
   (APF-native).
6. **G9.8** physical substrate anchor `A = q ∘ Ds` — **open gate**.
7. **G9.9–G9.12** calibration, residual-energy law, positive cost metric, and the
   explicit result that **positive pullback geometry cannot supply Lorentzian
   signature** — proved, several under named riders.
8. **G9.13** signed Lorentz–Finsler causal structure — **open gate**.
9. **G9.16–G9.19** trace–volume identity, loaded equilibrium, the **no-trace
   gate** `Ptr K⁻¹J = 0`, and the conditional `γ_C = 1` weak-field exterior.
10. **G9.20** nonlinear Einstein closure — **external Paper 6 endpoint**.

## 3. Paper-specific gates (there ARE assumptions beyond PLEC)

The result is **not** "no paper-specific assumptions beyond the PLEC framework."
The load-bearing gates a referee should press are: the finite joint-extension
package (G9.1), operational-to-precision-channel realization (G9.2), the
countable specification grammar (G9.3), finite smooth generation (G9.4), smooth
response-factor completeness (G9.6), the physical substrate anchor (G9.8), signed
causal signature (G9.13), and the no-trace source law (G9.18). Each is a typed
node in the ledger, not a hidden step.

## 4. What the weak-field checks do and do not show

`check_T_gammaC_carrier_fork` and `check_T_weight_one_reduction` establish, in
exact rationals, that the four carrier closures solve to `γ_C ∈ {1, 1/3, 0, -1}`,
that the plane carrier matches the Einstein family only at `n = 3`, and that the
weight-one curve `γ(w) = w/((n-1)-w)` gives GR at `w = 1` in every dimension.
**They do not derive `w = 1`.** The Cassini datum (`γ - 1 = (2.1 ± 2.3)×10⁻⁵`)
sits `0.91σ` above the no-source bound `γ_C ≤ 1` — a live one-sided tension, not a
saturation. A `≥ 3σ` confirmed `γ_obs > 1` falsifies the composite.

The amount-graded-testedness trio (checks 7–9) is the discharge-hook lane for the
`TCP-strong [C]` boundary: it shows the floor invariant grades representation
rather than magnitude, and walks the distributed-encoding `(E)` door without
adopting or refuting it.

## 5. Finite witness ≠ proof-level falsification

A failing witness would flag a broken finite instance; a passing witness is a
consistency check on the manuscript's finite constructions and controls. Neither
is a symbolic proof, and neither closes an open gate. The DAG shows exactly one
executable witness per node that has one; the majority of nodes have none by
design.

## 6. Determinism

`generate_paper9_dag.py` regenerates `theorems.json`, `interactive_dag.html`, and
`paper9_typed_dependency_dag.json` deterministically from the ledger encoded in
that script. CI re-runs it and checks the outputs are unchanged.
