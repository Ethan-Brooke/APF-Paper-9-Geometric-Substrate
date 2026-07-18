#!/usr/bin/env python3
"""Static and executable release gate for the Paper 9 companion repository.

Run from the repository root:

    python release_gate.py

Adapted to Contract A (nine bundled Paper 9 closure-spine witnesses).
This script is intentionally conservative. It catches the specific defects found
in the v3.7 GitHub release and should remain part of CI for v3.7.1+.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        fail(f"missing required file: {path}")
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def check_local_import_closure() -> None:
    path = ROOT / "apf/core.py"
    if not path.exists():
        return
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("apf."):
                    imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module == "apf":
                for alias in node.names:
                    imports.add(f"apf.{alias.name}")
            elif node.module and node.module.startswith("apf."):
                imports.add(node.module)

    for module in sorted(imports):
        rel = Path(*module.split("."))
        py = ROOT / f"{rel}.py"
        pkg = ROOT / rel / "__init__.py"
        if not py.exists() and not pkg.exists():
            fail(f"apf/core.py imports missing local module: {module}")


def check_subset_bank_api() -> None:
    core = read("apf/core.py")
    bank = read("apf/bank.py")
    if "._load()" in core and not re.search(r"^def _load\(", bank, re.M):
        fail("apf/core.py calls subset bank._load(), but apf/bank.py defines no _load()")


def check_runtime() -> None:
    proc = subprocess.run(
        [sys.executable, "run_checks.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    if proc.returncode != 0:
        fail(
            "run_checks.py returned nonzero exit code "
            f"{proc.returncode}\n--- output ---\n{output[-5000:]}"
        )
    if not re.search(r"\b9 passed,\s*0 failed,\s*9 total\b", output):
        fail("run_checks.py did not report exactly 9 passed, 0 failed, 9 total")


def check_dag() -> None:
    html = read("interactive_dag.html")
    if re.search(r"const\s+LINKS\s*=\s*\[\s*\]\s*;", html):
        fail("interactive_dag.html has zero dependency links")
    if re.search(r'"summary"\s*:\s*""', html):
        fail("interactive_dag.html contains blank theorem summaries")
    if "APF v6.8" in html:
        fail("interactive_dag.html is stamped with stale APF v6.8 metadata")


def check_release_prose() -> None:
    files = [
        "README.md",
        "START_HERE.md",
        "REVIEWERS_GUIDE.md",
        "ai_context/AGENTS.md",
        "APF_Reviewer_Walkthrough.ipynb",
        "apf/core.py",
        "apf/__init__.py",
        "run_checks.py",
        "repo_map.json",
    ]
    forbidden = {
        "v6.8": "stale Engine version v6.8",
        "v7.0": "stale Engine version v7.0",
        "v24.3.249": "stale Engine version v24.3.249",
        "355 `verify_all`": "stale 355-check count",
        "342 bank-registered": "stale 342-theorem count",
        "19 modules": "stale 19-module count",
        "25 modules": "unsupported 25-module count",
        "frozen 2026-05-04": "incorrect v24.3.427 freeze date",
        "APF-Codebase": "stale repository slug; use APF-Engine",
    }
    for filename in files:
        text = read(filename)
        for token, description in forbidden.items():
            if token in text:
                fail(f"{filename}: {description}: {token!r}")

    notebook = read("APF_Reviewer_Walkthrough.ipynb")
    if "self-contained verification** of every theorem" in notebook:
        fail("notebook overclaims verification of every Paper 9 theorem")
    if "5 theorems below are all [P]-derived" in notebook:
        fail("notebook launders P_structural/P_structural_instrument checks into [P]")

    guide = read("REVIEWERS_GUIDE.md")
    if "No paper-specific assumptions beyond the PLEC framework." in guide:
        fail("reviewer guide suppresses the manuscript's named paper-specific gates")
    if "multiple derivation paths" in guide:
        warn("reviewer guide claims multiple paths; verify against generated typed DAG")


def check_catalog_contract() -> None:
    text = read("theorems.json")
    if not text:
        return
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"theorems.json is invalid JSON: {exc}")
        return
    if data.get("bundled_in_this_repo") != 9:
        fail("theorems.json bundled count does not equal local registry count 9 (Contract A)")

    entries = data.get("entries", [])
    bundled = {
        e.get("name") for e in entries
        if e.get("bundled_in_this_repo")
    }
    bank = read("apf/bank.py")
    names = set(re.findall(r"'(check_[A-Za-z0-9_]+)'", bank))
    if bundled and bundled != names:
        fail(
            "theorems.json bundled set differs from apf/bank.py registry: "
            f"catalog-only={sorted(bundled - names)}, bank-only={sorted(names - bundled)}"
        )


def main() -> int:
    check_local_import_closure()
    check_subset_bank_api()
    check_runtime()
    check_dag()
    check_release_prose()
    check_catalog_contract()

    print("Paper 9 companion release gate")
    print("=" * 72)
    for message in WARNINGS:
        print(f"WARN: {message}")
    for message in ERRORS:
        print(f"FAIL: {message}")
    if ERRORS:
        print(f"\nRESULT: FAIL ({len(ERRORS)} error(s), {len(WARNINGS)} warning(s))")
        return 1
    print(f"\nRESULT: PASS (0 errors, {len(WARNINGS)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
