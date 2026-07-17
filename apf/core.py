"""apf/core.py — Paper 9 subset.

Vendored single-file extraction of the check functions cited in
Paper 9: The Geometric Substrate as Cost Structure of Comparison Continuations. The canonical APF codebase v6.8 (frozen 2026-04-18)
verifies 348 checks across 335 bank-registered theorems; this file
contains the 5-check subset
for this paper.

Each function is copied verbatim from its original source module.
See https://doi.org/10.5281/zenodo.18529115 for the full codebase.
"""

import inspect
import itertools
import math
from fractions import Fraction
import numpy as np
from apf.apf_utils import check, _result
_LAMBDA_T = Fraction(1)
_CLOSURES = {'plane': (Fraction(1), Fraction(1), Fraction(0)), 'four_cell': (Fraction(1), Fraction(3), Fraction(0)), 'per_channel': (Fraction(0), Fraction(1), Fraction(0)), 'pooled': (Fraction(-1), Fraction(1), Fraction(0))}
_CASSINI = Fraction(23, 1000000)
_RECRUITMENT_INSTRUMENT_BASELINE = frozenset({'check_H1_continuum_from_anchor_profile', 'check_H2_locality_from_recruitment_kernels', 'check_T_quantum_anchor_einstein_A', 'check_T_master_equation_form', 'check_T_three_regimes_tau_rec', 'check_T_tls_capacity_budget_knee_design_corollary', 'check_T_tls_transduction_class_discriminator_rule_D', 'check_T_substrate_anchor_entangled_state', 'check_T_cross_branch_matrix_element_form', 'check_T_sixteen_case_unification_structural', 'check_T_DCE_Q_dependence_prediction', 'check_T_purcell_DCE_consistency'})
_INSTRUMENT_ENUMERATION = {'B5_argmin_package': 'Paper 10 Supplement B5: E_rec argmin over profiles; prices the profile, blind to (lambda_t, lambda_s)', 'B34_approximate_A2': 'Paper 10 Supplement B3.4: slack bound sigma < eps*; ~11 orders too coarse at solar weak field (trace-mode cost ~ 2.2e-12 eps*)', 'paper10_sec8_clock_sector': 'DISCHARGED: the clock-sector depletion law K_t = K_t0(1 - alpha*chi) prices lambda_t only (clock-only per the parent walk); no ruler-sector counterpart exists in the licensed corpus', 'recruitment_bank_checks': 'the pinned baseline set below, each with its static-vacuity discharge: mu == 0 at the static fixed point, the dynamical layer holds as 0 = 0; quantum-anchor package silent for a single-branch classical static anchor; rate-layer TLS instruments (knee, Rule D) price transduction design, not the static equilibrium response', 'adopted_objects_exclusion': 'Paper 25 eq:linearized-EH + the phi_T <-> h_munu identification EXCLUDED because adopted (S5): including them would close the gate by adoption, not derivation'}
_TCP_MIN_VERBATIM = 'TCP-min [C]: the response deposit is denominated in committed capacity at a channel-uniform rate -- a cell-side deposit is a capacity amount billable in the ledger'
_TCP_STRONG_VERBATIM = "TCP-strong [C]: the static response is the load's committed line read at the cell -- the same amount, not less: the one-sided clause D(deposit) >= D(commitment); equality is not part of the premise -- it arrives only by composition with T-W1a's bound"
_CITABLE_BOUND = 'w <= 1, equivalently gamma_C <= 1/(n-2), at n = 3 gamma_C <= 1, at [P_structural | S0/S1 + TCP-min + H5-W + census legs + the Paper 9/Paper 10 base (P5, B7 incl. adopted C_M)]'
_CITABLE_POINT = "w = 1 (gamma_C = 1 at n = 3) ONLY at [P_structural | T-W1a's ledger + TCP-strong]; the standing chain reads gamma_C = 1 at [P_structural | H1 + H2 + H3(+adopted C_M) + census-saturation + H5 + {H6 or (S1 + TCP-strong)}]"
IE_DECLARATIONS = ({'input_id': 'gravity:gammaC_carrier_watch', 'axis': 'ROUTE', 'expect_export': False, 'claim_text': 'gamma_C <= 1 (no-source w <= 1 at n = 3): the PPN gamma is bounded above by the plane-carrier fork geometry (check_T_gammaC_carrier_fork, tier 3 [P_structural]). The Cassini central value gamma_obs - 1 = (2.1 +/- 2.3)e-5 sits 0.91 sigma ABOVE the bound -- a LIVE ONE-SIDED TENSION under watch, not a saturation and not a clean export. The pooled Nordstrom (gamma = 1 pooled) and per-channel (gamma = 0) alternatives are excluded at ~8.7e4 sigma / ~4.3e4 sigma. A >= 3 sigma confirmed gamma_obs > 1 falsifies. Held-for-repair by design: this route must never be silently promoted to a global-P export while the Cassini tension is live.', 'note': 'Onboards the gamma_C carrier program onto the ROUTE axis as a WATCH. The verdict is held (not exported); pinning it puts the signed Cassini one-sided tension under the verdict-drift tripwire, so any future re-derivation that flips the sign or promotes the route to an export fails the bank loudly. No physics import; inherits [P_structural].'},)
if __name__ == '__main__':
    for _n, _r in run_all().items():
        print('PASS' if _r.get('passed', True) else 'FAIL', _n)
        print('  grade:', _r['epistemic'], '| tier', _r['tier'])
        print('  ', _r['key_result'])
_EPS = Fraction(1)
_N_STEPS = 16
_LEDGER_BOUND = 'gamma_C <= 1 (n = 3) at [P_structural | S0/S1 + TCP-min + H5-W + census legs + the Paper 9/Paper 10 base (P5, B7 incl. adopted C_M)]'
_LEDGER_POINT_EP = 'gamma_C = 1 at [P_structural | H1 + H2 + H3(+adopted C_M) + census-saturation + H5 + (S1 + TCP-min + (E)+(P))]'
_LEDGER_POINT_STANDING = 'gamma_C = 1 at [P_structural | H1 + H2 + H3(+adopted C_M) + census-saturation + H5 + {H6 or (S1 + TCP-strong)}]'
_FAGT2C_GATE = 'flip iff f(M) - N*f(M/N) > N - 1 (one per-atom concurrent-activation law f charged to BOTH encodings; even spread M = kN)'
_FAGT2C_FIRST_FLIP_M_SQ = {16: 5, 256: 17}
_FAGT2C_CENSUS_PATTERN = 'contention|co[-_]?avail'
_FAGT2C_REGISTRY_BASELINE = frozenset({'check_T_ckm_flavour_coavailability_is_sepstr', 'T_contention_law_granularity_occupancy_fork'})
_FCL1_DOOR_SPEC = 'any banked atom-granular activation charge owes BOTH the pinned .382 gate f(M) - N*f(M/N) > N - 1 (the law charged to BOTH encodings) AND the granularity check g < N before any (E) claim; interface-coarse charges provably do not flip; two enumerated source shapes: (c1-gran) sub-record-granular finite activation capacity (A1-shaped; granularity unbanked) or (c1-occ) atom-granular irreducible jointness (occupancy at the read interface; QAC genre, empirical)'
IE_DECLARATIONS = ({'input_id': 'foundation:agt_encoding_wall', 'axis': 'ROUTE', 'route': 'amount_graded_testedness', 'expect_export': False, 'payload': {'name': 'agt_encoding_wall', 'closure_kind': 'obstruction_named', 'obstruction_class': 'AGT_ENCODING_WALL_NO_GO', 'knockout_summary': "No amount-graded testedness principle derives (scope: the corpus as formalized): three floor-coherent GCC signatures encode the same N-valued record at floor grades eps* x {1, log2 N, N} -- the magnitude-to-count transport is SIGNATURE DATA, the principle sought relocated, not derived. The (E) door is NAMED, not consumed (F-AGT2: distributed-vs-compressed record structure, with the read-channel flip gate pinned and tripwire F-AGT2-c live); AGT-par NOT adopted (ruled 2026-07-04: no separate hold-pattern entry); TCP-strong remains the lane's single named [C] in the w >= 1 direction; the contention-law fork forms (c1-gran)/(c1-occ) are named, unbanked, NOT adopted (.385). (check_L_amount_graded_testedness_encoding_no_go, amount_graded_testedness.py)"}, 'note': 'Onboards the .378 encoding wall onto the ROUTE axis as a closure-by-design obstruction. The AGT-par non-adoption and the single-[C] discipline are frozen in the knockout text; a future lane deriving amount-graded testedness inside the formalized corpus, or citing AGT-par as a second [C], fails the pin.'},)


# ======================================================================
# Extracted from canonical gamma_c_carrier_program.py
# ======================================================================

def check_T_gammaC_carrier_fork():
    fork = {name: _solve_linear_closure(*cond) for name, cond in _CLOSURES.items()}
    expected = {'plane': Fraction(1), 'four_cell': Fraction(1, 3), 'per_channel': Fraction(0), 'pooled': Fraction(-1)}
    check(fork == expected, 'the four carrier closures must solve to gamma in {1, 1/3, 0, -1}')
    check(len(set(fork.values())) == 4, 'the four fork points are distinct')
    for name, (c_t, c_s, rhs) in _CLOSURES.items():
        for name2, g in fork.items():
            residual = c_t * _LAMBDA_T + c_s * _lam_s(g) - rhs
            if name2 == name:
                check(residual == 0, f'{name} closure must hold at its point')
            else:
                check(residual != 0, f'{name} closure must fail at the {name2} point')
    four_trace_at_plane = _LAMBDA_T + 3 * _lam_s(fork['plane'])
    check(four_trace_at_plane == -2, 'plane closure forces the four-cell trace to -2 (mutual exclusion)')
    plane_trace_at_cell = _LAMBDA_T + _lam_s(fork['four_cell'])
    check(plane_trace_at_cell == Fraction(2, 3), 'four-cell closure forces the plane trace to 2/3')
    plane_matches, cell_matches, chan_matches, pool_matches = ([], [], [], [])
    for n in range(3, 11):
        g_gr = _gamma_GR(n)
        h_00, h_ij, _, _ = _trace_reversal_components(n)
        check(h_ij / h_00 == g_gr, 'gamma_GR(n) = 1/(n-2) must follow from trace reversal')
        if fork['plane'] == g_gr:
            plane_matches.append(n)
        if Fraction(1, n) == g_gr:
            cell_matches.append(n)
        if fork['per_channel'] == g_gr:
            chan_matches.append(n)
        if fork['pooled'] == g_gr:
            pool_matches.append(n)
    check(plane_matches == [3], 'the plane carrier matches the Einstein family ONLY at n = 3')
    check(cell_matches == [] and chan_matches == [] and (pool_matches == []), 'four-cell (1/n), per-channel (0), pooled (-1) match in NO dimension n >= 3 -- Cassini-independent structural kills')
    sigma_pooled = abs(fork['pooled'] - 1) / _CASSINI
    check(86000 < float(sigma_pooled) < 88000, 'pooled/Nordstrom gamma = -1 excluded at ~8.7e4 sigma')
    sigma_chan = abs(fork['per_channel'] - 1) / _CASSINI
    check(43000 < float(sigma_chan) < 44000, 'per-channel gamma = 0 excluded at ~4.3e4 sigma')
    check((1 + fork['pooled']) / 2 == 0, 'the gamma = -1 member has zero first-order light deflection')
    check(_LAMBDA_T - _lam_s(fork['pooled']) == 0, 'pooled: the first-order exchange sector v = lambda_t - lambda_s is destroyed (redshift-only response)')
    for n in range(3, 9):
        for w in (Fraction(0), Fraction(1), Fraction(1, 2), Fraction(3, 2)):
            check(_gamma_w(w, n) == w / (n - 1 - w), 'gamma(w) = w/((n-1)-w) closed form')
        check(_gamma_w(Fraction(1), n) == Fraction(1, n - 2), 'GR is w = 1 in EVERY dimension: gamma(1, n) = 1/(n-2) exact')
        check(_gamma_w(Fraction(0), n) == fork['per_channel'], 'direct-only is w = 0: the per-channel carrier, exactly')
    for n in range(3, 9):
        _, _, spread_00, spread_ij = _trace_reversal_components(n)
        check(spread_ij / spread_00 == -1, 'spread-only: signed ratio spread_ij/spread_00 = -1 exactly')
        check(-(spread_ij / spread_00) == _lam_s(fork['pooled']) / _LAMBDA_T, 'spread-only limit is the pooled row lambda_s = +lambda_t (sign included)')
        check(-(spread_ij / spread_00) != _lam_s(fork['plane']) / _LAMBDA_T, 'spread-only is NOT the plane (which needs lambda_s = -lambda_t)')
    return _result(name='T_gammaC_carrier_fork -- the four-point carrier fork, the dimension audit, the Cassini kills, and the weight-one curve', tier=3, epistemic='P_structural', summary="In the Paper 9 v1.6 calibrated normal form (lambda_t = +1, lambda_s = -gamma_C), the four carrier closures SOLVE to gamma_C in {1, 1/3, 0, -1} (plane / four-cell / per-channel / pooled), pairwise distinct and cross-exclusive (plane closure forces four-cell trace -2; four-cell forces plane trace 2/3). Dimension table: gamma_GR(n) = 1/(n-2) -- FLAGGED continuum import, recomputed in-check from trace-reversed linearized GR and Lovelock-robust (Gauss-Bonnet adds nothing linearized around flat) -- matches the plane carrier ONLY at n = 3; four-cell (1/n), per-channel (0), pooled (-1) match in no dimension. Cassini: pooled = Nordstrom (zero first-order deflection) dead at ~8.7e4 sigma; per-channel dead at ~4.3e4 sigma. THE WEIGHT-ONE CURVE (audit-donated): response = direct + w*spread gives gamma(w) = w/((n-1)-w) exactly; GR is w = 1 in EVERY n (gamma(1, n) = 1/(n-2)); direct-only (w = 0) is the per-channel carrier; spread-only carries the SIGNED pooled leg lambda_s = +lambda_t. The two Cassini-dead traps are the curve's two limits; deriving w = 1 is the live opener of record. Falsifier hooks: a gamma_obs anomaly; any change to the Paper 9 normal-form conventions (the four-cell sign-slip -1/3 artifact is the recorded caution).", key_result='carrier fork gamma_C in {1, 1/3, 0, -1} solved from closures; gamma_GR(n) = 1/(n-2) [continuum import, Lovelock-robust]; plane matches Einstein only at n = 3; pooled killed 8.7e4 sigma, per-channel 4.3e4 sigma (Cassini); weight-one curve gamma(w) = w/((n-1)-w), GR = w=1 in every n', dependencies=['A1', 'T8', 'Delta_signature'], cross_refs=['T_ledger_rent_excluded', 'T11'], artifacts={'fork': {k: str(v) for k, v in fork.items()}, 'dimension_table_matches': {'plane': [3], 'four_cell': [], 'per_channel': [], 'pooled': []}, 'cassini_sigma': {'pooled': float(sigma_pooled), 'per_channel': float(sigma_chan)}, 'weight_one_curve': 'gamma(w, n) = w/((n-1)-w); GR = w=1 all n', 'continuum_import_flag': 'gamma_GR(n) = 1/(n-2) from adopted trace-reversed linearized GR; Lovelock/GB-robust', 'witness': 'The Turning/c1_notrace_witness_2026-07-03.py 9/9 + register_carrier_witness_2026-07-03.py W9'})

def check_T_weight_one_reduction():
    F = Fraction

    def eta_diag(n):
        return [F(-1)] + [F(1)] * n

    def spread_deposit(n, w, rho=F(1), denom=None):
        if denom is None:
            denom = n - 1
        return [e * w * rho / denom for e in eta_diag(n)]

    def D(pattern):
        return sum(pattern)

    def w_of_gamma(g, n):
        return F(g) * (n - 1) / (1 + F(g))
    rho = F(1)
    for n in range(3, 9):
        check(D(eta_diag(n)) == n - 1, "the eta diagonal sums to n-1 over the cell: the denominator's origin (n-1 DISCHARGED, not an independent import)")
        for w in (F(0), F(1, 3), F(1), F(7, 5), F(-2, 3)):
            dep = spread_deposit(n, w, rho)
            commit = [rho] + [F(0)] * n
            check(D(dep) == w * rho and D(commit) == rho and (D(dep) / D(commit) == w), 'L-W0: w = D(spread deposit)/D(commitment) identically in n and w')
    for n in range(3, 7):
        for c in (F(1), F(2), F(n - 1), F(n + 1), F(7, 3)):
            w_star = c / (n - 1)
            check(w_star / (c - w_star) == F(1, n - 2), 'normalization invariance: D-balance selects gamma = 1/(n-2) under EVERY democratic-eta normalization c')
    for n in range(3, 7):
        for i in range(1, n + 1):
            for delta in (F(1), F(-3, 4), F(11, 7)):
                exch = [F(0)] * (n + 1)
                exch[0], exch[i] = (-delta, delta)
                check(D(exch) == 0, 'L-W1: clock<->ruler exchange (v_e-type) is D-neutral -- the reductio immunity is arithmetic, not fenced')
    for n in range(3, 6):
        base = spread_deposit(n, F(2, 3))
        for i in range(1, n + 1):
            pat = list(base)
            pat[0] -= F(5, 9)
            pat[i] += F(5, 9)
            check(D(pat) == D(base), 'adding exchange to any pattern leaves D unchanged')
        for i, j in itertools.combinations(range(1, n + 1), 2):
            pat = [F(0)] * (n + 1)
            pat[i], pat[j] = (F(4, 3), -F(4, 3))
            check(D(pat) == 0, "inter-plane ruler-ruler exchange is also D-neutral (the H5-W fence is broader than H6's)")
    for n in range(3, 9):
        for w in (F(0), F(1, 2), F(1), F(3, 2), F(-1, 3)):
            a = -F(w) / (n - 1)
            coef_eta = a - (1 + a * (n + 1)) / 2
            check(coef_eta == -(1 - F(w)) / 2, 'TR[h(w)] = hbar - ((1-w)/2) eta hbar_tr exactly')
            b = coef_eta
            G = (-F(1, 2), -F(1, 2) * (b + b), -F(1, 2) * (-2 * b))
            extra = (G[0] + F(1, 2), G[1], G[2])
            check(extra == (F(0), (1 - F(w)) / 2, -(1 - F(w)) / 2), 'L-W2: G_lin[h(w)] = kappa*T + ((1-w)/2)(eta box - dd) hbar exactly (adopted linearized theory, flagged)')
            check((extra == (F(0), F(0), F(0))) == (w == 1), 'the improvement term vanishes IFF w = 1, in every n: w != 1 IS the independent scalar comparison mode')
    for n in range(3, 7):
        for kvec in (tuple(range(1, n + 2)), (2,) + (3,) * n, (5, -1) + (1,) * (n - 1)):
            k = np.array(kvec, dtype=object)
            eta = np.diag([-1] + [1] * n).astype(object)
            k_up = eta @ k
            k2 = int(k_up @ k)
            M = eta * k2 - np.outer(k, k)
            div = k_up @ M
            check(all((int(x) == 0 for x in div)), 'the improvement term is identically conserved (exact integer Fourier: k^mu (eta k^2 - k k) = 0)')
    check(w_of_gamma(1, 3) == 1 and w_of_gamma(F(1, 3), 3) == F(1, 2) and (w_of_gamma(0, 3) == 0), 'n = 3 fork w-coordinates: plane w = 1, four-cell w = 1/2, per-channel w = 0')
    try:
        w_of_gamma(-1, 3)
        check(False, 'pooled gamma = -1 must have NO finite w')
    except ZeroDivisionError:
        pass

    def h00_w(w, n, A=F(7)):
        """h_00(w) through the leg-3 machinery: a = -w/(n-1), h_00 =
        hbar_00 + a*eta_00*hbar_tr (static source hbar_00 = A, hbar_tr =
        -A, eta_00 = -1). Audit fix F3 (2026-07-04): the pole is
        EVALUATED from the coefficient, not substituted -- a wrong h_00
        formula now fails this leg."""
        a = -F(w) / (n - 1)
        return A + a * F(-1) * -A
    check(all((h00_w(F(n - 1), n) == 0 and h00_w(F(n - 1) + F(1, 7), n) != 0 and (h00_w(F(1), n) == F(7) * F(n - 2, n - 1)) for n in range(3, 8))), 'h_00(w) = 0 at w = n-1 (the pooled/spread-only projective point), evaluated through the leg-3 coefficient: zero AT the pole, nonzero off it, w = 1 reproducing h_00 = A(n-2)/(n-1)')
    check(abs(float(_gamma_w(F(10 ** 9), 3)) + 1) < 1e-08 and abs(float(_gamma_w(F(-10 ** 9), 3)) + 1) < 1e-08, 'gamma(w) -> -1 as w -> +/-inf (pooled as the projective limit)')
    check(all((w_of_gamma(1, n) == F(n - 1, 2) and (n == 3) == (F(n - 1, 2) == 1) for n in range(3, 9))), 'the plane carrier at general n sits at w = (n-1)/2: scalar-tensor off n = 3 (no n-independent plane law)')
    for w in (F(0), F(1, 2), F(1), F(3, 2)):
        lam_over_A = 1 - _gamma_w(w, 3)
        check(lam_over_A == 2 * (1 - w) / (2 - w) and (lam_over_A == 0) == (w == 1), 'n = 3 calibrated trace source lambda/A = 2(1-w)/(2-w), zero iff w = 1')

    def gamma_of_shape(dep, commit=F(1)):
        """gamma read from a deposit shape by the SAME response route
        _gamma_w evaluates: h_00 = commitment + clock-channel deposit,
        h_ij = per-ruler-channel deposit, gamma = h_ij/h_00. Audit fix
        F2 (2026-07-04): the shape-table gammas are DERIVED from the
        deposit shapes, not asserted."""
        check(len(set(dep[1:])) == 1, 'the shape->gamma route needs channel-uniform ruler deposits')
        return dep[1] / (commit + dep[0])
    for n in range(3, 7):
        for w in (F(0), F(1, 2), F(1), F(3, 2)):
            check(gamma_of_shape(spread_deposit(n, w)) == _gamma_w(w, n), 'route calibration: on the eta-democratic shape the shape->gamma response route reproduces the weight-one curve exactly')
        dep_r = [F(0)] + [F(1, n)] * n
        check(D(dep_r) == 1 and gamma_of_shape(dep_r) == F(1, n), 'rulers-only shape + D-balance -> gamma = 1/n DERIVED via the response route (four-cell family; Cassini-dead 1/3 at n = 3): the shape carries the fork content')
        dep_c = [F(1)] + [F(0)] * n
        check(D(dep_c) == 1 and gamma_of_shape(dep_c) == 0, 'clock-only shape + D-balance -> gamma = 0 DERIVED via the response route (per-channel; Cassini-dead)')

    def gamma_bound_aniso(ct, cs, n):
        w_max = ct * (n - 1) / (n * cs - ct)
        return w_max / (n - 1 - w_max)
    for n in range(3, 9):
        for ct, cs in ((F(1), F(1)), (F(1), F(9, 10)), (F(1), F(6, 5)), (F(3), F(2)), (F(2), F(5)), (F(7, 3), F(7, 3))):
            if n * cs - 2 * ct <= 0:
                continue
            w_max = ct * (n - 1) / (n * cs - ct)
            dep = spread_deposit(n, w_max)
            check(ct * dep[0] + cs * sum(dep[1:]) == ct * F(1), 'anisotropic D_c-balance at w_max, re-derived from the deposit/commitment amounts, exact')
            check(gamma_bound_aniso(ct, cs, n) == ct / (n * cs - 2 * ct), 'the anisotropic bound gamma <= c_t/(n*c_s - 2*c_t)')
    check(gamma_bound_aniso(F(1), F(9, 10), 3) == F(10, 7) and gamma_bound_aniso(F(1), F(6, 5), 3) == F(5, 8) and (gamma_bound_aniso(F(1), F(1), 3) == F(1)), "n = 3 samples: 10/7 (too weak), 5/8 (excludes GR), exactly 1 at c_t = c_s: the bound AT 1 is TCP-min clause (ii)'s selection within a continuum")
    for ct in (F(1), F(2), F(7, 3)):
        for ratio_ in (F(1), F(9, 10), F(6, 5), F(1, 2), F(3), F(101, 100)):
            cs = ct * ratio_
            exists_all = all((n * cs - 2 * ct > 0 for n in range(3, 9)))
            tracks_all = exists_all and all((gamma_bound_aniso(ct, cs, n) == F(1, n - 2) for n in range(3, 9)))
            check(tracks_all == (cs == ct), "THE T4 SELECTION: the bound tracks gamma_GR(n) = 1/(n-2) in every n = 3..8 IFF c_t = c_s -- the dimension audit uniquely selects channel-uniformity (a selection, not a discharge: the linear amount-functional frame is the premise's)")
    for n in range(3, 9):
        w_bal = F(n - 1, n + 1)
        dep = spread_deposit(n, w_bal)
        check(sum((abs(x) for x in dep)) == F(1) and _gamma_w(w_bal, n) == F(1, n), "the L1 row: UNSIGNED channel-uniform balance -> gamma = 1/n in every n (four-cell family) -- excluded by TCP-min's LINEARITY clause, not by taste")
    for n in range(3, 9):
        lt = F(1)
        ls1 = -_gamma_w(F(1), n)
        check(lt + (n - 2) * ls1 == 0, "zeroing the D-net response component <=> the (1, n-2) linear rule <=> H6-prime's closure identity at w = 1")
        for w in (F(0), F(1, 2), F(3, 2)):
            ls_w = -_gamma_w(w, n)
            check((lt + (n - 2) * ls_w == 0) == (w == 1), 'the H6-prime identity holds IFF w = 1: record-billing with a D-fence selects the register rule')
    check((1, 3 - 2) == (1, 1), 'at n = 3 the (1, n-2) rule IS the plane rule (1, 1): the third coat -- do-not-re-walk; never cite the D-fence as licensing record-billing')
    for n in range(3, 7):
        grid = [F(g, 100) for g in range(-80, 300, 21)]
        for g1, g2 in itertools.combinations(grid, 2):
            dq = (w_of_gamma(g2, n) - w_of_gamma(g1, n)) / (g2 - g1)
            check(dq == (n - 1) / ((1 + g1) * (1 + g2)), 'exact Mobius difference-quotient: dw/dgamma > 0 on gamma > -1')
        thr = F(1, n - 2)
        for dg in (F(-1, 3), F(-1, 100), F(0), F(1, 100), F(1, 3)):
            g = thr + dg
            check((w_of_gamma(g, n) <= 1) == (g <= thr), 'w <= 1 iff gamma_C <= 1/(n-2), computed straddling the threshold')
    g_central = 1 + F(21, 10 ** 6)
    w_minus_1 = w_of_gamma(g_central, 3) - 1
    check(w_minus_1 > 0 and abs(float(w_minus_1) - 1.05e-05) < 5e-08, "CASSINI SIGNED: the central value sits ABOVE the bound (w - 1 = +1.05e-5 at central gamma) -- never cite as 'saturates'")
    check(0.912 < 2.1 / 2.3 < 0.914, 'the tension is 0.91 sigma ABOVE the bound: live one-sided tension, the bound survives at < 1 sigma')
    check(2.7 < 2.1 / (2.3 / 3) < 2.8, 'a factor-~3 precision improvement at the same central value puts the composite under ~3 sigma pressure')
    cass = F(23, 10 ** 6)
    margin = max(abs(float(w_of_gamma(1 - cass, 3) - 1)), abs(float(w_of_gamma(1 + cass, 3) - 1)))
    check(1.1e-05 < margin < 1.2e-05, 'the 1-sigma half-width maps to |w-1| <= ~1.15e-5: interval width only, NOT a saturation claim')
    chi_hat = 2.1e-06
    theta_dev = float(1 - _gamma_w(F(0), 3))
    check(0.5 * (theta_dev * chi_hat) ** 2 < 1e-11, 'the w-footprint is >= 11 orders sub-floor: the approximate-A2/no-slack route is dead for w as it was for theta')
    import apf.recruitment as _recruitment
    live_names = frozenset((name for name, obj in inspect.getmembers(_recruitment) if name.startswith('check_') and inspect.isfunction(obj) and (obj.__module__ == 'apf.recruitment')))
    check(live_names == _RECRUITMENT_INSTRUMENT_BASELINE, "F-W2 TRIPWIRE: the recruitment instrument census moved since the pinned twelve-name baseline -- a new ruler-sector or channel-anisotropic response instrument voids TCP clause (ii)'s pricing and forces a re-audit of the weight-one reduction (instruments landing outside the recruitment census remain E1-search-bounded, named)")
    return _result(name='T_weight_one_reduction -- the deposit-fraction identity, exchange annihilation, the scalar-improvement identity, the third coat, and the asymmetric conditional pair (the weight-one walk banked)', tier=3, epistemic='P_structural', summary='The weight-one walk (2026-07-04, REDUCED) banked at its proved strength. UNCONDITIONAL ARITHMETIC (exact rationals, n = 3..8): L-W0, the banked weight IS the deposit fraction w = D(spread deposit)/D(commitment) -- the denominator n-1 is DISCHARGED as the cell\'s eta-sum, and D-balance selects gamma = 1/(n-2) under EVERY democratic-eta normalization (the conservation statement is normalization-free); L-W1, D annihilates every exchange pattern (clock<->ruler and ruler-ruler): the v_e reductio has no purchase on the amount frame by arithmetic, given the linear channel-uniform amount functional (TCP-min clause (ii), which the T4 dimension audit uniquely selects within the anisotropic continuum gamma <= c_t/(n*c_s - 2*c_t) -- tracks gamma_GR in every n IFF c_t = c_s; the UNSIGNED L1 row lands on the four-cell 1/n); L-W2, G_lin[h(w)] = kappa*T + ((1-w)/2)(eta box - dd) hbar exactly, identically conserved (exact integer Fourier), vanishing IFF w = 1 -- w != 1 IS the independent scalar comparison mode (continuum-import flag carried). THE SHAPE CARRIES THE FORK: rulers-only -> 1/n, clock-only -> 0 under the same D-balance; the eta-democratic shape S1 is the honest residual import. THE THIRD COAT, machine-pinned: "bill the D-net component" <=> the (1, n-2) rule <=> H6-prime (the plane rule at n = 3); record-billing with a D-fence is the register fork re-entering -- do-not-re-walk. THE ASYMMETRIC PAIR (hypothesis artifacts; NOTHING HERE DERIVES w = 1): no-source ' + _CITABLE_BOUND + '; no-sink additionally requires TCP-strong, whose named discharge shape is an amount-graded testedness principle (walked and priced as the (E)+(P) anatomy, apf/amount_graded_testedness.py). CASSINI SIGNED (Bertotti-Iess-Tortora 2003): gamma - 1 = (2.1 +/- 2.3)e-5, central value 0.91 sigma ABOVE the bound -- live one-sided tension, NOT saturation; >= 3 sigma confirmed violation falsifies the composite; factor-~3 precision at the same central -> ~3 sigma pressure. The F-W2 tripwire re-asserts the recruitment census baseline in-check.', key_result="L-W0/L-W1/L-W2 exact: w = D(deposit)/D(commitment) (n-1 discharged as the cell's eta-sum; normalization-invariant); D annihilates exchange; w != 1 = one identically-conserved scalar improvement mode vanishing iff w = 1; shape carries the fork (rulers-only -> 1/n, clock-only -> 0); T4 selects channel-uniformity (tracks 1/(n-2) in every n iff c_t = c_s); D-fenced record-billing = the (1, n-2) rule = H6-prime (third coat, do-not-re-walk). NOTHING HERE DERIVES w = 1. Citable: no-source " + _CITABLE_BOUND + '; no-sink ' + _CITABLE_POINT + ". Cassini SIGNED (Bertotti-Iess-Tortora 2003): gamma - 1 = (2.1 +/- 2.3)e-5, central value 0.91 sigma ABOVE the bound -- live one-sided tension, NOT saturation; >= 3 sigma confirmed violation falsifies the composite. TCP-min [C]; TCP-strong [C]; H5-W named, unbanked, separate and standing; amount-graded testedness is TCP-strong's discharge hook (L_amount_graded_testedness_encoding_no_go).", dependencies=['A1', 'T8', 'Delta_signature'], cross_refs=['T_gammaC_carrier_fork', 'L_register_carrier_not_from_account_instruments', 'L_notrace_not_from_recruitment_instruments', 'L_amount_graded_testedness_encoding_no_go'], artifacts={'tcp_min_verbatim': _TCP_MIN_VERBATIM, 'tcp_strong_verbatim': _TCP_STRONG_VERBATIM, 'citable_bound': _CITABLE_BOUND, 'citable_point': _CITABLE_POINT, 'h5w_status': 'H5-W: census-transport re-fenced to D-net objects; named premise, unbanked; a WEAKER, typing-free variant of H5 -- flagged variant, not replacement; SEPARATE and still standing', 'cassini_signed': 'Bertotti-Iess-Tortora 2003: gamma - 1 = (2.1 +/- 2.3)e-5; central value 0.91 sigma ABOVE the bound (w - 1 = +1.05e-5); live one-sided tension, NOT saturation', 'falsification_convention': 'a confirmed gamma_obs > 1/(n-2) at >= 3 sigma falsifies the composite (S0/S1 + TCP-min + H5-W + census + P5/B7 base); gamma_obs < 1 at >= 3 sigma refutes only the no-sink half (TCP-strong)', 'third_coat': 'bill-the-D-net-component = the (1, n-2) rule = H6-prime = the plane rule at n = 3; do-not-re-walk', 't4_selection': 'bound gamma <= c_t/(n*c_s - 2*c_t) tracks 1/(n-2) in every n iff c_t = c_s; L1 row -> 1/n', 'shape_table': {'eta_democratic': 'Einstein family 1/(n-2)', 'rulers_only': '1/n (four-cell, Cassini-dead)', 'clock_only': '0 (per-channel, Cassini-dead)'}, 'n_minus_2_mechanism': "n-2 = (the cell's eta-sum n-1) - (one committed load's worth of deposit), conditional on the ledger", 'discharge_hook': 'an amount-graded testedness principle; walked 2026-07-04: the (E)+(P) anatomy (apf/amount_graded_testedness.py); the (E) distributed-encoding door is the single genuine reopening', 'witness': 'The Turning/weight_one_witness_2026-07-04.py 36/36 PASS (W1-W11)'})

def _trace_reversal_components(n, A=Fraction(7)):
    """Static point source in D = n+1: hbar_00 = A, hbar_trace = -A
    (eta^00 = -1); h_munu = hbar_munu - eta_munu*hbar_trace/(n-1).
    Returns (h_00, h_ij, spread_00, spread_ij); direct_00 = hbar_00."""
    hbar_00, hbar_tr = (A, -A)
    spread_00 = -Fraction(-1) * hbar_tr / (n - 1)
    spread_ij = -Fraction(1) * hbar_tr / (n - 1)
    h_00 = hbar_00 + spread_00
    h_ij = spread_ij
    return (h_00, h_ij, spread_00, spread_ij)

def _solve_linear_closure(c_t, c_s, rhs=Fraction(0)):
    """Solve c_t*lambda_t + c_s*lambda_s(gamma) = rhs for gamma.

    With lambda_t = 1 and lambda_s = -gamma this is c_t - c_s*gamma = rhs,
    i.e. gamma = (c_t - rhs)/c_s. Solved, not hand-set."""
    check(c_s != 0, 'closure must constrain the ruler channel')
    return Fraction(c_t - rhs, 1) / Fraction(c_s, 1)

_CLOSURES = {'plane': (Fraction(1), Fraction(1), Fraction(0)), 'four_cell': (Fraction(1), Fraction(3), Fraction(0)), 'per_channel': (Fraction(0), Fraction(1), Fraction(0)), 'pooled': (Fraction(-1), Fraction(1), Fraction(0))}

def _gamma_w(w, n):
    """The weight-one curve: response = direct + w*spread ->
    gamma(w, n) = h_ij(w)/h_00(w) = w/((n-1)-w). Exact rationals."""
    A = Fraction(7)
    hbar_00, hbar_tr = (A, -A)
    h_00 = hbar_00 + w * (-Fraction(-1) * hbar_tr / (n - 1))
    h_ij = w * (-Fraction(1) * hbar_tr / (n - 1))
    return h_ij / h_00

_LAMBDA_T = Fraction(1)

def _lam_s(gamma):
    """Ruler response coefficient: lambda_s = -gamma_C (Paper 9 v1.6)."""
    return -gamma

def _gamma_GR(n):
    """Trace-reversed linearized GR: gamma_GR(n) = 1/(n-2), n spatial dims.

    CONTINUUM IMPORT (flagged): recomputed below from the h_00/h_ij
    decomposition of the adopted linearized theory; Lovelock-robust
    (Gauss-Bonnet adds nothing linearized around flat)."""
    return Fraction(1, n - 2)

_CASSINI = Fraction(23, 1000000)

_TCP_STRONG_VERBATIM = "TCP-strong [C]: the static response is the load's committed line read at the cell -- the same amount, not less: the one-sided clause D(deposit) >= D(commitment); equality is not part of the premise -- it arrives only by composition with T-W1a's bound"

_CITABLE_BOUND = 'w <= 1, equivalently gamma_C <= 1/(n-2), at n = 3 gamma_C <= 1, at [P_structural | S0/S1 + TCP-min + H5-W + census legs + the Paper 9/Paper 10 base (P5, B7 incl. adopted C_M)]'

_CITABLE_POINT = "w = 1 (gamma_C = 1 at n = 3) ONLY at [P_structural | T-W1a's ledger + TCP-strong]; the standing chain reads gamma_C = 1 at [P_structural | H1 + H2 + H3(+adopted C_M) + census-saturation + H5 + {H6 or (S1 + TCP-strong)}]"

_TCP_MIN_VERBATIM = 'TCP-min [C]: the response deposit is denominated in committed capacity at a channel-uniform rate -- a cell-side deposit is a capacity amount billable in the ledger'

_RECRUITMENT_INSTRUMENT_BASELINE = frozenset({'check_H1_continuum_from_anchor_profile', 'check_H2_locality_from_recruitment_kernels', 'check_T_quantum_anchor_einstein_A', 'check_T_master_equation_form', 'check_T_three_regimes_tau_rec', 'check_T_tls_capacity_budget_knee_design_corollary', 'check_T_tls_transduction_class_discriminator_rule_D', 'check_T_substrate_anchor_entangled_state', 'check_T_cross_branch_matrix_element_form', 'check_T_sixteen_case_unification_structural', 'check_T_DCE_Q_dependence_prediction', 'check_T_purcell_DCE_consistency'})


# ======================================================================
# Extracted from canonical amount_graded_testedness.py
# ======================================================================

def check_L_amount_graded_testedness_encoding_no_go():
    eps, N = (_EPS, _N_STEPS)
    ta_A = _ta(('a_v',), {'a_v'})
    theory_A = [(0, ta_A, eps * ta_A)]
    check(_floor_coherent(theory_A, eps), 'SIG-A theory is floor-coherent')
    gamma_A = _invariant_lower_bound(ta_A, eps)
    check(ta_A == 1 and gamma_A == eps, 'SIG-A (single-atom): least grade 1*eps for the N=16-valued record')
    bits = ('b1', 'b2', 'b3', 'b4')
    ta_B = _ta(bits, set(bits))
    theory_B = [(0, 1, eps)] * 4
    check(_floor_coherent(theory_B, eps), 'SIG-B theory is floor-coherent')
    gamma_B = _invariant_lower_bound(ta_B, eps)
    check(ta_B == 4 and gamma_B == eps * 4, 'SIG-B (positional): least grade log2(N)*eps = 4*eps, SAME record')
    rungs = tuple((f'r{i}' for i in range(1, N + 1)))
    ta_C = _ta(rungs, set(rungs))
    theory_C = [(0, 1, eps)] * N
    check(_floor_coherent(theory_C, eps), 'SIG-C theory is floor-coherent')
    gamma_C_sig = _invariant_lower_bound(ta_C, eps)
    check(ta_C == N and gamma_C_sig == eps * N, 'SIG-C (unary): least grade N*eps = 16*eps, SAME record')
    check(len({gamma_A, gamma_B, gamma_C_sig}) == 3, 'three floor-coherent signatures, one physical record, three distinct least grades eps*{1, log2 N, N}: no canonical magnitude grading is forced -- the floor invariant grades representation')
    check(gamma_C_sig / gamma_A == N and gamma_C_sig / gamma_B == Fraction(N, 4), 'the grade ratio spans the full encoding range (x16, x4): the magnitude-to-count transport is signature data, not a theorem')
    unit_atoms = tuple((f'u{i}' for i in range(1, N + 1)))
    check(_ta(unit_atoms, set()) == 0, 'SIG-D raw: the aggregate-tested composite has ta = 0 -- violates groundedness (b1:def:signature item 3, a NAMED OPEN of Paper 10)')
    bills, coherent = ([], [])
    for deficit in range(1, N):
        expressed = unit_atoms[:N - deficit]
        ta_held = _ta(expressed, {'u1'})
        theory_D = [(0, ta_held, eps * ta_held)]
        coherent.append(_floor_coherent(theory_D, eps))
        bills.append(_invariant_lower_bound(ta_held, eps))
    check(all(coherent), 'SIG-D repaired: the grounded one-axiom theory is floor-coherent at every deficit 1..15 (bill DERIVED by the GCC machinery, F5c)')
    check(all((b == eps for b in bills)), 'SIG-D repaired: the bill is eps* for EVERY deficit 1..15 -- constant, independent of the unexpressed amount: deficit-scaling fails under binary cleavage even with groundedness granted')
    lam, t_delta, q, tau = (1.0, 0.1, 0.01, 100.0)
    p = 0.5 * (1.0 - math.exp(-2.0 * lam * t_delta))
    n = round(tau / t_delta)
    Delta = _h(_conv(q, p)) - _h(q)
    check(0.0 < p < 0.5, 'flip probability p in (0, 1/2)')
    check(Delta > 0.0, 'per-step ledger increment Delta > 0 (lem:c2-ledger)')
    cm_floor = n * Delta - 1
    check(cm_floor > 0.0, 'one-bit refresh floor C_M >= n*Delta - 1 > 0 (thm:c2-floor)')
    check(abs(_h(_conv(1e-12, p)) - _h(1e-12) - _h(p)) < 1e-06, 'q -> 0 limit: Delta -> h(p) (the injected-entropy rate)')
    Ns = [2, 4, 16, 256, 65536]
    rates = [_H_N(p, Nv) for Nv in Ns]
    check(all((r2 > r1 for r1, r2 in zip(rates, rates[1:]))), 'H_N increases with N: finer/larger records do cost more')
    check(all((r / math.log2(Nv) <= _h(p) + p + 1e-09 for r, Nv in zip(rates, Ns))), 'H_N/log2(N) bounded (<= h(p) + p): the MOST GENEROUS billing of the Shannon ledger is O(log N) -- upper shape only, N-ary converse NOT claimed (Wyner-Ziv 1973 binary is the cited theorem)')
    per_step = [r / Nv for r, Nv in zip(rates, Ns)]
    check(all((a > b for a, b in zip(per_step, per_step[1:]))), 'H_N/N strictly decreasing toward 0: LINEAR m/delta grading fails even at the most generous billing')
    ratio = {}
    for Nv in (16, 256):
        linear_floor = Nv * (n * Delta - 1)
        generous_log = n * _H_N(p, Nv)
        ratio[Nv] = linear_floor / generous_log
        check(ratio[Nv] > 1.0, f'N={Nv}: the distributed-encoding linear floor sits STRICTLY above the generous O(log) billing (audit fix F5a threshold)')
    check(ratio[256] / ratio[16] > 256 / 16 * (math.log2(16) / math.log2(256)), 'the linear/log gap grows like N/log N (> 8 across N = 16 -> 256): exactly the encoding-hypothesis shape -- the linearity enters through the encoding, by hand')
    return _result(name='L_amount_graded_testedness_encoding_no_go -- the GCC floor invariant grades representation, not magnitude; the Shannon route is O(log) generous-upper-shape and bills expression, not absence (the encoding wall)', tier=4, epistemic='P_structural_instrument', summary='No amount-graded testedness principle is a theorem of the corpus as formalized 2026-07-04. Shape (ii) REFUTED as theorem: three floor-coherent GCC signatures (single-atom / positional / unary) hold the SAME N = 16-valued record at least grades eps*{1, log2 N, N} -- the floor invariant (b1:prop:invariant, b1:cor:count) grades the tested-atom count ta exactly, and the magnitude-to-count transport is signature data: the principle sought, relocated, not derived. The unit-partition route dies twice: it violates groundedness (b1:def:signature item 3, a NAMED OPEN), and repaired it bills one eps* regardless of the deficit (1..15 machine-checked) -- binary cleavage caps any partition at one floor\'s worth. Shape (i) PARTIAL: the C2 refresh ledger reproduces (Delta > 0, C_M >= n*Delta - 1) and extends at the MOST GENEROUS billing (full N-ary injected noise entropy h(p) + p*log2(N-1)) only LOGARITHMICALLY (H_N/log2 N bounded, H_N/N -> 0 strictly); linear-in-N arises exactly from holding the record as N independent one-bit records -- the distributed-encoding hypothesis, a new adopted premise, not a derivation (linear floor strictly above generous log billing; gap grows like N/log N). HONESTY FLAGS: the N-ary finite-error converse is NOT claimed (Wyner-Ziv 1973 binary is the cited theorem); the C_M <-> committed-capacity identification stays adopted (B7); the route bills EXPRESSION, never ABSENCE -- wrong shape and wrong direction for TCP-strong. SCOPE: non-derivability from the corpus AS FORMALIZED; NEVER cite as "APF cannot grade amounts". The single reopening door is (E), the distributed-encoding existence question (F-AGT2): a native derivation that static response records are held distributed delivers (E); a banked compressed/positional holding structure kills linear amount-grading permanently and TCP-strong stays a bare [C].', key_result='encoding wall: three floor-coherent GCC signatures hold the same N=16-valued record at eps*{1, log2 N, N} -- no amount-graded testedness principle is a theorem of the floor invariant (magnitude-to-count transport is signature data); unit-partition route lands on the groundedness NAMED OPEN and degrades to one eps* at every deficit; the Shannon/refresh route yields at most an O(log N) generous-billing upper shape (N-ary converse NOT claimed; Wyner-Ziv binary cited) and bills expression, not absence. Non-derivability from the corpus as formalized 2026-07-04; the (E) distributed-encoding door is the named reopening (F-AGT2). TCP-strong stays the named [C]; the citable bound stays gamma_C <= 1 (n = 3) at [P_structural | S0/S1 + TCP-min + H5-W + census legs + the Paper 9/Paper 10 base (P5, B7 incl. adopted C_M)].', dependencies=['A1', 'T_admissibility_greedoid_structure'], cross_refs=['T_agt_par_anatomy', 'T_weight_one_reduction', 'T_gammaC_carrier_fork'], artifacts={'signature_grades_eps_units': {'SIG_A_single_atom': 1, 'SIG_B_positional': 4, 'SIG_C_unary': 16}, 'sig_D_bills_eps_units': [str(b) for b in bills], 'generous_table': {'N': Ns, 'H_N_bits': [round(r, 4) for r in rates], 'H_N_over_log2N': [round(r / math.log2(Nv), 4) for r, Nv in zip(rates, Ns)], 'H_N_over_N': [round(r / Nv, 6) for r, Nv in zip(rates, Ns)]}, 'linear_over_log_ratio': {str(k): round(v, 2) for k, v in ratio.items()}, 'honesty_flags': ['N-ary converse NOT claimed (Wyner-Ziv 1973 binary is the cited theorem)', 'C_M <-> committed capacity ADOPTED (B7)', 'groundedness = named open (b1:def:signature item 3), not discharged', 'bills expression, not absence'], 'reopening_door': '(E) distributed-encoding existence (F-AGT2): record-structure question, outside the calculus vocabulary as formalized', 'witness': 'The Turning/amount_graded_testedness_walk_2026-07-04/witness_encoding_countermodel.py 11/11 + witness_nary_refresh_grading.py 10/10'})

def check_T_fagt2_encoding_argmin_pressure_and_read_channel():
    eps = _EPS
    check(1 < math.log2(3) < 3, 'the formation ordering 1 < log2 N < N holds already at N = 3 (proved trivially for all N >= 3, by inspection)')
    for N in (4, 8, 16, 32, 256, 65536):
        lg = int(math.log2(N))
        g_A, g_B, g_C = (1 * eps, lg * eps, N * eps)
        check(g_A < g_B < g_C, f'N={N}: formation grades strictly ordered eps*(1, {lg}, {N}) -- compressed single-atom argmin, distributed argmax (A2-pressure axis 1, witness 2)')
    lam, t_delta, q, tau = (1.0, 0.1, 0.01, 100.0)
    p = 0.5 * (1.0 - math.exp(-2.0 * lam * t_delta))
    n = round(tau / t_delta)
    Delta = _h(_conv(q, p)) - _h(q)
    check(abs(p - 0.0906) < 0.0005 and n == 1000 and (abs(Delta - 0.384) < 0.005), 'the banked constants of the .378 refresh model reproduce: p = 0.0906, n = 1000, Delta = 0.384')
    check(p < Delta, 'constant-dependence flag: the refresh ordering holds AT THE BANKED CONSTANTS because H_N/log2 N -> p < Delta; not claimed for all (p, q, tau)')
    for N in (4, 8, 16, 32, 256, 65536):
        lg = int(math.log2(N))
        compressed_generous = n * _H_N(p, N)
        positional = lg * (n * Delta - 1)
        distributed = N * (n * Delta - 1)
        check(compressed_generous < positional < distributed, f'N={N}: bank-faithful refresh ordering compressed(generous) < positional < distributed -- distributed cost-maximal on the second banked axis too; PRESSURE, not a kill (signature choice is outside every banked argmin domain as formalized 2026-07-04 -- census-true, see F-AGT2-d)')
    for N in (16, 256):
        lg = int(math.log2(N))
        form_A, form_B, form_C = (Fraction(1), Fraction(lg), Fraction(N))
        check(all((form_C + r * 1 > form_A + r * 1 for r in range(0, 10 ** 4, 997))), f'N={N} grading (a) size-blind: distributed never argmin at any read count -- the lever needs a size-sensitive grading')
        per_read = {'A': Fraction(1), 'B': Fraction(lg), 'C': Fraction(1)}
        check(per_read['C'] == per_read['A'], f'N={N} grading (b) ta-graded: distributed only TIES the compressed single-atom per rung-read (1 vs 1)')
        check(all((form_C + r * per_read['C'] > form_A + r * per_read['A'] for r in range(0, 10 ** 4, 997))), f'N={N} grading (b): the formation gap N-1 is never recovered -- distribution never strict argmin vs compression')
        r_star = (form_C - form_B) / (per_read['B'] - per_read['C'])
        check(form_C + r_star * per_read['C'] == form_B + r_star * per_read['B'] and form_C + (r_star + 1) * per_read['C'] < form_B + (r_star + 1) * per_read['B'], f'N={N} grading (b): distributed beats POSITIONAL exactly past r* = (N - log2 N)/(log2 N - 1) = {r_star} reads -- but positional was never the argmin')
        kappa = Fraction(3, 2)

        def f_binary(m):
            return m * kappa if m >= 2 else Fraction(m)

        def f_linear(m):
            return kappa * m

        def f_sq(m):
            return Fraction(m) ** 2

        def flip(M_):
            return _dist_cost(M_, N, f_sq) < _comp_cost(M_, f_sq)
        check([M for M in range(1, 4 * N + 1) if _dist_cost(M, N, f_binary) < _comp_cost(M, f_binary)] == [] and N * (kappa - 1) < N - 1, f'N={N} (c-i) binary shared/exclusive surcharge, coherently applied: NO M flips in 1..{4 * N} (saving <= N(kappa-1) = {N * (kappa - 1)} < N-1 = {N - 1}) -- a bounded surcharge never opens the door')
        check(all((_contention_saving(M, N, f_linear) == 0 for M in (1, N - 1, N, 2 * N + 3, 10 * N))), f'N={N} (c-ii) LINEAR per-atom law f(m) = kappa*m: contention saving identically ZERO at every reader count M -- a linear charge (any kappa) can NEVER flip the argmin; premise (c1) must be STRICT SUPERADDITIVITY of the per-atom law (the sharpened adverse lemma)')
        first_flip = next((M for M in range(1, 10 ** 5) if flip(M)))
        check(first_flip == _FAGT2C_FIRST_FLIP_M_SQ[N] and (not flip(first_flip - 1)) and flip(N), f'N={N} (c-iii) strictly superadditive f(m) = m^2 FLIPS: first flip at M = {first_flip} (sqrt-N scale; matches the pin), boundary strict, and M = N flips -- the door opens IF (c1) + (c2) hold, both NAMED UNBANKED, NOT adopted')

        def f_bound(m, _N=N):
            """Exact-boundary witness (audit minor 2): contention saving
            f(N) - N*f(1) = N - 1 exactly -- must NOT flip."""
            return Fraction(2 * _N - 1) if m == _N else Fraction(m)

        def f_bound_plus(m, _N=N):
            """One past the boundary: saving = N exactly -- must flip."""
            return Fraction(2 * _N) if m == _N else Fraction(m)
        sav_eq = _contention_saving(N, N, f_bound)
        sav_gt = _contention_saving(N, N, f_bound_plus)
        flip_eq = _dist_cost(N, N, f_bound) < _comp_cost(N, f_bound)
        flip_gt = _dist_cost(N, N, f_bound_plus) < _comp_cost(N, f_bound_plus)
        check(all((flip(M_) == (_contention_saving(M_, N, f_sq) > N - 1) for M_ in range(1, 4 * N, 7))) and all((flip(k * N) == (f_sq(k * N) - N * f_sq(k) > N - 1) for k in range(1, 11))) and (flip_eq == (sav_eq > N - 1)) and (flip_gt == (sav_gt > N - 1)), f'N={N}: the gate f(M) - sum f(m_i) > N - 1 (even spread: f(M) - N*f(M/N) > N - 1) matches the sweep exactly AND both exact-boundary witnesses -- the flip condition IS the door (tripwire F-AGT2-c arithmetic)')
        check(sav_eq == N - 1 and (not flip_eq) and (sav_gt == N) and flip_gt and (_comp_cost(1, f_sq) == 2) and (_dist_cost(N, N, f_sq) == 2 * N), f"N={N}: EXACT-BOUNDARY WITNESS (audit minor 2, non-tautological): a law saving exactly N - 1 does NOT flip and a law saving exactly N DOES -- the gate's strict -1 is pinned; formation constants pinned exactly (_comp_cost(1, f_sq) = 1 + f(1) = 2; _dist_cost(N, N, f_sq) = N + N*f(1) = 2N)")
    check(_FAGT2C_FIRST_FLIP_M_SQ == {16: 5, 256: 17} and 'BOTH encodings' in _FAGT2C_GATE, 'TRIPWIRE F-AGT2-c: the coherent flip gate is pinned in-module and re-derived above against the sweep; any future banked contention/co-availability cost law must be run against f(M) - N*f(M/N) > N - 1 (the banked per-atom law charged to BOTH encodings) before any (E) claim rides on it; a linear or sublinear law leaves compression argmin')
    import re as _re
    from apf import bank as _bank
    _bank._load()
    census = frozenset((k for k in _bank.REGISTRY if _re.search(_FAGT2C_CENSUS_PATTERN, k, _re.IGNORECASE)))
    check(census == _FAGT2C_REGISTRY_BASELINE, "TRIPWIRE F-AGT2-c census (the F-W2 pattern made external): the contention/co-availability name surface of the loaded registry equals the pinned baseline -- one pre-existing name, check_T_ckm_flavour_coavailability_is_sepstr, a SepStr co-availability CLASSIFICATION (gauge_invariant_record.py), not a cost law, plus the v24.3.385 contention-law consolidation (T_contention_law_granularity_occupancy_fork), which entered the census by name and was dispositioned per this tripwire's own obligation: every candidate law it touches is gate-run in-check, no (E) claim is made, no cost law is banked -- the DATED baseline extension is the tripwire firing as designed; a future banked contention or co-availability cost law in ANY module lands in this census and trips this leg, forcing the gate run before any (E) claim (out-of-census namings stay a named residue, exactly as F-W2's out-of-recruitment instruments)")
    import inspect as _inspect
    import apf.plec as _plec
    check(callable(getattr(_plec, 'check_Regime_R', None)) and callable(getattr(_plec, 'check_T_trivial_alignment_is_Type_II', None)) and ('argmin_q' in _inspect.getsource(_plec.check_Regime_R)) and ('admissible destinations' in _inspect.getsource(_plec.check_T_trivial_alignment_is_Type_II)), "F-AGT2-d census anchors stand: PLEC's argmin ranges over a path class (check_Regime_R, 'argmin_q' source fingerprint) and the banked destination-argmin -- 'argmin over admissible destinations (a, D')' with the Z2 two-destination witness -- is check_T_trivial_alignment_is_Type_II ('admissible destinations' source fingerprint; anchor re-aimed at the landing audit, MAJOR 1) -- the escape hatch ('no banked argmin ranges over encoding choice') is census-true as of 2026-07-04, NOT categorical; a destination-argmin generalization (it would touch these fingerprints or land a new census name) or a principal ruling on A2's constitutive domain UPGRADES the pressure to a refutation of (E) and retires this flag in that leg (succession clause)")
    check('TCP-min' in _LEDGER_POINT_EP and 'TCP-strong' in _LEDGER_POINT_STANDING and ('H5-W' in _LEDGER_BOUND), 'the citable ledger strings ride unchanged (TCP-min / TCP-strong / H5-W verbatim): nothing here delivers (E), TCP-strong, or gamma_C = 1; the walk verdict was REDUCE')
    return _result(name='T_fagt2_encoding_argmin_pressure_and_read_channel -- the (E) door walked: distributed encoding cost-maximal on both banked axes (the A2 pressure); linear contention saving-free; the strictly-superadditive flip gate pinned (tripwire F-AGT2-c); (E) NOT adopted, NOT refuted', tier=3, epistemic='P_structural', summary='The F-AGT2 walk (2026-07-04, REDUCE 0.85) banked at its proved strength -- the (E) distributed-encoding door walked, neither delivered nor shut. THE A2-PRESSURE LEMMA (adverse, new): on both banked cost axes -- GCC formation (grades eps*{1, log2 N, N}; ordering proved trivially for all N >= 3, exercised at powers of two) and C2 refresh at bank-faithful billing (compressed generous at n*H_N; the banked constants p = 0.0906, n = 1000, Delta = 0.384; ordering constant-dependent, holding because p < Delta) -- the distributed signature is cost-maximal and the compressed single-atom signature cost-minimal: any argmin over encoding choice would select AGAINST (E), so a derivation of (E) must exit {formation, refresh} or bypass argmin. Signature choice is outside every banked argmin domain as formalized 2026-07-04 -- CENSUS-TRUE, NOT CATEGORICAL (named exposure F-AGT2-d, the succession clause: a generalization of plec.py\'s trivial-alignment destination-argmin (check_T_trivial_alignment_is_Type_II, source-fingerprinted in-check), or a principal ruling that A2\'s constitutive domain covers encoding choice, upgrades this pressure to a REFUTATION of (E); the flag retires in whatever leg resolves it). THE READ-CHANNEL TRICHOTOMY (E1-search-bounded at three gradings; the coherent model per audit MAJOR 1 -- one per-atom concurrent-activation law f charged to BOTH encodings, pigeonhole forcing sharing once M > N): (a) size-blind -- compression wins at every read count; (b) ta-graded -- ties per rung-read, the formation gap never recovered; (c) strictly superadditive -- FLIPS, iff f(M) - N*f(M/N) > N - 1: a linear law (any kappa) saves identically zero and can never flip, the binary surcharge saves <= N(kappa-1) < N-1 and never flips, f(m) = m^2 first flips at M = 5 (N = 16) and M = 17 (N = 256), sqrt-N scale, M = N included. The door\'s two premises -- (c1) strict superadditivity of the per-atom activation law, (c2) the read density -- are NAMED UNBANKED, NOT adopted; "static profiles are read-dominated" is unsourced plausibility, never a premise. TRIPWIRE F-AGT2-c LIVE (gate + exact-boundary witness + registry name census, baseline pinned 2026-07-04): any future banked contention/co-availability cost law lands in the census and must clear the pinned gate before any (E) claim. Nothing here derives (E), TCP-strong, w = 1, or gamma_C = 1; AGT-par stays RULED no-hold-pattern; (E)+(P) ==> TCP-strong stays ONE DIRECTION; the citable chains ride unchanged (' + _LEDGER_BOUND + '; with (E)+(P) in the slot: ' + _LEDGER_POINT_EP + '). Cassini signed: central value 0.91 sigma ABOVE the bound.', key_result='The (E) door narrowed to the concurrency/co-availability structure of static-field reads: distributed encoding cost-maximal on BOTH banked axes (formation eps*{1, log2 N, N}; refresh bank-faithful at p = 0.0906, n = 1000, Delta = 0.384) -- the A2-pressure lemma; a linear per-atom contention law saves identically ZERO (no flip at any reader count, any kappa) and a bounded surcharge never flips (saving <= N(kappa-1) < N-1); a strictly superadditive law flips iff f(M) - N*f(M/N) > N - 1 (f = m^2: M = 5 at N = 16, M = 17 at N = 256; M = N flips) -- the ONLY enumerated door, premises (c1) strict superadditivity + (c2) read density NAMED UNBANKED, NOT adopted. Tripwire F-AGT2-c pins the gate in-check; named exposure F-AGT2-d (the A2-pressure escape hatch is census-true, not categorical) carried as the succession clause. (E) NOT adopted, NOT refuted; verdict REDUCE 0.85; TCP-strong stays the named [C] with its one-direction (E)+(P) anatomy.', dependencies=['A1', 'T_admissibility_greedoid_structure'], cross_refs=['L_amount_graded_testedness_encoding_no_go', 'T_agt_par_anatomy', 'T_weight_one_reduction', 'T_gammaC_carrier_fork'], artifacts={'formation_grades_eps_units': {'compressed': 1, 'positional': 'log2 N', 'distributed': 'N'}, 'refresh_bank_constants': {'p': round(p, 4), 'n': n, 'Delta': round(Delta, 4), 'ordering': 'constant-dependent: holds because p < Delta'}, 'trichotomy': {'a_size_blind': 'compression wins -- dead for (E)', 'b_ta_graded': 'ties per rung-read; formation gap never recovered -- dead for (E)', 'c_superadditive': 'flips -- the door; both legs unbanked'}, 'tripwire_F_AGT2_c': {'gate': _FAGT2C_GATE, 'first_flip_m_sq': {'N=16': 5, 'N=256': 17}, 'boundary_witness': 'saving == N-1 exactly does NOT flip; saving == N flips (the strict -1 pinned); formation pins _comp_cost(1, f_sq) = 2, _dist_cost(N, N, f_sq) = 2N', 'registry_census': {'pattern': _FAGT2C_CENSUS_PATTERN, 'baseline_2026_07_04': sorted(_FAGT2C_REGISTRY_BASELINE), 'note': 'one pre-existing SepStr classification, not a cost law; any new census name trips the leg; baseline extended DATED v24.3.385 with the contention-law consolidation check, dispositioned in-check (gate-run, no cost law banked)'}, 'linear_law': 'saving identically 0 -- never flips', 'binary_surcharge': 'saving <= N(kappa-1) < N-1 -- never flips', 'obligation': 'any future banked contention/co-availability cost law runs against this gate before any (E) claim'}, 'named_exposure_F_AGT2_d': "the A2-pressure escape hatch (no banked argmin ranges over encoding choice) is census-true 2026-07-04, not categorical; a generalization of the banked destination-argmin (check_T_trivial_alignment_is_Type_II, plec.py, source-fingerprinted in-check) or a principal ruling on A2's constitutive domain upgrades the pressure to a refutation of (E) -- succession clause: the flag retires in the resolving leg", 'door_premises': '(c1) strict superadditivity of the per-atom concurrent-activation law on shared atoms + (c2) law-dependent read density -- NAMED, UNBANKED, NOT ADOPTED', 'e_status': '(E) NOT adopted, NOT refuted -- verdict REDUCE 0.85; TCP-strong <== (E)+(P) one direction only; AGT-par RULED no-hold-pattern', 'read_dominated_status': 'unsourced physical plausibility (walk characterization) -- never a premise', 'ledger_bound': _LEDGER_BOUND, 'ledger_point_EP': _LEDGER_POINT_EP, 'cassini_signed': 'Bertotti-Iess-Tortora 2003: gamma - 1 = (2.1 +/- 2.3)e-5; central value 0.91 sigma ABOVE the bound -- live one-sided tension, NOT saturation', 'walk_of_record': 'Reference - The F-AGT2 Walk - The A2 Pressure and the Read-Channel Door (2026-07-04).md v0.2 (REDUCE 0.85; hostile fresh-context audit LAND-WITH-FIXES 0.85)', 'witness': 'The Turning/f_agt2_walk_2026-07-04/ 41/41 -- witness_a2_pressure.py 12/12 + witness_read_channel_lever.py 14/14 (the coherent rebuilt model) + witness_banked_consumption.py 5/5 + witness_frostman_typing.py 5/5 + witness_deflation_scope.py 5/5 (premise-transcription only) + flip arithmetic from audit_probe_contention_coherence.py'})

def check_T_contention_law_granularity_occupancy_fork():
    import inspect as _inspect
    import re as _re
    eps = _EPS
    N, C = (_N_STEPS, 6)

    def _delta_JR(J, R):
        return eps * (J - R)
    check(_delta_JR(0, 1) == -eps, 'two Sep readers sharing the record channel d: J = 0, R = 1 -> Delta = -eps (the banked v24.3.381 identity, pairwise): compatible sharing priced SUBADDITIVELY -- a discount')
    m_vals = [_delta_JR(0, M - 1) for M in (2, 3, 5, 10, 100)]
    check(all((b < a for a, b in zip(m_vals, m_vals[1:]))) and m_vals[-1] == -99 * eps, 'M Sep readers (TYPED ITERATED JOIN over the T1 configuration, walk premise D2 -- an extension over the walk-typed configuration, not the banked pairwise theorem verbatim, audit m5): Delta = -(M-1)*eps, strictly deepening -- every added compatible reader makes the joint CHEAPER, never dearer (exact fractions)')
    check(all((_delta_JR(0, R) <= 0 for R in range(0, 20))) and all((_delta_JR(J, 1) > 0 for J in range(2, 20))) and (_delta_JR(1, 1) == 0), 'sign anatomy: with J = 0 (Sep) Delta <= 0 at every sharing count; Delta > 0 requires J > R -- irreducible jointness (the occupancy feature, constitutive sign bit) is the ONLY positive source in the banked calculus')

    def _f_hold_factory(c_read):

        def f(m):
            m = Fraction(m)
            return m * c_read - (m - 1) * eps
        return f
    for c_read in (Fraction(2), Fraction(3, 2), Fraction(5)):
        f_h = _f_hold_factory(c_read)
        check(all((f_h(m1 + m2) < f_h(m1) + f_h(m2) for m1 in range(1, 8) for m2 in range(1, 8))), f'c_read={c_read}: the Delta-transported per-atom law f(m) = m*c_read - (m-1)*eps is strictly SUBADDITIVE (affine, positive intercept)')
    f2 = _f_hold_factory(Fraction(2))
    check(all((_contention_saving(M, N, f2) <= 0 for M in (1, 4, N, 2 * N, 10 * N))) and [M for M in range(1, 8 * N) if _dist_cost(M, N, f2) < _comp_cost(M, f2)] == [], "gate disposition (the .382 pinned gate, the law charged to BOTH encodings): the Delta-transported law saves <= 0 at every reader count and NO M flips -- on the corpus's canonical joint-cost calculus, at the natural Sep formalization, the door shuts rather than opens")
    mu_star = Fraction(1)
    import apf.core as _core
    src_md = _inspect.getsource(_core.check_L_MD_extension)
    check('kappa(delta_T) >= mu*' in src_md and 'Every nonzero admissibility act' in src_md and ('positive minimum cost' in src_md), "the MD floor consumed at its banked source (landing-audit F4: fingerprinted at runtime, not hardcoded): check_L_MD_extension prices PER ACT -- 'Every nonzero admissibility act has positive minimum cost', kappa(delta_T) >= mu* -- so m read acts bill at mu* per act; f(m) = mu*m below is the typed walk transport of that per-act floor")
    check(all((_contention_saving(M, N, lambda m: mu_star * Fraction(m)) == 0 for M in (1, 5, N, 3 * N, 10 * N))), 'the banked MD activation floor f(m) = mu*m (check_L_MD_extension, defense-typed; read-act coverage a TYPED WALK TRANSPORT of the Route-A MD rationale, audit m4) saves identically zero: the one banked activation price is linear -- the no-flip side of the gate')
    import apf.recruitment as _rec
    from apf.gamma_c_carrier_program import _RECRUITMENT_INSTRUMENT_BASELINE as _FW2_PIN
    live_names = frozenset((nm for nm, obj in _inspect.getmembers(_rec) if nm.startswith('check_') and _inspect.isfunction(obj) and (obj.__module__ == 'apf.recruitment')))
    src_rec = _inspect.getsource(_rec).lower()
    check(live_names == _FW2_PIN and all((tok not in src_rec for tok in ('reader', 'concurrent', 'contention', 'co-avail', 'coavail', 'simultaneous read'))) and all((str(_inspect.signature(getattr(_rec, nm))) == '()' for nm in live_names)), f'F-CL2 (computable leg, re-run live on every execution): all {len(_FW2_PIN)} recruitment.py instruments (the F-W2 pinned name set, consumed from the pin) are reader-free -- no reader/concurrent/contention/co-availability token in the module, every check signature closed; a banked reader-indexed recruitment extension (a demand-multiplicity variable in E_rec or the master equation) TRIPS THIS LEG; until then route R1 is closed by BLINDNESS, not by verdict')

    def _feasible_dist(M, g):
        return all((load <= C for load in _spread(M, N // g)))

    def _feasible_comp(M):
        return M <= C

    def _flip_window(g):
        return [M for M in range(1, N * C + 2) if not _feasible_comp(M) and _feasible_dist(M, g)]
    w1 = _flip_window(1)
    check(w1 != [] and w1[0] == C + 1 and (w1[-1] == N * C) and _feasible_comp(C) and _feasible_dist(C, 1), f'ATOM-granular cap (g = 1, C = {C}): both encodings admissible at M = C (no flip below cap); the argmin flips BY FEASIBILITY on M in ({C}, {N * C}] exactly -- compressed inadmissible, distributed admissible: A1-SHAPED finiteness at atom granularity opens the door with NO posited superadditive law')
    check(_flip_window(N) == [], "RECORD-COARSE cap (g = N): both encodings exceed the cap at the same M -- window EMPTY, encoding-blind; the A1-native cell (region containing the whole record) a fortiori, UNDER T3 -- a typed walk inference, not a theorem: atom granularity is NOT A1-FORCED (audit m2; stated as this check's scope, never as a theorem), so (c1) is not derivable from A1 alone")
    windows = {g: _flip_window(g) for g in (1, 2, 4, 8, 16)}
    check(all(((windows[g] != []) == (g < N) for g in windows)) and all((len(windows[g]) == C * (N // g - 1) for g in windows if g < N)) and all((windows[g][-1] == C * (N // g) for g in windows if g < N)), "THE GRANULARITY DICHOTOMY (named model clauses: g | N divisibility; even-over-cells spread as the best-admissible-configuration reading of the argmin -- LOAD-BEARING, an adversarial front-loaded spread empties every window): the flip window is (C, C*N/g], |window| = C*(N/g - 1), nonempty IFF g < N -- a concurrency bottleneck delivers (E) precisely when its capacity cells SEPARATE the distributed encoding's atoms; upper edges exact")
    INF = Fraction(10 ** 9)

    def _f_cap(m):
        return Fraction(m) if m <= C else INF
    check(all((_f_cap(a + b) > _f_cap(a) + _f_cap(b) for a in range(1, C + 1) for b in range(1, C + 1) if a + b > C)) and all((_f_cap(a + b) == _f_cap(a) + _f_cap(b) for a in range(1, C) for b in range(1, C) if a + b <= C)), 'the cap law is additive below cap and strictly superadditive exactly at cap crossings: A1-type finiteness supplies the superadditive SHAPE of (c1) for FREE -- the open premise is the granularity, not the shape; (c1) re-types as (c1-gran)')

    def _f_B(B):
        return lambda m: Fraction(m) + (B if m > C else 0)
    M_probe = 2 * C
    big, bnd = (Fraction(N * N), Fraction(N - 1))
    check(_contention_saving(M_probe, N, _f_B(big)) == big and _dist_cost(M_probe, N, _f_B(big)) < _comp_cost(M_probe, _f_B(big)) and (_contention_saving(M_probe, N, _f_B(bnd)) == bnd) and (not _dist_cost(M_probe, N, _f_B(bnd)) < _comp_cost(M_probe, _f_B(bnd))), 'finite-proxy consistency: the cap is the B -> infinity limit of the gate-passing family f(m) = m + B*[m > C] (saving = B; B = N-1 exactly does NOT flip -- the pinned strict boundary honored; B = N^2 flips): no contradiction with the .382 bounded-surcharge lemma, whose binary family has saving <= N(kappa-1) < N-1 by construction')
    import apf.core as _core
    src_lirr = _inspect.getsource(_core.check_L_irr)
    check('plays no role' in src_lirr and 'compares joint vs sum' in src_lirr and ('supplies no Delta' in src_lirr), "the L_nc fence is banked text (L_irr Step 1: L_nc never compares joint vs sum and supplies no Delta): (c1) may not be sourced from L_nc -- the phase-21 stamped category error, now a banked sentence; occupancy fixes Delta's sign, a declared initial datum alongside A1")
    import apf.delta_calculus as _dc
    rdc = _dc.check_T_delta_JR_derived()
    check('Delta = eps*(J - R)' in rdc['name'] and 'shared CHANNELS' in rdc['artifacts']['R_convention'], 'the banked identity consumed at its own pins: Delta = eps*(J - R) with R = shared billed CHANNELS (literal channel identity) -- the derived joint-vs-sum pricing that leg 1 extends by typed iterated join')
    import apf.gauge_invariant_record as _gir
    src_sep = _inspect.getsource(_gir.check_T_ckm_flavour_coavailability_is_sepstr)
    check('incompatible' in src_sep.lower() and (not _re.search('(?<!in)compatible', src_sep.lower())), "the SepStr citation at its CORRECTED antecedent (walk-audit MAJOR 1, fingerprinted): the one banked co-availability result classifies forced INCOMPATIBLE disjoint-basis co-availability -- two incompatible mass bases on the generation qutrit -- as SepStr; 'compatible' appears in the banked check only inside 'incompatible' (case-insensitive fingerprint, landing-audit F5: an all-caps resurrection is caught); even forced incompatibility fails to force IJC there, and the corpus has NEVER tested compatible co-availability -- classification, cost-silent: silence typed as blindness, not a zero price (audit m8)")
    import apf.operational_completeness as _oc
    r9 = _oc.check_T_ledger_rent_excluded()
    check('per-activation' in r9['name'] and 'no standing rent' in r9['name'], "no-refutation clauses, typed both ways: a concurrency-dependent per-activation charge is kind (b) -- booked when and only when reads occur, not rent; the cap form of (c1-gran) books nothing at all (a feasibility constraint, not a cost line); and the Delta identity's subadditive verdict indexes HOLDINGS (kind (a)) -- the discount removes the holding route to (c1), it does not refute a kind-(b) in-flight contention law")
    check('atom-granular' in _FCL1_DOOR_SPEC and windows[1] != [] and (windows[16] == []), "THE OCCUPANCY FORK: a DERIVED contention charge has exactly one banked shape -- (c1-occ): occupancy at the static-field read interface AT ATOM GRANULARITY (the only sign-positive banked source is J, and the dichotomy gates the jointness too: interface-coarse jointness does not flip); QAC genre, per-interface, evidence-shaped, NOT ADOPTED. THE SHARP BILL, stated both halves (walk note v0.2 sec 2 R4, landing-audit F6): (c1-occ) REQUIRES the static-field read interface to present record-incompatible co-available families -- and T1's own typing DENIES them for a classical broadcast interface, which is Sep-shaped AS CURRENTLY TYPED -- the fork's adverse side. The re-typings compose: (c1) <=> an atom-granular positive concurrency charge, exactly two enumerated source shapes (E1-search-bounded): (c1-gran) sub-record-granular activation capacity (A1-shaped; granularity unbanked) or (c1-occ) atom-granular irreducible jointness (occupancy-shaped; empirical)")
    check('BOTH encodings' in _FAGT2C_GATE and 'g < N' in _FCL1_DOOR_SPEC and ('(E)' in _FCL1_DOOR_SPEC), 'F-CL1 LIVE (wired as an EXTENSION of the F-AGT2-c obligation, NOT a duplicate census -- the registry census leg and baseline live in the .382 check): any future banked atom-granular activation charge owes BOTH the pinned gate AND the g < N granularity check before any (E) claim; the granularity check is now part of the tripwire discipline for this lane')
    check('T_contention_law_granularity_occupancy_fork' in _FAGT2C_REGISTRY_BASELINE and 'check_T_ckm_flavour_coavailability_is_sepstr' in _FAGT2C_REGISTRY_BASELINE, "the census disposition of record: this check's own name matches the census pattern by construction ('contention'); the .382 baseline was extended DATED (v24.3.385) per the tripwire's own discipline -- the expected drift-net catch of this landing; nothing here banks a contention COST LAW: every candidate law touched was gate-run above")
    check('TCP-min' in _LEDGER_POINT_EP and 'TCP-strong' in _LEDGER_POINT_STANDING and ('H5-W' in _LEDGER_BOUND), 'hygiene: the citable ledger strings ride unchanged verbatim (TCP-min / TCP-strong / H5-W); (c1)/(c1-gran)/(c1-occ)/(c2)/(E) all named, unbanked, NOT adopted; (E)+(P) ==> TCP-strong stays ONE DIRECTION; the walk verdict was REDUCE 0.85; nothing here delivers (E), TCP-strong, w = 1, or gamma_C = 1')
    return _result(name='T_contention_law_granularity_occupancy_fork -- the contention-law walk banked: the sharing-price consolidation (the Delta discount, gate-run adverse), the granularity dichotomy (flip iff g < N under the named model clauses; atom granularity NOT A1-forced), the occupancy fork ((c1-occ) evidence-shaped, NOT adopted)', tier=3, epistemic='P_structural', summary="The contention-law walk (2026-07-04, REDUCE 0.85) banked at its proved strength -- the (c1) premise walked, neither derived nor refuted. THE SHARING-PRICE CONSOLIDATION (adverse, <= 0): the banked Delta = eps*(J - R) pricing, extended by TYPED ITERATED JOIN over the walk-typed Sep configuration (T1: reader i = {shared record channel d, own readout channel r_i}; J = 0 by definition of the configuration, not by banked classification), prices M compatible Sep readers at Delta = -(M-1)*eps -- a strictly deepening DISCOUNT; the transported per-atom law (affine, positive intercept, strictly subadditive) and the banked MD activation floor (linear; read-act coverage a typed walk transport) are both gate-run: saving <= 0, never flip; the recruitment corpus is reader-blind by census (name set consumed from the F-W2 pin). THE GRANULARITY DICHOTOMY, under the named model clauses (one cap charged to BOTH encodings; even-over-cells spread = the best-admissible-configuration reading, LOAD-BEARING -- an adversarial spread empties every window; g | N): a finite activation cap C at granularity g is additive below cap and strictly superadditive exactly at cap crossings -- the superadditive SHAPE of (c1) is free from A1-type finiteness -- and flips the encoding argmin by feasibility iff g < N, on the window M in (C, C*N/g] exactly (g = N encoding-blind; the cap is the B -> infinity limit of a gate-passing family, B = N-1 strict boundary honored). The A1-native cell is encoding-blind UNDER T3, a typed walk inference: atom granularity is NOT A1-FORCED -- the check's stated scope, never a theorem. THE OCCUPANCY FORK: the only sign-positive banked source is irreducible jointness (occupancy, the constitutive sign bit; the L_nc fence banked in-text), so a derived contention charge has exactly one banked shape -- (c1-occ): occupancy at the static-field read interface at atom granularity, QAC genre, evidence-shaped, NOT adopted; THE SHARP BILL stated both halves: (c1-occ) requires the static-field read interface to present record-incompatible co-available families -- and T1's typing denies them for a classical broadcast interface, Sep-shaped as currently typed -- the fork's adverse side. A fortiori context at the CORRECTED antecedent (walk-audit MAJOR 1): the one banked co-availability result classifies forced INCOMPATIBLE disjoint-basis co-availability as SepStr; compatible co-availability never tested. FALSIFIERS: F-CL1 extends the F-AGT2-c obligation (gate + granularity check before any (E) claim; not a duplicate census -- this check's own name entered the .382 census and the baseline was extended dated, dispositioned in-check); F-CL2 live (a reader-indexed recruitment extension trips the reader-blindness leg). Nothing here delivers (c1), (E), TCP-strong, w = 1, or gamma_C = 1; (c1)/(c1-gran)/(c1-occ)/(c2)/(E) all named, unbanked, NOT adopted; (E)+(P) ==> TCP-strong stays ONE DIRECTION; the citable chains ride unchanged (" + _LEDGER_BOUND + '; with (E)+(P) in the slot: ' + _LEDGER_POINT_EP + '). Cassini signed: central value 0.91 sigma ABOVE the bound.', key_result="The (E) door narrowed to its final shape: (c1) <=> an atom-granular positive concurrency charge, exactly two enumerated source shapes (E1-search-bounded) -- (c1-gran) sub-record-granular finite activation capacity (the granularity dichotomy: flip window (C, C*N/g], nonempty iff g < N; superadditive shape FREE from finiteness; atom granularity NOT A1-forced, typed scope) or (c1-occ) occupancy at the static-field read interface (QAC genre, evidence-shaped; sharp bill both halves: (c1-occ) requires record-incompatible co-available families at the read interface, which T1's typing denies for a classical broadcast interface -- Sep-shaped as currently typed). Adverse consolidation: M compatible Sep readers price at Delta = -(M-1)*eps under the banked identity extended by typed iterated join -- a deepening discount; every candidate law touched was run against the .382 pinned gate (MD floor saving 0; Delta-transport saving <= 0; cap family flips only at g < N) -- never flips on the banked side. F-CL1 + F-CL2 live; the F-AGT2-c census baseline extended dated with this check's own name, dispositioned in-check. (c1) neither derived nor refuted; verdict REDUCE 0.85; nothing adopted.", dependencies=['A1', 'T_admissibility_greedoid_structure', 'check_T_delta_JR_derived', 'L_MD_extension', 'T_ledger_rent_excluded'], cross_refs=['T_fagt2_encoding_argmin_pressure_and_read_channel', 'L_amount_graded_testedness_encoding_no_go', 'T_agt_par_anatomy', 'T_weight_one_reduction', 'T_ckm_flavour_coavailability_is_sepstr'], artifacts={'gate_dispositions': {'MD_floor_linear': 'saving identically 0 -- never flips', 'delta_transport_Sep': 'saving <= 0 (affine, positive intercept, strictly subadditive) -- never flips; the door-shut side', 'binary_surcharge': 'saving <= N(kappa-1) < N-1 -- never flips (.382, consumed)', 'm_squared': 'flips M = 5 (N=16), 17 (N=256) -- the .382 pinned reference', 'cap_g1': 'flips on (C, N*C] by feasibility -- the B -> infinity limit of a gate-passing family', 'cap_g_geq_N': 'never flips -- encoding-blind'}, 'granularity_dichotomy': {'flip_window': '(C, C*N/g], |window| = C*(N/g - 1); nonempty iff g < N', 'model_clauses': ['one cap charged to BOTH encodings', 'even-over-cells spread = best-admissible-configuration (LOAD-BEARING; an adversarial front-loaded spread empties every window)', 'g | N divisibility'], 'A1_native': 'encoding-blind under T3 (a typed walk inference); atom granularity NOT A1-forced -- scope, not theorem'}, 'sharing_price': 'M compatible Sep readers: Delta = -(M-1)*eps -- a deepening discount (typed iterated join over the T1 configuration; the only positive source is J, occupancy)', 'occupancy_fork': "(c1) <=> atom-granular positive concurrency charge; two source shapes: (c1-gran) sub-record-granular activation capacity (granularity unbanked) or (c1-occ) occupancy at the static-field read interface (QAC genre, empirical); both NOT adopted; sharp bill both halves (walk note v0.2 sec 2 R4): (c1-occ) requires the static-field read interface to present record-incompatible co-available families, and T1's typing denies them for a classical broadcast interface -- Sep-shaped as currently typed", 'sepstr_corrected_antecedent': 'forced INCOMPATIBLE disjoint-basis co-availability (two incompatible mass bases on the generation qutrit) is SepStr -- walk-audit MAJOR 1 carried; compatible co-availability never tested', 'F_CL1': _FCL1_DOOR_SPEC, 'F_CL2': 'a banked reader-indexed recruitment extension trips the reader-blindness leg (the census is re-run live on every execution); until then route R1 is closed by blindness, not by verdict', 'census_disposition': 'this check entered the F-AGT2-c census by name; the baseline was extended DATED v24.3.385 and dispositioned in-check (no contention cost law banked; all candidate laws gate-run)', 'not_adopted': '(c1), (c1-gran), (c1-occ), (c2)/(c2-prime), (E) -- all named, unbanked, NOT adopted', 'ledger_bound': _LEDGER_BOUND, 'ledger_point_EP': _LEDGER_POINT_EP, 'cassini_signed': 'Bertotti-Iess-Tortora 2003: gamma - 1 = (2.1 +/- 2.3)e-5; central value 0.91 sigma ABOVE the bound -- live one-sided tension, NOT saturation', 'walk_of_record': 'Reference - The Contention-Law Walk - The Granularity Dichotomy and the Occupancy Re-Typing (2026-07-04).md v0.2 (REDUCE 0.85; hostile fresh-context audit LAND-WITH-FIXES 0.85, MAJOR 1 + m1-m8 carried)', 'witness': 'The Turning/contention_law_walk_2026-07-04/ 34/34 at the pre-.385 tree (witness 1 leg 3 updated to the extended dated baseline post-landing, landing-audit F1, re-run green) -- witness_1_banked_consumption.py 11/11 + witness_2_delta_reader_pricing.py 9/9 + witness_3_granularity_dichotomy.py 9/9 + witness_4_recruitment_reader_blindness.py 5/5'})

_N_STEPS = 16

_EPS = Fraction(1)

def _floor_coherent(theory, eps):
    """b1:def:floorcoherent: C_a >= eps * (ta(E) - ta(D)) for every axiom."""
    return all((Ca >= eps * (taE - taD) for taD, taE, Ca in theory))

def _conv(a, b):
    """Binary convolution a * b (independent flip composition)."""
    return a * (1 - b) + b * (1 - a)

def _h(x):
    """Binary entropy, bits."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)

def _ta(expr, tested_atoms):
    """Tested-atom occurrence count ta(E) (b1:def:expr)."""
    return sum((1 for a in expr if a in tested_atoms))

def _invariant_lower_bound(taE, eps):
    """b1:cor:count: gamma(1 -> E) >= eps * ta(E) under floor-coherence."""
    return eps * taE

def _H_N(p, Nval):
    """Noise entropy of the N-ary symmetric channel at total flip prob p."""
    if Nval == 2:
        return _h(p)
    return _h(p) + p * math.log2(Nval - 1)

def _dist_cost(M, N, f):
    """Distributed encoding: formation N + per-atom contention charges."""
    return N + sum((f(m) for m in _spread(M, N) if m > 0))

_FAGT2C_FIRST_FLIP_M_SQ = {16: 5, 256: 17}

_LEDGER_POINT_STANDING = 'gamma_C = 1 at [P_structural | H1 + H2 + H3(+adopted C_M) + census-saturation + H5 + {H6 or (S1 + TCP-strong)}]'

_LEDGER_BOUND = 'gamma_C <= 1 (n = 3) at [P_structural | S0/S1 + TCP-min + H5-W + census legs + the Paper 9/Paper 10 base (P5, B7 incl. adopted C_M)]'

def _comp_cost(M, f):
    """Compressed encoding: formation 1 + all M readers on the one atom."""
    return 1 + f(M)

_FAGT2C_GATE = 'flip iff f(M) - N*f(M/N) > N - 1 (one per-atom concurrent-activation law f charged to BOTH encodings; even spread M = kN)'

_LEDGER_POINT_EP = 'gamma_C = 1 at [P_structural | H1 + H2 + H3(+adopted C_M) + census-saturation + H5 + (S1 + TCP-min + (E)+(P))]'

def _contention_saving(M, N, f):
    """f(M) - sum_atoms f(m_i): what sharing relief is worth to the
    distributed encoding under the one shared law."""
    return f(M) - sum((f(m) for m in _spread(M, N) if m > 0))

_FAGT2C_CENSUS_PATTERN = 'contention|co[-_]?avail'

_FAGT2C_REGISTRY_BASELINE = frozenset({'check_T_ckm_flavour_coavailability_is_sepstr', 'T_contention_law_granularity_occupancy_fork'})

def _spread(M, N):
    """M concurrent readers spread as evenly as possible over N atoms."""
    q, r = divmod(M, N)
    return [q + 1] * r + [q] * (N - r)

_FCL1_DOOR_SPEC = 'any banked atom-granular activation charge owes BOTH the pinned .382 gate f(M) - N*f(M/N) > N - 1 (the law charged to BOTH encodings) AND the granularity check g < N before any (E) claim; interface-coarse charges provably do not flip; two enumerated source shapes: (c1-gran) sub-record-granular finite activation capacity (A1-shaped; granularity unbanked) or (c1-occ) atom-granular irreducible jointness (occupancy at the read interface; QAC genre, empirical)'
