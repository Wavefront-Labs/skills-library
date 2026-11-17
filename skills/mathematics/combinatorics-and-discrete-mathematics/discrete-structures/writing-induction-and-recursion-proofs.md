---
id: mathematics.combinatorics-and-discrete-mathematics.discrete-structures.writing-induction-and-recursion-proofs
name: writing-induction-and-recursion-proofs
category: mathematics
field: combinatorics-and-discrete-mathematics
product: discrete-structures
tags: [discrete-structures, discrete-mathematics, mathematical-induction, strong-induction, structural-induction, well-founded-induction, well-ordering-principle, recursion, recursive-definitions, loop-invariants, strengthening-the-hypothesis, partial-orders, posets, trees, recurrences, program-correctness, termination, base-case, inductive-step]
level: intro
status: draft
description: "Write correct induction proofs: ordinary, strong, structural and well-founded induction, choosing and strengthening the hypothesis, base cases, and proofs about recursively defined objects."
sources: ["Lehman, Leighton & Meyer, Mathematics for Computer Science (MIT OCW, 2017)", "Rosen, Discrete Mathematics and Its Applications (8th ed., 2018)", "Velleman, How to Prove It (3rd ed.), ch. 6"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing induction and recursion proofs

**Goal:** prove statements about every natural number, every tree, every string or every
run of a loop with an induction that is valid — right variable, right hypothesis, right
base cases.

## 1. Choose the kind of induction from the object
| Object | Induction |
|---|---|
| P(n) where P(n+1) uses only P(n) | ordinary (weak) |
| P(n) uses some earlier P(k) (e.g. factorisation into primes, n = a·b) | strong: assume P(k) for all n₀ ≤ k ≤ n |
| recursively defined sets (trees, formulas, lists, strings) | structural: base constructors, then each constructor preserves P |
| pairs, lexicographic order, terms of a rewriting system | well-founded induction on a well-founded order |
| "there is no smallest counterexample" | well-ordering principle (minimal counterexample) — equivalent to strong induction |

## 2. The template (ordinary induction)
1. **State P(n) explicitly** as a sentence with n free: "P(n): Σ_{i=1}^{n} i = n(n+1)/2."
2. **Base case** n = n₀: verify directly — computing both sides, not "trivially".
3. **Inductive step:** "Let n ≥ n₀ and assume P(n)." Derive P(n+1), and *mark the line
   where the hypothesis is used*.
4. **Conclude:** "By induction, P(n) holds for all n ≥ n₀."
For strong induction with a recursion reaching back k steps (e.g. a_n = a_{n−1} +
a_{n−2}), you need **k base cases**.

## 3. When the step won't go through: strengthen the hypothesis
Often P(n) is too weak to imply P(n+1) but a stronger Q(n) is self-sustaining.
- Classic: "Σ 1/i² < 2" fails as an induction; "Σ_{i≤n} 1/i² ≤ 2 − 1/n" goes through.
- Tiling a 2ⁿ×2ⁿ board minus one square with L-trominoes: strengthen to "minus *any*
  square".
- Loop invariants are the programming version: the invariant must be strong enough to
  imply the postcondition at exit *and* preserved by each iteration.
If you find yourself needing information about the n-case that P(n) doesn't give,
add that information to P.

## 4. Structural induction and recursive definitions
For a set defined by constructors — e.g. binary trees: `leaf`, or `node(L, R)` —
prove P(leaf), then assume P(L), P(R) and prove P(node(L, R)). Example: in every
binary tree, #leaves = #internal nodes + 1. No "n" needed; inducting on height or
size also works but is clumsier.

Recursive *functions* need two checks: **well-definedness/termination** (each recursive
call is on something smaller in a well-founded order — e.g. Ackermann terminates by
lexicographic order on (m, n)) and **correctness** (induction along that same order).

## 5. Recurrences
To show a closed form for a recurrence, induct using the recurrence as the step. To
find the closed form first: unroll a few terms, guess, then prove — or use the
characteristic polynomial / generating functions (see
mathematics.combinatorics-and-discrete-mathematics.enumerative-combinatorics.counting-with-generating-functions).
For inequalities like T(n) ≤ c·n log n (divide-and-conquer), pick c in the proof and
check base cases for small n separately — the "substitution method" fails if you
guess T(n) ≤ cn and then "prove" T(n) ≤ cn + 1.

## Gotchas
- **The build-up/size mismatch:** the step must handle an *arbitrary* object of size
  n+1, not just ones built from a particular size-n object.
- **Hidden base-case failure:** the "all horses are one colour" argument fails because
  the step from n = 1 to 2 uses an overlap that doesn't exist. Check the step for the
  smallest n.
- Inducting on the wrong variable in multi-variable statements; fix the others first
  ("for all m, induct on n") or induct on a combined measure.
- Asymptotic notation inside the hypothesis ("T(n) = O(n)") is not a fixed statement —
  induct on explicit constants.
- Uncertain: naming conventions ("complete" vs "strong" vs "course-of-values"
  induction) vary by textbook; the logic is identical.

## Verify
- [ ] P(n) written out as a full sentence.
- [ ] Enough base cases for how far back the step reaches; each computed.
- [ ] The step works for an arbitrary object of the next size, including the smallest.
- [ ] The line using the inductive hypothesis is identifiable.
- [ ] For recursive definitions: termination argued via a well-founded measure.
