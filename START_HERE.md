# Start here — APF Paper 9 v3.7 companion

You are looking at the executable companion to **Paper 9 v3.7** and **Technical
Supplement v1.1** of the Admissibility Physics Framework.

## Three entry points

1. **Read the papers.** `Paper_9_..._v3.7.pdf` (main, 61pp) and
   `..._Technical_Supplement_v1.1.pdf` (65pp) carry all formal claims.
2. **Run the checks.**
   ```bash
   python -m venv .venv && . .venv/bin/activate
   pip install -e .
   python run_checks.py --verbose
   ```
   Nine finite witnesses; expect `9 passed, 0 failed, 9 total`. Each prints its
   real grade (`P_structural` / `P_structural_instrument` / `P_structural_reading`).
3. **Read the ledger.** Open `interactive_dag.html` in a browser for the typed
   closure graph, or `theorems.json` for the machine-readable version.

## What this is

A **conditional dependency package** with an explicitly open physical-realization
frontier. The general finite-basis theorem is conditional on a named
joint-extension package and machine-witnessed exactly on the finite atom-cover
model; precision-channel generation, smooth generation, the physical substrate
anchor, Lorentzian signature, the no-trace source law, and the nonlinear Einstein
endpoint are separately typed gates. The nonlinear Einstein closure is an
**external Paper 6 endpoint**.

## What this is not

Not a self-contained proof of general relativity, and not a repository where
"every theorem traces to a passing check." Only the nine executable witnesses
carry local checks; the conditional, open, external, and model-certificate nodes
do not, by design.

## Canonical engine

APF-Engine **v24.3.427** (commit `7ab898e`, **3,918** bank-registered checks).
Freeze receipts are in `artifacts/` (`paper9_bank_audit.json`,
`paper9_interface_atlas.json`, `paper9_interface_ci.json`). The nine checks here
are vendored from that engine; canonical-bank introspection is frozen into
`apf/_release_fixtures.py` so this repo is self-contained.

## Corpus

Paper 9 sits in the APF corpus (Papers 0–48). The full paper list with DOIs is in
`repo_map.json` and `ai_context/PAPER_LINEAGE.md`. The engine is deposited as
Paper 21 (the Executable Constraint Framework).
