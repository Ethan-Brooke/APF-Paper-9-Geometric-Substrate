"""apf/bank.py — Paper 9 v3.7.1 companion registry.

Release-local registry for the nine self-contained checks bundled with this
paper-companion repository. Mirrors the canonical apf.bank surface used by the
verifier: REGISTRY (OrderedDict), get_check(name), run_all(verbose=False).

This is NOT the canonical 3,918-entry engine bank. It registers exactly the
nine Paper 9 closure-spine witnesses. See apf/core.py and the theorem ledger
(theorems.json) for the full typed status of every Paper 9 node, including the
conditional, open, external, and model-certificate nodes that carry no local
executable witness.
"""
from collections import OrderedDict
import traceback

from apf import core as _core

# The nine bundled check names (single source of truth: core.BUNDLED_CHECKS).
_BUNDLED = [
    'check_T_finite_operational_basis_scope_contract',
    'check_T_finite_operational_basis',
    'check_T_finite_minimal_joint_realization_atom_cover',
    'check_T_held_to_record_typing',
    'check_T_gammaC_carrier_fork',
    'check_T_weight_one_reduction',
    'check_L_amount_graded_testedness_encoding_no_go',
    'check_T_fagt2_encoding_argmin_pressure_and_read_channel',
    'check_T_contention_law_granularity_occupancy_fork',
]
assert _BUNDLED == _core.BUNDLED_CHECKS, "bank/core bundled-set drift"

EXPECTED_CHECK_COUNT = 9


def _build_registry():
    reg = OrderedDict()
    for name in _BUNDLED:
        fn = getattr(_core, name, None)
        if fn is None:
            raise ImportError(f"bundled check missing from apf.core: {name}")
        reg[name] = fn
    return reg


REGISTRY = _build_registry()


def get_check(name):
    """Return the check function registered as `name`. Raises KeyError if missing."""
    if name not in REGISTRY:
        raise KeyError(f"Check '{name}' not found. Available: {sorted(REGISTRY.keys())}")
    return REGISTRY[name]


def run_all(verbose=False):
    """Run every registered check, returning a list of result dicts."""
    results = []
    for name, fn in REGISTRY.items():
        try:
            r = fn()
            if not isinstance(r, dict):
                r = {"name": name, "passed": bool(r), "key_result": str(r)}
            elif "passed" not in r:
                r["passed"] = True
            r.setdefault("name", name)
        except Exception as e:
            r = {
                "name": name,
                "passed": False,
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(),
            }
        if verbose:
            status = "PASS" if r.get("passed", True) else "FAIL"
            print(f"  {r['name']}: {status}")
            if r.get("key_result"):
                print(f"    {r['key_result']}")
        results.append(r)
    return results
