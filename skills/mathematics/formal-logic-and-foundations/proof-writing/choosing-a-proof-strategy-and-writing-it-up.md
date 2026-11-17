---
id: mathematics.formal-logic-and-foundations.proof-writing.choosing-a-proof-strategy-and-writing-it-up
name: choosing-a-proof-strategy-and-writing-it-up
category: mathematics
field: formal-logic-and-foundations
product: proof-writing
tags: [proof-writing, mathematical-proof, proof-strategies, direct-proof, contrapositive, proof-by-contradiction, induction, strong-induction, counterexample, cases, existence-proof, uniqueness, if-and-only-if, epsilon-delta, mathematical-writing, rigour, exposition, polya, homework, latex]
level: intro
status: draft
description: "From statement to checkable proof: unpack definitions, hunt counterexamples, pick direct, contrapositive, contradiction, induction or cases, and write it up so every step can be verified."
sources: ["Velleman, How to Prove It (3rd ed., CUP 2019)", "Pólya, How to Solve It (1945)", "Hammack, Book of Proof (3rd ed., open textbook)", "Halmos, How to Write Mathematics (1970)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a proof strategy and writing it up

**Goal:** turn "prove that …" into a proof that is correct and that another person can
verify line by line — without staring at a blank page.

## 1. Before proving: read and test the statement
1. **Identify the logical shape.** Rewrite with explicit quantifiers and connectives:
   "∀n ∈ ℕ, (n² even → n even)". The shape dictates the opening of the proof.
2. **Unpack every definition** into its formal content. "n is even" → "∃k ∈ ℤ, n = 2k".
   Most beginner proofs stall because a definition was never written down.
3. **Try small cases and look for a counterexample.** If the statement is false you
   save hours; if it is true, the cases show *why*. For "∀" claims, test the boundary
   (0, 1, empty set, constant function, n = 2).
4. **Draw a picture** for geometry, analysis (graph the function, mark ε and δ),
   and combinatorics (small configurations).

## 2. Pick the strategy from the shape
| Goal shape | Opening move |
|---|---|
| P → Q | Direct: assume P, derive Q. If P is weak and ¬Q gives something concrete, **contrapositive**: assume ¬Q, derive ¬P. |
| P ↔ Q | Two directions, labelled (⇒) and (⇐). |
| ∀x P(x) | "Let x be arbitrary." Then prove P(x) with no extra assumptions about x. |
| ∃x P(x) | Construct (or bound) a witness, then *verify* it satisfies P. |
| ∃! x | Existence, then uniqueness: suppose x and y both work, show x = y. |
| ∀n ≥ n₀ (integers) | Induction: base case, then assume P(n) (or all P(k), k ≤ n — strong induction), derive P(n+1). |
| ¬P, "there is no…", irrationality, infinitude | Contradiction: assume P, derive a falsehood. |
| A = B (sets) | Double inclusion: x ∈ A ⇒ x ∈ B and back. |
| statement splits naturally | Cases — make sure they are exhaustive (n even / odd; x ≥ 0 / x < 0). |

Use contradiction sparingly: if the "contradiction" proof just proves the contrapositive
and then contradicts the assumption, rewrite it as a contrapositive — it is clearer.

## 3. Working the middle
- Work forwards from hypotheses and backwards from the goal ("to show Q it suffices to
  show R"), until the chains meet. Keep the backward chain on scratch paper.
- Ask: where is each hypothesis used? An unused hypothesis means either it is
  unnecessary (check with a counterexample when it fails) or your proof has a gap.
- Look for a known theorem whose conclusion looks like your goal.
- Analysis (ε–δ): find δ on scratch paper by working backwards from |f(x) − L| < ε,
  then write the proof forwards starting with "Let ε > 0. Set δ = …".

## 4. Writing it up
- State what you are proving and the method: "We prove the contrapositive."
- Introduce every symbol before using it ("Let k ∈ ℤ be such that n = 2k").
- Write full sentences; symbols are nouns and verbs inside them. "∴" and arrows between
  lines hide the logic — say "hence", "since", "by Lemma 2".
- One idea per paragraph; isolate reusable steps as lemmas.
- Justify each non-trivial step with a reason, and only the non-trivial ones.
- End by connecting back to the statement: "Hence n is even, as required."
- In LaTeX use `amsthm` environments (`theorem`, `proof`); `\qedhere` when a proof ends
  in a display.

## Gotchas
- **Proving the converse** by accident (assuming Q, deriving P). Check the direction.
- **Choosing x specifically** in a ∀ proof ("let n = 4"). Examples are not proofs of
  universal statements — but one counterexample *disproves* one.
- Induction step that silently fails at the smallest case (the "all horses are the same
  colour" bug): check the step works for n = n₀.
- Dividing by something that could be zero; taking square roots of possibly negative
  quantities; "WLOG" without a symmetry that actually justifies it.
- Circularity: using the result (or an equivalent) inside its own proof.

## Verify
- [ ] Statement rewritten with explicit quantifiers; definitions unpacked.
- [ ] Small cases tested; no counterexample found (or the claim corrected).
- [ ] Every hypothesis is used, or its irrelevance explained.
- [ ] Every variable introduced; every non-obvious step justified.
- [ ] A reader who knows only the definitions could check it without asking you.
