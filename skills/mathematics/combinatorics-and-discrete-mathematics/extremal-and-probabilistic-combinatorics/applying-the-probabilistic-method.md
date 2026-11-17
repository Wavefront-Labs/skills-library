---
id: mathematics.combinatorics-and-discrete-mathematics.extremal-and-probabilistic-combinatorics.applying-the-probabilistic-method
name: applying-the-probabilistic-method
category: mathematics
field: combinatorics-and-discrete-mathematics
product: extremal-and-probabilistic-combinatorics
tags: [extremal-and-probabilistic-combinatorics, probabilistic-method, first-moment-method, linearity-of-expectation, union-bound, alteration-method, deletion-method, second-moment-method, chebyshev, lovasz-local-lemma, ramsey-numbers, ramsey-theory, random-graphs, erdos-renyi, extremal-graph-theory, turan, chernoff-bounds, existence-proof, derandomisation]
level: advanced
status: draft
description: "Prove a combinatorial object exists by choosing it at random: first-moment and union bounds, alterations, second moment, Lovász Local Lemma, and Ramsey-type lower bounds with worked numbers."
sources: ["Alon & Spencer, The Probabilistic Method (4th ed., Wiley 2016)", "Molloy & Reed, Graph Colouring and the Probabilistic Method (Springer 2002)", "Zhao, Graph Theory and Additive Combinatorics (CUP 2023)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Applying the probabilistic method

**Goal:** show that an object with property P exists by defining a random object and
proving Pr[P] > 0 — often the only known way to get good lower bounds in extremal
combinatorics.

## 1. The core logic
If a random object has P with positive probability, some object has P. If a random
variable X satisfies E[X] ≤ t, some outcome has X ≤ t (and some has X ≥ t). That's all —
the art is choosing the distribution and the bad events.

## 2. Union bound / first moment (the workhorse)
Write "not P" as a union of bad events B_1…B_m. If Σ Pr[B_i] < 1, then Pr[P] > 0.

**Ramsey lower bound (Erdős 1947).** Colour each edge of K_n red/blue independently with
probability 1/2. For each k-set S, Pr[S monochromatic] = 2^{1 − (k choose 2)}. If
(n choose k)·2^{1 − (k choose 2)} < 1, some colouring has no monochromatic K_k, so
R(k, k) > n. This holds for n = ⌊2^{k/2}⌋ when k ≥ 3, giving R(k, k) > 2^{k/2}.
Plug in numbers for a specific k to check: the inequality, not the asymptotic slogan, is
the proof.

## 3. Alterations (delete the bad parts)
When the union bound fails, accept some bad configurations and remove them.
Example — graphs with no short cycles and large chromatic number, or the simpler
**independent set bound**: pick each vertex with probability p; let X = number chosen,
Y = number of edges with both ends chosen. E[X − Y] = pn − p²|E|. Delete one endpoint
per bad edge: the result is independent with expected size ≥ pn − p²|E|; optimise p
(p = n/(2|E|)) to get α(G) ≥ n²/(4|E|).
Ramsey via alteration improves the constant: R(k, k) > n − (n choose k)2^{1−(k choose 2)}
for every n.

## 4. Second moment (show something *does* occur)
For a count X ≥ 0, Pr[X = 0] ≤ Var(X)/E[X]² (Chebyshev). If Var(X) = o(E[X]²),
then X > 0 with high probability. Compute Var(X) = Σ Pr[A_i] + Σ_{i≠j} (Pr[A_i ∧ A_j]
− Pr[A_i]Pr[A_j]) — only dependent pairs contribute. This is how thresholds in random
graphs G(n, p) are proved (e.g. appearance of a fixed subgraph, triangles at
p ≫ 1/n).

## 5. Lovász Local Lemma (rare, mostly independent bad events)
If each bad event has Pr ≤ p, depends on at most d others, and e·p·(d + 1) ≤ 1, then
with positive probability **no** bad event occurs — even when Σ Pr[B_i] ≫ 1.
Use it for k-SAT with bounded variable occurrences, colourings of hypergraphs
(property B), and Ramsey lower bounds with better constants. Moser–Tardos resampling
makes many LLL applications algorithmic.

## 6. Concentration
Chernoff/Hoeffding bounds for sums of independent indicators,
Pr[|X − μ| ≥ δμ] ≤ 2e^{−δ²μ/3} for 0 < δ ≤ 1 (one common form); Azuma/McDiarmid for
functions with bounded differences. Use them to make "most" choices good at once,
then a union bound over polynomially many events.

## 7. Extremal companions
Results like Turán's theorem (max edges with no K_{r+1}, attained by the balanced
complete r-partite graph) and Kővári–Sós–Turán are proved by counting/convexity, but
probabilistic constructions supply the matching lower bounds (random graphs with
deletions). Pair upper bounds by double counting with lower bounds by randomness.

## Gotchas
- Pr > 0 gives existence only — not a construction. Say so; derandomise (conditional
  expectations) only if you need an explicit object.
- Check independence assumptions: edges of a random colouring are independent, but
  events about overlapping k-sets are not (fine for union bound and expectation, not for
  multiplying probabilities).
- Asymptotic "≈" steps hide constants; verify the inequality for the specific
  parameters claimed.
- Uncertain: several constants (Chernoff forms, LLL symmetric condition e·p·(d+1) ≤ 1
  vs 4pd ≤ 1) appear in different versions; cite the version you use.

## Verify
- [ ] Probability space defined explicitly (what is random, with what distribution).
- [ ] Bad events listed; their probabilities computed exactly, then bounded.
- [ ] The final inequality checked numerically for the claimed parameters.
- [ ] Dependence handled correctly for the tool used (union bound, second moment, LLL).
