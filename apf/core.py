"""apf/core.py — Paper 9 v3.7.1 companion: aggregated executable-witness surface.

Re-exports the nine self-contained checks bundled for Paper 9 v3.7 and
Technical Supplement v1.1. Each check is vendored from the canonical
APF-Engine v24.3.427 (commit 7ab898e). No canonical-only apf.* module is
imported at runtime: bank/cross-module introspection is frozen into
apf/_release_fixtures.py.

These checks are FINITE WITNESSES and FALSIFIER CONTROLS. They do not
substitute for the symbolic proofs in the manuscript/supplement, and they do
not convert conditional or open gates into proved physical theorems.
"""
from apf.continuation_calculus import (
    check_T_finite_operational_basis_scope_contract,
    check_T_finite_operational_basis,
    check_T_finite_minimal_joint_realization_atom_cover,
)
from apf.aboutness_occupancy_section import (
    check_T_held_to_record_typing,
)
from apf.gamma_c_carrier_program import (
    check_T_gammaC_carrier_fork,
    check_T_weight_one_reduction,
)
from apf.amount_graded_testedness import (
    check_L_amount_graded_testedness_encoding_no_go,
    check_T_fagt2_encoding_argmin_pressure_and_read_channel,
    check_T_contention_law_granularity_occupancy_fork,
)

# The nine bundled checks, in Paper 9 closure-spine order (finite-basis triad,
# held-to-record typing, then the weak-field / encoding witnesses).
BUNDLED_CHECKS = [
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
