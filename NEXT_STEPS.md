# NEXT_STEPS — Paper 9 v3.7.1 repository hotfix

The companion repository has been rebuilt as a **v3.7.1 repository hotfix**
(manuscript stays v3.7, Technical Supplement stays v1.1). It replaces the broken
`v3.7` release (empty DAG, missing modules, stale metadata, overclaims).

Before tagging, confirm locally:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
python run_checks.py          # 9 passed, 0 failed, 9 total
python release_gate.py        # RESULT: PASS
python generate_paper9_dag.py # regenerates theorems.json + interactive_dag.html (should be a no-op diff)
```

Then, on a machine with GitHub credentials:

```bash
git add -A
git commit -m "Paper 9 v3.7.1 repository hotfix: self-contained 9-check witness layer, typed closure DAG, metadata reconciliation, release gate + CI"
git tag v3.7.1
git push origin main --tags        # or force-push if the existing tree is being replaced
```

PDFs remain at manuscript versions v3.7 and TS v1.1; only code, ledger, DAG,
metadata, notebook, guides, and CI changed.
