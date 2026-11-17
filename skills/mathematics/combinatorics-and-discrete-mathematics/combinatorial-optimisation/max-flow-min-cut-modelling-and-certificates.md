---
id: mathematics.combinatorics-and-discrete-mathematics.combinatorial-optimisation.max-flow-min-cut-modelling-and-certificates
name: max-flow-min-cut-modelling-and-certificates
category: mathematics
field: combinatorics-and-discrete-mathematics
product: combinatorial-optimisation
tags: [combinatorial-optimisation, combinatorial-optimization, network-flows, max-flow, min-cut, max-flow-min-cut-theorem, ford-fulkerson, edmonds-karp, dinic, push-relabel, bipartite-matching, menger, vertex-splitting, circulations, lower-bounds, integrality, total-unimodularity, lp-duality, certificates, networkx, or-tools]
level: practitioner
status: gated
description: "Model assignment, routing and cut problems as maximum flows, solve with a library, and prove optimality with a minimum cut: vertex splitting, lower bounds, integrality and duality certificates."
sources: ["Schrijver, Combinatorial Optimization: Polyhedra and Efficiency (Springer 2003)", "Ahuja, Magnanti & Orlin, Network Flows (Prentice Hall 1993)", "Kleinberg & Tardos, Algorithm Design (2005), ch. 7"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Max-flow / min-cut: modelling and certificates

**Goal:** recognise when a discrete optimisation problem is secretly a maximum flow,
build the network correctly, and back every answer with a cut that proves it optimal.

## 1. The theorem you are exploiting
In a directed network with source s, sink t and capacities c(e) ≥ 0, the maximum s–t
flow value equals the minimum capacity of an s–t cut (a set S ∋ s, t ∉ S; capacity =
Σ c(u,v) over u ∈ S, v ∉ S). With **integer capacities there is an integral maximum
flow** — this is why flows solve combinatorial problems exactly, not just LP relaxations
(the constraint matrix is totally unimodular).

## 2. Modelling patterns
| Problem | Construction |
|---|---|
| bipartite matching | s → each left vertex (cap 1), left → right edges (cap 1), right → t (cap 1) |
| assignment with quotas | s → worker (cap = max jobs), job → t (cap = demand) |
| edge-disjoint s–t paths (Menger) | unit capacity on each edge; flow value = number of paths |
| vertex-disjoint paths / vertex capacities | **split** each v into v_in → v_out with cap = vertex capacity |
| undirected edges | replace by two opposite arcs, each with the edge capacity |
| several sources/sinks | super-source → each source, each sink → super-sink |
| project selection / closure (profit vs prerequisites) | s → project (profit), cost item → t (cost), dependencies ∞; answer = Σ profits − min cut |
| image segmentation, min-cost labelling with pairwise terms | s/t edges for unary costs, neighbour edges for pairwise costs (graph cuts) |
| lower bounds ℓ(e) ≤ f(e) | circulation with demands: shift ℓ out, adjust node balances, check feasibility with one max-flow |
Infinite capacities: use a number larger than any finite cut (e.g. sum of all finite
capacities + 1), not floating `inf`, unless the library explicitly supports it.

## 3. Solving
- NetworkX: `nx.maximum_flow(G, s, t, capacity="capacity")` and `nx.minimum_cut(...)`
  (returns the value and the partition (S, T)). Fine up to ~10⁵ edges in practice.
- Faster: Google OR-Tools `SimpleMaxFlow` / `SimpleMinCostFlow`, LEMON, Boost Graph
  Library (push–relabel, Boykov–Kolmogorov for vision graphs).
- Algorithms to know by name: Edmonds–Karp O(VE²) (BFS augmenting paths), Dinic
  O(V²E) and O(E√V) on unit bipartite graphs (≈ Hopcroft–Karp), push–relabel
  O(V²√E) with heuristics — fastest in practice for dense problems.
- Costs as well as capacities → **min-cost flow** (assignment with costs, transportation
  problems); still integral with integer data.

## 4. Certificates (what makes an answer trustworthy)
- **Flow feasibility:** every arc 0 ≤ f ≤ c; conservation at every node except s, t.
- **Optimality:** exhibit the cut (S, T) from the final residual graph (S = vertices
  reachable from s). Its capacity must equal the flow value. Check this independently of
  the solver — it is a few lines of code.
- In applications, translate the cut back: for bipartite matching, the cut yields a
  minimum vertex cover (König); for project selection, S is the optimal project set;
  for disjoint paths, the cut is a minimum separating set.

## 5. When it is *not* a flow
Flows handle one commodity with conservation. Multi-commodity flow (different goods
sharing capacity) is an LP and integer versions are NP-hard. Matchings in **non-bipartite**
graphs need Edmonds' blossom algorithm (`nx.max_weight_matching`), not a flow. Problems
with "at most k of these sets" or general side constraints usually need integer
programming; recognise them before forcing a flow model.

## Gotchas
- Forgetting to split vertices when the constraint is on vertices, not edges.
- Using an undirected NetworkX `Graph` for a directed model (or vice versa) changes
  the meaning of capacities.
- Floating-point capacities lose the integrality guarantee and can make some
  augmenting-path methods misbehave; scale to integers.
- Complexity bounds, the practical-speed ranking and the ~10⁵-edge NetworkX figure are (gated: unconfirmed, source is paywalled or blocked); benchmark on your instance sizes. NetworkX maximum_flow/minimum_cut/max_weight_matching and OR-Tools SimpleMaxFlow names were confirmed by running them; a toy network gave flow 5 with cut ({s,a,b},{t}) of capacity 5.

## Verify
- [ ] Every modelling constraint maps to a capacity, a node split or a demand.
- [ ] Flow is integral when capacities are integral; conservation checked.
- [ ] Min-cut capacity computed independently equals the flow value.
- [ ] Cut translated back into a meaningful certificate in the original problem.
