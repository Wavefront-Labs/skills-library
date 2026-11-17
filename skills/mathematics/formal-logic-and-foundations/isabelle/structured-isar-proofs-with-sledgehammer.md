---
id: mathematics.formal-logic-and-foundations.isabelle.structured-isar-proofs-with-sledgehammer
name: structured-isar-proofs-with-sledgehammer
category: mathematics
field: formal-logic-and-foundations
product: isabelle
tags: [isabelle, isabelle-hol, isar, sledgehammer, nitpick, quickcheck, interactive-theorem-proving, higher-order-logic, hol, auto, simp, blast, metis, fastforce, induction, archive-of-formal-proofs, afp, jedit, formal-verification, theory-files, locales]
level: practitioner
status: draft
description: "Write readable Isabelle/HOL proofs in Isar: test conjectures with nitpick and quickcheck, structure with have/show/obtain, close steps with sledgehammer, simp and auto."
sources: ["Nipkow & Klein, Concrete Semantics (Springer 2014; free online)", "Nipkow, Programming and Proving in Isabelle/HOL (Isabelle distribution tutorial)", "Wenzel, The Isabelle/Isar Reference Manual", "Blanchette, Hammering towards QED (Journal of Formalized Reasoning, 2016)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Structured Isar proofs with Sledgehammer

**Goal:** prove a lemma in Isabelle/HOL with a structured Isar proof that a human can
read, using counterexample finders before you invest and Sledgehammer to discharge the
individual steps.

## 1. Environment
- Isabelle ships with its own IDE (Isabelle/jEdit; a VS Code front end also exists).
  Proof checking is continuous: the **Output** panel shows the goal state at the cursor,
  and purple/red highlighting marks unfinished or failed parts.
- A theory file:
  ```
  theory Scratch imports Main begin
  lemma rev_rev: "rev (rev xs) = xs"
    by (induction xs) auto
  end
  ```
  Use `HOL-Library`, `HOL-Analysis`, `HOL-Number_Theory` etc. via `imports`. The
  **Archive of Formal Proofs (AFP)** has thousands of developments — search it before
  formalising something standard.

## 2. Before proving: try to break it
- `nitpick` searches for finite countermodels; `quickcheck` tests random/exhaustive
  instances. Run them on every non-trivial conjecture — a false lemma with a missing
  hypothesis wastes far more time than the check.
- Both can report "no counterexample found", which is evidence, not proof. Nitpick may
  also report "potentially spurious" counterexamples involving infinite types.

## 3. Isar structure
```
lemma sum_upto: "(∑i≤n. i) = n * (n + 1) div (2::nat)"
proof (induction n)
  case 0
  then show ?case by simp
next
  case (Suc n)
  have "(∑i≤Suc n. i) = (∑i≤n. i) + Suc n" by simp
  also have "… = n * (n + 1) div 2 + Suc n" using Suc.IH by simp
  also have "… = Suc n * (Suc n + 1) div 2" by simp
  finally show ?case .
qed
```
Building blocks:
- `fix x` / `assume h: "P x"` / `show "Q x"` mirror "let x … suppose … then".
- `have name: "stmt"` for intermediate facts; `using`/`from` to feed facts.
- `obtain y where "P y" using h by blast` to use an existential.
- `also … finally` for calculational chains (`…` refers to the previous right-hand
  side); `moreover … ultimately` to collect facts.
- `proof (cases …)`, `proof (induction … arbitrary: …)`, `proof (rule ccontr)`.
- `?case`, `?thesis` are the current goal; `case (Suc n)` names IH as `Suc.IH`.
Generalise the induction with `arbitrary: ys` when the IH must hold for all values of
another variable — the classic fix for a "too weak" induction hypothesis.

## 4. Closing steps: the automation ladder
1. `by simp` / `by auto` — rewriting with the simpset (`simp add: foo_def`); auto adds
   classical reasoning. `by fastforce`, `by force` try harder.
2. `by blast` — pure first-order/predicate reasoning, no rewriting.
3. `by linarith` / `by presburger` / `by algebra` for arithmetic fragments; `by eval` for
   computable ground facts.
4. **`sledgehammer`** — sends the goal plus relevant library facts to external ATPs/SMT
   solvers (E, Vampire, Z3, cvc5…) and returns a proof line such as
   `by (metis foo bar)` or `by (smt (verit) …)`. Click to insert. If a one-liner is
   slow or fragile, ask for an Isar proof (`sledgehammer [isar_proofs]`) or add an
   intermediate `have`.
Keep steps small enough that each closes with one of these.

## 5. Maintainability
- Prefer `simp only:`/explicit lemma lists for steps sensitive to the simpset; global
  `[simp]` attributes on your own lemmas change behaviour everywhere downstream.
- Name lemmas meaningfully; state general versions; use locales for algebraic structure
  assumptions shared across lemmas.
- Large `metis` calls can be slow; `smt` proofs need the solver at replay time (Isabelle
  bundles them, but proof reconstruction can break across versions).

## Gotchas
- Types matter: `2::nat` vs `2::real`; `div` is truncating on nat/int; `-` on nat
  truncates at 0. Add explicit type annotations when a numeral's type is ambiguous.
- `sorry` and `oops` leave holes; the theory still "loads" with `sorry` (marked), so
  search for them before claiming a result.
- Uncertain: the sum-syntax and the exact lemmas `simp` needs in the example may differ
  between Isabelle releases; adjust if a step fails.

## Verify
- [ ] Conjecture survives `nitpick` and `quickcheck` before proving.
- [ ] Whole theory processes without errors; no `sorry`/`oops` remain.
- [ ] Each Isar step is closed by a short method call; long `metis`/`smt` lines replaced
      by smaller steps where they are slow.
- [ ] The formal statement (types, hypotheses) matches the intended informal one.
