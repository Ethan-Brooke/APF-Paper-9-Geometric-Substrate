"""APF Paper 9 companion package — self-contained witness layer for
Paper 9 v3.7 (The Geometric Substrate as Cost Structure of Comparison
Continuations) and Technical Supplement v1.1.

Vendored from canonical APF-Engine v24.3.427 (commit 7ab898e, bank 3918).
The formal claims live in the manuscript and Technical Supplement; this package
executes a declared subset of finite witnesses and falsifier controls. Canonical
bank / cross-module introspection legs are frozen into apf/_release_fixtures.py
so the package is fully self-contained (no canonical-only apf.* import at runtime).

Full engine: https://doi.org/10.5281/zenodo.20041675  (Paper 9 concept DOI)
"""
__version__ = "3.7.1"
__engine_version__ = "24.3.427"
__engine_commit__ = "7ab898e"
__engine_bank_size__ = 3918
