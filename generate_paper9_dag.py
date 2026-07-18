#!/usr/bin/env python3
"""generate_paper9_dag.py — build the typed Paper 9 closure DAG.

Emits, deterministically, from the ledger encoded below:
  - paper9_typed_dependency_dag.json   (nodes + typed edges + provenance)
  - interactive_dag.html               (self-contained browser view)

This is the Paper 9 v3.7 / Technical Supplement v1.1 closure ledger — NOT the
full APF-Engine graph. It types every node (APF-native proof, standard math
import, conditional theorem, exact model certificate, named open gate, external
Paper 6 endpoint, executable witness) and every edge, so a reviewer can read
the dependency structure, the open gates, and where a local executable witness
is attached. A node carries a local check only where an executable witness
exists; conditional and open gates are shown explicitly.
"""
import json, html
from pathlib import Path

ENGINE = {"version": "24.3.427", "commit": "7ab898e", "bank_size": 3918}

NODE_CLASSES = [
    "APF_NATIVE", "STANDARD_IMPORT", "CONDITIONAL_THEOREM", "MODEL_CERTIFICATE",
    "NAMED_OPEN_GATE", "EXTERNAL_ENDPOINT", "EXECUTABLE_WITNESS",
]
EDGE_CLASSES = [
    "DEPENDS_ON", "IMPORTS", "REQUIRES_GATE", "CERTIFIED_BY_MODEL",
    "WITNESSED_BY_CHECK", "EXTERNALIZES_TO", "CROSS_REFERENCE",
]

# ---- executable witnesses (the nine bundled checks; grades are the real
#      registry grades, verified by run_checks.py) ------------------------
WITNESS = [
    ("W_scope_contract", "check_T_finite_operational_basis_scope_contract",
     "P_structural_instrument",
     "Names the atom-cover hypotheses; exact boundary C=1999999999/2000000000 gives N=0; a finite no-amalgamation countermodel keeps the general bridge open."),
    ("W_finite_basis", "check_T_finite_operational_basis", "P_structural",
     "Exact-Fraction finite atom-cover model: a complete minimal operational-distinction basis exists with |B_U| <= floor(C_U/eps*); every control arm fires; no float tolerance enlarges the admitted set."),
    ("W_min_joint", "check_T_finite_minimal_joint_realization_atom_cover", "P_structural",
     "One compatible minimum no-excess joint carrier realizes the complete basis; independent minima with distinct joint ids are rejected."),
    ("W_held_record", "check_T_held_to_record_typing", "P_structural_reading",
     "Held carrier H, invariant record quotient R(H), and outcome instruments {C_i} are three distinct typed objects on one common ==-decided record space; distinctness follows from nonzero radical + SSB degeneracy, each shown load-bearing by a collapse control on the degenerated model."),
    ("W_gammaC_fork", "check_T_gammaC_carrier_fork", "P_structural",
     "The four carrier closures solve to gamma_C in {1, 1/3, 0, -1}; gamma_GR(n)=1/(n-2) matches the plane carrier only at n=3; pooled/per-channel Cassini-dead; the weight-one curve gamma(w)=w/((n-1)-w)."),
    ("W_weight_one", "check_T_weight_one_reduction", "P_structural",
     "Exact-rational weight-one walk: w=D(deposit)/D(commitment); exchange annihilation; the scalar mode vanishes iff w=1. Nothing here derives w=1; the citable no-source bound is gamma_C<=1 at n=3 with TCP-min/TCP-strong named [C]."),
    ("W_agt_nogo", "check_L_amount_graded_testedness_encoding_no_go", "P_structural_instrument",
     "The GCC floor invariant grades representation, not magnitude: three floor-coherent signatures hold the same N-valued record at eps*{1,log2 N,N} — no amount-graded-testedness principle is a theorem of the floor invariant (magnitude-to-count transport is signature data)."),
    ("W_fagt2", "check_T_fagt2_encoding_argmin_pressure_and_read_channel", "P_structural",
     "The (E) door walked: distributed encoding is cost-maximal on both banked axes; linear contention saves nothing; the strictly-superadditive flip gate f(M)-N f(M/N)>N-1 is pinned. (E) neither adopted nor refuted."),
    ("W_contention", "check_T_contention_law_granularity_occupancy_fork", "P_structural",
     "The contention-law walk: sharing-price consolidation (Delta discount, gate-run adverse), the granularity dichotomy (flip iff g<N under named clauses), and the occupancy fork ((c1-occ) evidence-shaped, not adopted)."),
]

# ---- ledger nodes: G9 spine + supplement package + imports + external -----
# tuple: (id, label, node_class, status, summary)
NODES = [
    # cross-reference anchors
    ("P10_grammar", "Continuation grammar (Paper 10)", "CONDITIONAL_THEOREM", "I",
     "The judgment G |-_C D->E and geometry-as-continuation-cost are imported from Paper 10 as primitive grammar."),
    ("P2_linear", "Linear Paper 2 specialization", "APF_NATIVE", "P",
     "The flat quotient branch with optimal response gains, proved as a specialization."),
    ("P14_record", "Record-transition typing (Paper 14 / TS def:ts-record-transition)", "APF_NATIVE", "P_structural_reading",
     "The held-carrier / invariant-record-quotient / outcome-instrument split on a common record space; a declared structural reading, not a primitive theorem."),
    # finite-basis package
    ("joint_pkg", "Joint-realizability package", "NAMED_OPEN_GATE", "O/G",
     "Finite joint extension + minimum attainment + closure invariance + positive marginal extension floor: the named package the general finite-basis theorem is conditional on."),
    ("atom_model", "Exact atom-cover model certificate", "MODEL_CERTIFICATE", "model",
     "The Engine-certified finite atom-cover instantiation of the finite-basis mechanism and one compatible minimum joint carrier: an exact model witness, not the general theorem."),
    ("G9_1", "G9.1 A finite complete operational basis exists", "CONDITIONAL_THEOREM", "R|G/C",
     "General basis existence is conditional on the joint-realizability package; the exact atom-cover model is Engine-certified."),
    ("G9_2", "G9.2 Basis realized as finite separating precision channels", "NAMED_OPEN_GATE", "O/G",
     "Faithful operational-to-precision-channel realization: a named open gate; operational content is not yet a physical precision-channel family."),
    ("G9_3", "G9.3 Record topology is Hausdorff and second countable", "CONDITIONAL_THEOREM", "P|G",
     "State separation gives Hausdorff; second countability needs a countable specification grammar and a topology-generating subfamily (gate)."),
    ("G9_4", "G9.4 Finite smooth generation -> subcartesian differential space", "CONDITIONAL_THEOREM", "P|G",
     "Proved under the finite smooth-generation gate."),
    ("G9_5", "G9.5 Complete local continuation flows generate smooth orbits", "CONDITIONAL_THEOREM", "I/P",
     "On the finite-differential-presentation locus, the imported subcartesian orbit theorem gives immersed smooth continuation orbits."),
    ("G9_6", "G9.6 Smooth response-factor completeness gives ker D-beta = N^ctx", "CONDITIONAL_THEOREM", "P|G",
     "The boxed kernel identity holds under the two-way smooth factorization gate; equal response fibres are insufficient for equal derivative kernels."),
    ("G9_7", "G9.7 Intrinsic response-orbit quotient gauge and length", "APF_NATIVE", "P",
     "Proved intrinsically on the regular quotient (thm:canonical-operational-anchor, thm:response-orbit-length)."),
    ("G9_8", "G9.8 Physical anchor pulls length back to site geometry", "NAMED_OPEN_GATE", "O/C",
     "Construct s and A = q . Ds, type the null kernel and provenance, prove direct-germ calibration (gate:physical-substrate-anchor)."),
    ("G9_9", "G9.9 Calibrated physical path cost bi-Lipschitz to response distance", "CONDITIONAL_THEOREM", "P|H",
     "Comparison theorem proved; ledger-rate bounds and response-class completeness remain physical inputs (thm:ledger-calibration)."),
    ("G9_10", "G9.10 Smooth residual energy is half squared local distance", "CONDITIONAL_THEOREM", "P|SRR",
     "Proved locally when the residual Hessian is positive definite (thm:residual-energy-distance)."),
    ("G9_11", "G9.11 Parallelogram quadraticity gives a positive cost metric", "APF_NATIVE", "P|Q",
     "Proved from the parallelogram certificate; whether the substrate passes it is open (prop:positive-cost-metric)."),
    ("G9_12", "G9.12 Positive pullback geometry cannot supply Lorentzian signature", "APF_NATIVE", "P",
     "Positive cost is explicitly separated from Lorentzian comparison geometry (prop:positive-pullback-no-lorentz)."),
    ("G9_13", "G9.13 Signed Lorentz-Finsler comparison structure for the causal cone", "NAMED_OPEN_GATE", "O/C",
     "Derive the causal cone, orientation, signed two-homogeneous function, and Lorentzian Hessian (gate:signed-comparison)."),
    ("G9_14", "G9.14 Isotropic quadratic exterior recruitment gives chi ~ 1/r", "CONDITIONAL_THEOREM", "C/P",
     "Proved from an assumed isotropic quadratic exterior kernel (prop:point-source-profile)."),
    ("G9_15", "G9.15 Calibrated clock response conditionally recovers redshift", "CONDITIONAL_THEOREM", "R",
     "Conditional recovery under load law, calibration, and the proper-time dictionary."),
    ("G9_16", "G9.16 Generator trace equals comparison-volume variation", "APF_NATIVE", "P/C",
     "Proved in the represented clock-ruler comparison plane (thm:trace-volume)."),
    ("G9_17", "G9.17 Linear loaded equilibrium h_chi = chi K^-1 J + O(chi^2)", "CONDITIONAL_THEOREM", "P|H",
     "Proved under the gauge-fixed response-Hessian hypothesis (thm:no-trace-operator)."),
    ("G9_18", "G9.18 The no-trace gate is Ptr K^-1 J = 0", "NAMED_OPEN_GATE", "O/C",
     "The decisive local theorem; source-selection or a constrained-volume theorem are the principal routes."),
    ("G9_19", "G9.19 No trace gives gamma_C = 1 and the first-PN exterior", "CONDITIONAL_THEOREM", "C/R",
     "Follows conditionally from the no-trace gate through the trace-volume theorem (cor:ppn-volume-mode, thm:conditional-weak-field)."),
    ("G9_20", "G9.20 The represented nonlinear closure is Einstein gravity", "EXTERNAL_ENDPOINT", "I/C",
     "External Paper 6 H1-H3/A9/Lovelock endpoint; the finite-continuability translation remains open."),
    # standard math imports
    ("imp_sikorski", "Sikorski differential-space structure", "STANDARD_IMPORT", "import",
     "Standard Sikorski differential-space machinery (thm:ts-sikorski)."),
    ("imp_subcart", "Subcartesian / orbit theorem", "STANDARD_IMPORT", "import",
     "Standard subcartesian differential-space and immersed-orbit theorems (thm:ts-subcartesian, thm:ts-orbit-import)."),
    ("imp_constrank", "Constant-rank theorem", "STANDARD_IMPORT", "import",
     "Standard constant-rank / initial-topology results (thm:ts-constant-rank, thm:ts-initial-topology)."),
    ("imp_lovelock", "Lovelock endpoint import", "STANDARD_IMPORT", "import",
     "Standard Lovelock uniqueness feeding the Paper 6 external endpoint."),
]

EDGES = [
    # finite-basis package
    ("G9_1", "joint_pkg", "REQUIRES_GATE"),
    ("G9_1", "atom_model", "CERTIFIED_BY_MODEL"),
    ("atom_model", "W_finite_basis", "WITNESSED_BY_CHECK"),
    ("atom_model", "W_scope_contract", "WITNESSED_BY_CHECK"),
    ("atom_model", "W_min_joint", "WITNESSED_BY_CHECK"),
    ("W_finite_basis", "W_scope_contract", "DEPENDS_ON"),
    ("W_min_joint", "W_finite_basis", "DEPENDS_ON"),
    ("G9_1", "P10_grammar", "CROSS_REFERENCE"),
    # spine dependency chain
    ("G9_2", "G9_1", "DEPENDS_ON"),
    ("G9_3", "G9_2", "DEPENDS_ON"),
    ("G9_4", "G9_3", "DEPENDS_ON"),
    ("G9_5", "G9_4", "DEPENDS_ON"),
    ("G9_6", "G9_5", "DEPENDS_ON"),
    ("G9_7", "G9_6", "DEPENDS_ON"),
    ("G9_8", "G9_7", "DEPENDS_ON"),
    ("G9_9", "G9_8", "DEPENDS_ON"),
    ("G9_10", "G9_9", "DEPENDS_ON"),
    ("G9_11", "G9_10", "DEPENDS_ON"),
    ("G9_12", "G9_11", "DEPENDS_ON"),
    ("G9_13", "G9_12", "DEPENDS_ON"),
    ("G9_16", "G9_7", "DEPENDS_ON"),
    ("G9_17", "G9_16", "DEPENDS_ON"),
    ("G9_18", "G9_17", "DEPENDS_ON"),
    ("G9_19", "G9_18", "DEPENDS_ON"),
    ("G9_20", "G9_19", "DEPENDS_ON"),
    # gates required by conditional theorems
    ("G9_3", "G9_2", "REQUIRES_GATE"),
    ("G9_6", "G9_6", "REQUIRES_GATE") if False else ("G9_7", "G9_8", "REQUIRES_GATE"),
    ("G9_14", "G9_13", "REQUIRES_GATE"),
    ("G9_19", "G9_18", "REQUIRES_GATE"),
    # imports
    ("G9_4", "imp_sikorski", "IMPORTS"),
    ("G9_5", "imp_subcart", "IMPORTS"),
    ("G9_6", "imp_constrank", "IMPORTS"),
    ("G9_20", "imp_lovelock", "IMPORTS"),
    # record layer / held-to-record
    ("G9_3", "P14_record", "DEPENDS_ON"),
    ("P14_record", "W_held_record", "WITNESSED_BY_CHECK"),
    ("P14_record", "P14_record", "CROSS_REFERENCE") if False else ("W_held_record", "P14_record", "CROSS_REFERENCE"),
    # weak-field witnesses
    ("G9_19", "W_gammaC_fork", "WITNESSED_BY_CHECK"),
    ("G9_19", "W_weight_one", "WITNESSED_BY_CHECK"),
    ("W_weight_one", "W_gammaC_fork", "DEPENDS_ON"),
    ("W_weight_one", "W_agt_nogo", "DEPENDS_ON"),
    ("W_fagt2", "W_agt_nogo", "DEPENDS_ON"),
    ("W_contention", "W_fagt2", "DEPENDS_ON"),
    ("G9_19", "W_agt_nogo", "WITNESSED_BY_CHECK"),
    # linear specialization + externalization
    ("G9_7", "P2_linear", "CROSS_REFERENCE"),
    ("G9_20", "G9_20", "CROSS_REFERENCE") if False else ("G9_19", "G9_20", "EXTERNALIZES_TO"),
]
EDGES = [e for e in EDGES if e]

def build():
    wnodes = [dict(id=i, label=nm, node_class="EXECUTABLE_WITNESS", status=g,
                   summary=s, check=nm) for (i, nm, g, s) in WITNESS]
    lnodes = [dict(id=i, label=l, node_class=c, status=st, summary=s)
              for (i, l, c, st, s) in NODES]
    nodes = lnodes + wnodes
    ids = {n["id"] for n in nodes}
    edges = []
    for src, dst, cls in EDGES:
        assert src in ids, f"edge src missing: {src}"
        assert dst in ids, f"edge dst missing: {dst}"
        assert cls in EDGE_CLASSES, f"bad edge class: {cls}"
        edges.append(dict(source=src, target=dst, edge_class=cls))
    # invariants the release gate cares about
    assert all(n["summary"].strip() for n in nodes), "blank summary present"
    assert edges, "no links"
    return dict(
        schema="apf.paper9.typed_dependency_dag.v1",
        paper="Paper 9 v3.7 / Technical Supplement v1.1",
        engine=ENGINE,
        node_classes=NODE_CLASSES, edge_classes=EDGE_CLASSES,
        counts=dict(nodes=len(nodes), edges=len(edges),
                    witnesses=len(wnodes), open_gates=sum(1 for n in nodes if n["node_class"]=="NAMED_OPEN_GATE")),
        nodes=nodes, edges=edges,
    )

CLASS_COLOR = {
    "APF_NATIVE": "#4C9A2A", "STANDARD_IMPORT": "#6c757d",
    "CONDITIONAL_THEOREM": "#e08e0b", "MODEL_CERTIFICATE": "#3b7dd8",
    "NAMED_OPEN_GATE": "#c0392b", "EXTERNAL_ENDPOINT": "#7d3cb5",
    "EXECUTABLE_WITNESS": "#128a6f",
}

def render_html(dag):
    j = json.dumps(dag)
    legend = "".join(
        f'<span class="lg"><i style="background:{CLASS_COLOR[c]}"></i>{c}</span>'
        for c in NODE_CLASSES)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Paper 9 v3.7.1 — Typed Closure DAG</title>
<style>
 body{{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:0;background:#0f1115;color:#e8e8e8}}
 header{{padding:14px 20px;background:#171a21;border-bottom:1px solid #2a2f3a}}
 h1{{font-size:16px;margin:0 0 4px}} .sub{{font-size:12px;color:#9aa4b2}}
 .legend{{padding:8px 20px;font-size:11px;background:#12151b;border-bottom:1px solid #2a2f3a}}
 .lg{{margin-right:14px;white-space:nowrap}} .lg i{{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:5px;vertical-align:middle}}
 #wrap{{display:flex;height:calc(100vh - 96px)}}
 svg{{flex:1}} #side{{width:360px;padding:14px 16px;overflow:auto;background:#12151b;border-left:1px solid #2a2f3a;font-size:12.5px;line-height:1.5}}
 .node circle{{stroke:#0f1115;stroke-width:1.5px;cursor:pointer}} .node text{{fill:#cfd6e0;font-size:10px;pointer-events:none}}
 line.edge{{stroke:#3a4150;stroke-width:1.2px}} .badge{{display:inline-block;padding:1px 6px;border-radius:3px;font-size:10px;color:#fff}}
 code{{color:#7fd1c0}}
</style></head><body>
<header><h1>Paper 9 — Typed Closure Dependency DAG</h1>
<div class="sub">v3.7 / Technical Supplement v1.1 · engine v{ENGINE['version']} ({ENGINE['commit']}, bank {ENGINE['bank_size']}) · {dag['counts']['nodes']} nodes · {dag['counts']['edges']} typed links · {dag['counts']['witnesses']} executable witnesses · {dag['counts']['open_gates']} named open gates. This is the Paper 9 closure ledger, not the full engine graph.</div></header>
<div class="legend">{legend}</div>
<div id="wrap"><svg id="svg"></svg><div id="side"><b>Click a node</b><br>Its type, status, summary, and typed edges appear here.</div></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script>
const DAG = {j};
const CC = {json.dumps(CLASS_COLOR)};
const svg = d3.select("#svg"), W = svg.node().clientWidth, H = svg.node().clientHeight;
const g = svg.append("g");
svg.call(d3.zoom().on("zoom", e => g.attr("transform", e.transform)));
const link = g.selectAll("line").data(DAG.edges).enter().append("line").attr("class","edge");
const node = g.selectAll(".node").data(DAG.nodes).enter().append("g").attr("class","node")
  .call(d3.drag().on("start",ds).on("drag",dg).on("end",de)).on("click",(e,d)=>show(d));
node.append("circle").attr("r", d=>d.node_class==="EXECUTABLE_WITNESS"?9:7).attr("fill",d=>CC[d.node_class]);
node.append("text").attr("dx",11).attr("dy",3).text(d=>d.id);
const sim = d3.forceSimulation(DAG.nodes)
  .force("link", d3.forceLink(DAG.edges).id(d=>d.id).distance(70).strength(.5))
  .force("charge", d3.forceManyBody().strength(-260))
  .force("center", d3.forceCenter(W/2,H/2)).force("collide",d3.forceCollide(22));
sim.on("tick",()=>{{link.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y).attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
  node.attr("transform",d=>`translate(${{d.x}},${{d.y}})`);}});
function show(d){{const ins=DAG.edges.filter(e=>e.target===d.id||e.target.id===d.id), outs=DAG.edges.filter(e=>e.source===d.id||e.source.id===d.id);
 const eline=e=>`<div>&middot; <span class="badge" style="background:#333">${{e.edge_class}}</span> ${{(e.source.id||e.source)===d.id?"&rarr; "+(e.target.id||e.target):"&larr; "+(e.source.id||e.source)}}</div>`;
 document.getElementById("side").innerHTML =
  `<div><span class="badge" style="background:${{CC[d.node_class]}}">${{d.node_class}}</span> <b>${{d.id}}</b></div>
   <p><b>${{d.label}}</b></p><p><i>status:</i> <code>${{d.status}}</code>${{d.check?` &nbsp; <i>check:</i> <code>${{d.check}}</code>`:""}}</p>
   <p>${{d.summary}}</p><hr style="border-color:#2a2f3a"><b>Edges</b>${{[...outs,...ins].map(eline).join("")||"<div>(none)</div>"}}`;}}
function ds(e,d){{if(!e.active)sim.alphaTarget(.3).restart();d.fx=d.x;d.fy=d.y;}}
function dg(e,d){{d.fx=e.x;d.fy=e.y;}}
function de(e,d){{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}}
</script></body></html>"""



def emit_theorems_catalog(dag):
    """Paper 9 ledger catalog. Types every node; marks exactly the nine bundled
    executable witnesses. This is NOT the 3,918-entry engine bank."""
    legend = {
        "APF_NATIVE": "Proved in Paper 9 from stated definitions/assumptions (finite mathematics).",
        "STANDARD_IMPORT": "Standard mathematical import (Sikorski/subcartesian/constant-rank/Lovelock).",
        "CONDITIONAL_THEOREM": "Conditional on an explicit gate or structural commitment.",
        "MODEL_CERTIFICATE": "Exact finite model certificate; not the general theorem.",
        "NAMED_OPEN_GATE": "Named open gate; not proved.",
        "EXTERNAL_ENDPOINT": "Imported endpoint from another APF paper (Paper 6).",
        "EXECUTABLE_WITNESS": "Bundled local check; a finite witness / falsifier control, not a symbolic proof.",
    }
    entries = []
    for n in dag["nodes"]:
        is_w = n["node_class"] == "EXECUTABLE_WITNESS"
        entries.append({
            "id": n["id"],
            "name": n.get("check", n["label"]),
            "node_class": n["node_class"],
            "status": n["status"],
            "grade": n["status"] if is_w else None,
            "bundled_in_this_repo": bool(is_w),
            "summary": n["summary"],
        })
    bundled = [e["name"] for e in entries if e["bundled_in_this_repo"]]
    cat = {
        "schema": "apf.paper9.theorem_ledger.v1",
        "paper": "Paper 9 v3.7 / Technical Supplement v1.1",
        "engine": ENGINE,
        "total_bank_registered": ENGINE["bank_size"],
        "bundled_in_this_repo": len(bundled),
        "bundled_check_names": bundled,
        "note": ("The formal claims live in the manuscript and Technical Supplement. "
                 "This catalog types every Paper 9 closure node; only the nine "
                 "executable witnesses carry a bundled local check. Conditional, open, "
                 "external, and model-certificate nodes carry no local check by design."),
        "node_class_legend": legend,
        "entries": entries,
    }
    from pathlib import Path
    import json as _j
    Path("theorems.json").write_text(_j.dumps(cat, indent=1))
    return len(bundled), len(entries)


if __name__ == "__main__":
    dag = build()
    Path("paper9_typed_dependency_dag.json").write_text(json.dumps(dag, indent=1))
    Path("interactive_dag.html").write_text(render_html(dag))
    nb, ne = emit_theorems_catalog(dag)
    print(f"theorems.json: bundled={nb} entries={ne}")
    print(f"nodes={dag['counts']['nodes']} edges={dag['counts']['edges']} "
          f"witnesses={dag['counts']['witnesses']} open_gates={dag['counts']['open_gates']}")
