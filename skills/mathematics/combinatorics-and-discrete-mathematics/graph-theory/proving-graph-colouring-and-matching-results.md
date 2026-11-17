---
id: mathematics.combinatorics-and-discrete-mathematics.graph-theory.proving-graph-colouring-and-matching-results
name: proving-graph-colouring-and-matching-results
category: mathematics
field: combinatorics-and-discrete-mathematics
product: graph-theory
tags: [graph-theory, graph-colouring, graph-coloring, chromatic-number, greedy-colouring, brooks-theorem, four-colour-theorem, planar-graphs, euler-formula, matchings, halls-theorem, konigs-theorem, tuttes-theorem, bipartite-graphs, augmenting-paths, degeneracy, extremal-counterexample, minimal-counterexample, handshake-lemma, networkx]
level: practitioner
status: docs-checked
description: "Prove graph colouring, matching and planarity results: degree counting, greedy and degeneracy bounds, minimal counterexamples, Hall, König, Tutte and Euler."
sources: ["https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.coloring.greedy_color.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proving graph colouring and matching results

**Goal:** prove (or refute) a statement about colourings, matchings or planarity with
the handful of techniques that do most of the work in graph theory.

## 1. Pin down the definitions
State: simple graph or multigraph? loops? finite? connected? directed? "Colouring" =
proper vertex colouring unless stated (adjacent vertices differ); edge colouring and
list colouring are different problems. Many "counterexamples" come from mismatched
conventions.

## 2. Universal tools
- **Handshake lemma:** Σ deg(v) = 2|E|. Hence an even number of odd-degree vertices;
  average degree 2|E|/|V|.
- **Pigeonhole on degrees:** some vertex has degree ≤ average; this seeds inductions.
- **Minimal counterexample:** assume a counterexample with the fewest vertices (or
  edges). Delete a well-chosen vertex/edge, apply the statement to the smaller graph,
  and extend back. The structure you derive about the minimal counterexample (min
  degree, connectivity) is usually the proof.
- **Extremal choice:** take a longest path, a maximum matching, a spanning tree — its
  maximality gives structure (e.g. endpoints of a longest path have all neighbours on
  the path).

## 3. Colouring techniques
- **Greedy:** colour vertices in any order with the smallest free colour ⇒ χ(G) ≤ Δ + 1.
  Order matters: if G is **d-degenerate** (every subgraph has a vertex of degree ≤ d),
  colour in reverse of a min-degree elimination order ⇒ χ ≤ d + 1.
- **Planar graphs:** Euler's formula V − E + F = 2 (connected, plane) ⇒ E ≤ 3V − 6 for
  V ≥ 3 ⇒ a vertex of degree ≤ 5 ⇒ 5-degenerate ⇒ χ ≤ 6 by greedy. The 5-colour
  theorem adds a Kempe-chain swap at a degree-5 vertex. The four-colour theorem is
  computer-assisted; cite it, don't reprove it.
- **Brooks' theorem:** χ ≤ Δ for connected G unless G is complete or an odd cycle.
- **Lower bounds:** χ ≥ ω (clique number), χ ≥ |V|/α (independence number). Odd cycles
  need 3 colours; a graph is 2-colourable iff it has no odd cycle (bipartite).
- Mycielski's construction shows χ can be large with ω = 2, so clique bounds can be
  far from tight.

## 4. Matchings
- **Augmenting paths (Berge):** a matching is maximum iff no augmenting path exists. To
  prove maximality, show none exists; to improve, find one.
- **Hall's theorem** (bipartite, sides X, Y): a matching saturating X exists iff
  |N(S)| ≥ |S| for every S ⊆ X. To prove a matching exists, verify Hall's condition
  (often via a degree/counting argument: if every vertex in X has degree ≥ d and every
  vertex in Y degree ≤ d, the condition holds — e.g. regular bipartite graphs have
  perfect matchings).
- **König:** in bipartite graphs, max matching = min vertex cover. Exhibiting both a
  matching and a cover of the same size certifies optimality.
- **Tutte:** G has a perfect matching iff for all S, the number of odd components of
  G − S is ≤ |S|. Use the violating S as a certificate of *no* perfect matching.

## 5. Small-case checking with software
Test conjectures on all small graphs before proving: NetworkX
(`nx.greedy_color`, `nx.max_weight_matching`, `nx.check_planarity`,
`nx.graph_atlas_g()` gives all 1253 graphs up to 7 vertices). Petersen graph, odd cycles, K₄, K₃,₃ and K₅
are the first things to test against.

## Gotchas
- Induction by *adding* a vertex to a smaller graph ("build-up error") may miss graphs
  not obtainable that way; induct by *removing* from an arbitrary graph instead.
- Deleting a vertex may disconnect the graph; check the hypothesis (connectivity, min
  degree) survives in the smaller instance.
- Euler's formula needs a connected plane embedding; for c components it is
  V − E + F = 1 + c.
- NetworkX function names and defaults can change between versions; check the docs for the installed release.

## Checked
2026-11-01. The four NetworkX functions exist in NetworkX 3.7 and `graph_atlas_g()` returns 1253 graphs with at most 7 nodes (computed); greedy_color is documented on the NetworkX page. The theorem statements (handshake, greedy and degeneracy bound, Euler, Brooks, Berge, Hall, Konig, Tutte) are standard results and were not re-derived here. Removed: SageMath and House of Graphs tool claims (not checked).

Method: documentation plus short Python computations; the skill's own commands were not run.

## Verify
- [ ] Graph conventions (simple, finite, connected) stated.
- [ ] Claim tested on all graphs up to ~7 vertices and on the named small examples.
- [ ] Inductive/minimal-counterexample step keeps all hypotheses in the smaller graph.
- [ ] Optimality claims come with a matching certificate (cover, Hall violator, Tutte set).
