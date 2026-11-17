---
id: mind-self.critical-thinking-and-argumentation.informal-logic.reconstructing-hidden-premises
name: reconstructing-hidden-premises
category: mind-self
field: critical-thinking-and-argumentation
product: informal-logic
tags: [informal-logic, logic, validity, soundness, deduction, induction, inductive-strength, enthymeme, hidden-premise, missing-premise, counterexample-method, standard-form, argument-forms, modus-ponens, modus-tollens, affirming-the-consequent, denying-the-antecedent, principle-of-charity, critical-thinking]
level: practitioner
status: draft
description: "Put everyday reasoning in standard form, supply the missing premise charitably, then test validity with counterexamples and judge soundness or inductive strength."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reconstructing hidden premises — standard form, validity, soundness

**Goal:** take an everyday argument ("we shouldn't hire him, he's never managed a team")
and decide, step by step, whether its reasoning is good — separating *does it follow*
from *is it true*.

## 1. Put it in standard form
Number the premises, draw a line, write the conclusion:
```
P1. He has never managed a team.
----
C.  We should not hire him for this role.
```
Drop repetition, rhetoric and side remarks. Keep the claims that actually do work.

## 2. Supply the missing premise (enthymeme)
Ask: *what would have to be true for P1 to guarantee C?* Write the general rule:
```
P2. (hidden) We should not hire anyone for this role who has never managed a team.
```
**Principle of charity:** choose the most plausible premise that makes the argument
work, not the most extreme one. "Management experience is a strong advantage here" is
more charitable than "only ex-managers are competent" — but it also makes the argument
weaker (inductive, not deductive). Note which version you chose.

## 3. Valid? — the counterexample method
An argument is **valid** if it is impossible for all premises to be true and the
conclusion false. Test it: try to imagine a case where every premise holds and the
conclusion fails. If you can, it's invalid.
- Common valid forms: *modus ponens* (If A then B; A; so B), *modus tollens*
  (If A then B; not B; so not A), disjunctive syllogism (A or B; not A; so B).
- Common invalid look-alikes: *affirming the consequent* (If A then B; B; so A) and
  *denying the antecedent* (If A then B; not A; so not B). "If it rained, the street is
  wet. The street is wet. So it rained." — counterexample: a street cleaner.
- Swap in nonsense terms with the same shape; if the form produces a true-premise,
  false-conclusion instance, the form is invalid.

## 4. Sound? — are the premises true
**Sound** = valid + all premises true. Most real disputes are here, not in the logic.
The hidden premise is usually the one to challenge.

## 5. Inductive arguments: strength, not validity
Arguments from samples, analogies, or causes are never valid in the strict sense; ask
how *strong* they are:
- **Sample:** large enough? representative? (a survey of one office ≠ all staff).
- **Analogy:** are the two cases alike in the respects that matter here?
- **Cause:** is there a mechanism, a comparison group, and alternative explanations ruled out?
Strength comes in degrees — say "moderately strong" rather than forcing yes/no.

## Gotchas
- **Valid ≠ true.** "All fish fly; salmon are fish; so salmon fly" is valid and unsound.
- **Invalid ≠ false conclusion.** The conclusion may be true for other reasons.
- **Uncharitable reconstruction** turns into a straw man (see fallacy-recognition).
- **Two-claim conclusions** ("we should cut X and fund Y") are two arguments.
- Formal-logic notation is optional here; this is the practical skill. For a philosophy-
  method treatment see religion-philosophy.western-philosophy.argumentation-and-philosophical-method.reconstructing-and-critiquing-an-argument.

## Verify
- [ ] Premises and conclusion are numbered and separated.
- [ ] A hidden premise is written down and is the most charitable workable version.
- [ ] You tried to construct a counterexample before calling it valid.
- [ ] You judged truth of premises separately from validity.
- [ ] For inductive arguments, you rated strength and named the main alternative explanation.
