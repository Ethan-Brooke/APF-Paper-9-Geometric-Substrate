# APF Paper 9 — The Geometric Substrate as Cost Structure of Comparison Continuations

Companion repository for **Paper 9 v3.7** and its **Technical Supplement v1.1**
(Admissibility Physics Framework).

- Manuscript: `Paper_9_Geometric_Substrate_Cost_Structure_v3.7.pdf`
- Technical Supplement: `Paper_9_Geometric_Substrate_Cost_Structure_Technical_Supplement_v1.1.pdf`
- Zenodo (Paper 9 concept DOI): https://doi.org/10.5281/zenodo.20041675
- Canonical engine: APF-Engine **v24.3.427** (commit `7ab898e`, **3,918** bank-registered checks)

> **Reviewer-safe scope.** This repository accompanies Paper 9 v3.7 and Technical
> Supplement v1.1. The formal mathematical claims live in those documents. The
> local Python package executes a **declared subset of nine finite witnesses and
> falsifier controls**; those checks do not substitute for the symbolic proofs and
> do not convert conditional or open gates into proved physical theorems.
>
> The Paper 9 closure ledger distinguishes APF-native theorems, standard
> mathematical imports, conditional theorems, exact model certificates, named open
> gates, and the external Paper 6 nonlinear endpoint. The browser DAG
> (`interactive_dag.html`) displays that typed ledger. A local check is attached
> only where an executable witness exists.
>
> Current release status:
> - dependency closure: **conditional package**;
> - physical-realization closure: **explicitly open**;
> - local executable witnesses: **9 passing checks** (`python run_checks.py`);
> - canonical Engine receipt: commit `7ab898e`, full-bank `verify_all --bank-audit` **3,918/3,918 gap 0, Bucket A empty** (see `artifacts/`).

## What Paper 9 does and does not claim

Paper 9 establishes a **dependency-explicit route** from finite operational
comparison content to record topology, Sikorski differential structure,
subcartesian regular loci, smooth continuation orbits, and positive
response-orbit geometry. The general finite-basis theorem is **conditional on a
named joint-extension package** and is machine-witnessed exactly on the finite
atom-cover model. Physical precision-channel generation, finite smooth
generation, smooth response-factor completeness, the physical substrate anchor,
Lorentzian signature, the physical no-trace source law, and the nonlinear
Einstein endpoint remain **separately typed gates**. The weak-field trace
reduction is therefore a **conditional bridge, not an unconditional rederivation
of general relativity**.

## Quick start

```bash
python -m venv .venv && . .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e .
python run_checks.py            # runs the nine bundled checks
python run_checks.py --verbose  # per-check grade + key result
python release_gate.py          # static + runtime release contract
```

The only runtime dependency is `numpy`. The nine checks run in a fresh
environment with no access to the canonical engine: all canonical-bank /
cross-module introspection has been frozen into `apf/_release_fixtures.py`
(a build-time snapshot of the canonical census at commit `7ab898e`).

## The nine bundled checks (executable witnesses)

Each carries its **actual** registry grade — `P_structural`,
`P_structural_instrument`, or `P_structural_reading` — not plain `[P]`.

| # | Check | Grade | Paper 9 role |
|---|-------|-------|--------------|
| 1 | `check_T_finite_operational_basis_scope_contract` | `P_structural_instrument` | Names the atom-cover hypotheses; exact boundary N=0; no-amalgamation countermodel keeps the general bridge open |
| 2 | `check_T_finite_operational_basis` | `P_structural` | Exact finite atom-cover model witness; complete minimal basis with `|B_U| <= floor(C_U/eps*)` |
| 3 | `check_T_finite_minimal_joint_realization_atom_cover` | `P_structural` | One compatible minimum joint carrier; independent-minima control |
| 4 | `check_T_held_to_record_typing` | `P_structural_reading` | Held carrier / invariant record quotient / outcome instruments are three distinct typed objects on one record space |
| 5 | `check_T_gammaC_carrier_fork` | `P_structural` | Four-point carrier fork `gamma_C ∈ {1, 1/3, 0, -1}`; Cassini kills; weight-one curve |
| 6 | `check_T_weight_one_reduction` | `P_structural` | Deposit-fraction identity; exchange annihilation; scalar mode vanishes iff `w=1`. Does **not** derive `w=1` |
| 7 | `check_L_amount_graded_testedness_encoding_no_go` | `P_structural_instrument` | The GCC floor invariant grades representation, not magnitude (encoding wall) |
| 8 | `check_T_fagt2_encoding_argmin_pressure_and_read_channel` | `P_structural` | The (E) door: distributed encoding cost-maximal; strictly-superadditive flip gate pinned |
| 9 | `check_T_contention_law_granularity_occupancy_fork` | `P_structural` | Granularity dichotomy + occupancy fork; (c1-occ) evidence-shaped, not adopted |

The full Paper 9 closure ledger — including the conditional, open, external, and
model-certificate nodes that carry **no** local check — is in `theorems.json`
and rendered as a typed graph in `interactive_dag.html`.

## Trust hierarchy

```
formal proof in the manuscript / supplement
    + exact dependency/status ledger (theorems.json, interactive_dag.html)
    + executable finite witnesses and falsifier controls (apf/, run_checks.py)
```

Passing witness code does **not** by itself establish a theorem: the witnesses
are finite instances and falsifier controls. Where a node is conditional or open,
the ledger says so, and no local check changes that.

## Repository layout

```
Paper_9_..._v3.7.{tex,pdf}                 main manuscript
Paper_9_..._Technical_Supplement_v1.1.{tex,pdf}
apf/                                       nine self-contained checks + frozen fixtures
run_checks.py                              verifier (9 passed / 0 failed / 9 total)
release_gate.py                            static + runtime release contract (CI)
generate_paper9_dag.py                     regenerates theorems.json + interactive_dag.html
theorems.json                              typed Paper 9 closure ledger (9 bundled)
paper9_typed_dependency_dag.json           typed nodes + edges
interactive_dag.html                       browser view of the typed ledger
artifacts/                                 canonical Engine freeze receipts
ai_context/                                machine-readable context pack
```

## License

MIT (see `LICENSE`).
