---
id: mathematics.formal-logic-and-foundations.lean-prover.proving-theorems-with-lean4-and-mathlib
name: proving-theorems-with-lean4-and-mathlib
category: mathematics
field: formal-logic-and-foundations
product: lean-prover
tags: [lean-prover, lean, lean4, mathlib, interactive-theorem-proving, formalisation, formal-verification, tactics, simp, rw, linarith, ring, omega, norm-num, apply-question, lake, loogle, sorry, type-theory, dependent-types, coercions, vs-code]
level: practitioner
status: docs-checked
description: "Formalise and prove a lemma in Lean 4 with Mathlib: project setup, finding library lemmas, the core tactic toolkit, natural-number subtraction pitfalls, and keeping proofs robust."
sources:
  - https://leanprover-community.github.io/install/project.html
  - https://leanprover-community.github.io/mathematics_in_lean/C02_Basics.html
  - https://leanprover-community.github.io/mathematics_in_lean/C03_Logic.html
  - https://leanprover-community.github.io/mathematics_in_lean/C05_Elementary_Number_Theory.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proving theorems with Lean 4 and Mathlib

**Goal:** state a mathematical result in Lean 4, prove it using Mathlib, and finish
with no `sorry`, by leaning on search and automation instead of re-proving the library.

## 1. Setup
- Follow the Lean community "project" install page. A new project depending on Mathlib is
  made with `lake new my_project math` (the page shows a version-pinned form,
  `lake +v4.24.0 new my_project math`), then `lake update` inside the folder.
- Run `lake exe cache get` to fetch prebuilt Mathlib files instead of compiling Mathlib.
- The `lean-toolchain` file pins the Lean version; update it together with Mathlib.
  Code from older tutorials may use renamed lemmas.
- Use VS Code; the **Infoview** panel shows the goal state at the cursor.

## 2. Stating things
```lean
example (x y : ℝ) (h : x ≤ y) : x + 1 ≤ y + 1 := by
  linarith

example (a b : ℕ) (h : a ≤ b) : a + 1 ≤ b + 1 := by
  omega
```
`theorem` names a result, `example` is anonymous. Hypotheses are arguments `(h : P)`.

## 3. Finding the lemma you need
- `apply?` suggests a lemma for the goal; Mathematics in Lean also points to Loogle for
  searching the library.
- Check the current Mathlib documentation for other search tools and naming conventions;
  they change over time.

## 4. The core tactic toolkit
| Situation | Tactic |
|---|---|
| goal `∀ x, ...` / `P → Q` | `intro x` / `intro h` |
| goal `∃ x, P x` | `use 3` |
| hypothesis `∃`/`∧` | `obtain ⟨x, hx⟩ := h` |
| goal `P ∧ Q` / `P ↔ Q` | `constructor` |
| case split | `rcases h with h1 \| h2`, `by_cases h : P` |
| rewrite with an equation | `rw [lemma]` |
| ring identities | `ring`, `group`, `abel` |
| linear inequalities | `linarith` |
| naturals/integers | `omega` |
| numerals | `norm_num` |
| rewriting/simplifying | `simp` |
| finite decidable goals | `decide` |
| induction | `induction n with \| zero => ... \| succ n ih => ...` |
| contradiction | `by_contra h`, `exfalso`, `contradiction` |
Structure longer proofs with `have` and `calc` chains; they read like paper proofs.

## 5. Pitfalls
- **Natural subtraction truncates:** Mathematics in Lean notes that truncated subtraction
  cuts off at zero, so `2 - 5 = 0` in ℕ. Carry hypotheses `b ≤ a` or work in ℤ.
- `(n : ℝ)` and `n` are different terms; casts need explicit handling. Look up the cast
  tactics in the current Mathlib documentation.

## 6. Workflow
Write the skeleton with `sorry` for each step, check the overall structure compiles,
then fill sorries one by one. Ask the Lean community with a minimal working example.

## Gotchas
- Lean 3 syntax does not work in Lean 4.
- Tactic names change between Mathlib versions; check the docs for your pinned version.

## Verify
- [ ] The project builds with no errors.
- [ ] No `sorry`, `admit` or new `axiom`.
- [ ] The Lean statement means what the informal statement means (types, casts,
      ℕ vs ℝ, edge cases).

## Checked
2026-11-01. Confirmed in the Lean community project page: `lake new ... math`,
`lake update`, `lake exe cache get`, the `lean-toolchain` file, Infoview. Confirmed in
Mathematics in Lean chapters 2, 3 and 5: rw, ring, linarith, norm_num, constructor, apply?,
calc, have, abel, group, intro, use, obtain, rcases, by_cases, by_contra, exfalso,
contradiction, omega, simp, decide, induction, truncated subtraction, sorry, Loogle.
Removed: nlinarith, positivity, field_simp, push_neg (absent or renamed in the pages),
aesop, tauto, norm_cast family, exact?, rw?, Moogle, LeanSearch, naming-convention rules,
`lake build`, lake-manifest and `#print axioms` details, the 'import Mathlib' claim and
other unconfirmed specifics.
Method: documentation only; no commands were run.
