---
id: languages-linguistics.linguistics.semantics-pragmatics.entailment-implicature-and-presupposition-tests
name: entailment-implicature-and-presupposition-tests
category: languages-linguistics
field: linguistics
product: semantics-pragmatics
tags: [semantics-pragmatics, semantics, pragmatics, entailment, implicature, conversational-implicature, scalar-implicature, grice, cooperative-principle, maxims, cancellability, presupposition, projection, family-of-sentences, presupposition-triggers, speech-acts, austin, searle, felicity-conditions, compositional-semantics, truth-conditions, ambiguity, vagueness]
level: practitioner
status: draft
description: "Tell entailment, implicature and presupposition apart with standard diagnostics (cancellation, reinforcement, projection), test ambiguity vs vagueness, and analyse speech acts by felicity conditions."
sources: ["Grice, Logic and Conversation (1975)", "Levinson, Pragmatics", "Kearns, Semantics", "Potts, lecture notes on presupposition and implicature"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entailment, implicature and presupposition — the diagnostics

**Goal:** given a sentence and an inference people draw from it, classify the
inference correctly and defend the classification with tests — the core move in
semantics and pragmatics analysis.

## 1. The three kinds of inference
- **Entailment** (semantic): if *S* is true, *P* must be true. "Kim killed the
  spider" ⊨ "The spider died."
- **Conversational implicature** (pragmatic): *P* follows from assuming the speaker
  is cooperative. "Some students passed" +> "not all passed."
- **Presupposition**: *P* is taken for granted as background. "Kim stopped smoking"
  presupposes "Kim used to smoke."

## 2. Diagnostics
| Test | Entailment | Implicature | Presupposition |
|---|---|---|---|
| **Cancel it** ("…, in fact all did") | contradiction | fine | usually odd (but can be cancelled in special contexts) |
| **Reinforce it** ("some, but not all") | redundant | not redundant | redundant-ish |
| **Embed under negation/question/conditional/modal** ("family of sentences") | disappears | often disappears | **survives (projects)** |
Run all three; one test alone misleads.

Family-of-sentences example: "Kim stopped smoking." / "Kim didn't stop smoking." /
"Did Kim stop smoking?" / "If Kim stopped smoking, …" — "Kim used to smoke" survives
all → presupposition.

## 3. Implicature in detail (Gricean)
- Maxims: **Quantity** (as informative as required, not more), **Quality** (true,
  evidenced), **Relation** (relevant), **Manner** (clear, brief, orderly).
- **Scalar implicatures:** a weaker term on a scale implicates the negation of the
  stronger: ⟨some, most, all⟩, ⟨possible, likely, certain⟩, ⟨warm, hot⟩.
- **Generalised vs particularised:** generalised arise by default ("some" → not all);
  particularised need a specific context ("Is there petrol?" "There's a garage round
  the corner" → it's open and sells petrol).
- **Conventional implicatures** ("but" contrasts, "even") aren't cancellable and
  aren't truth-conditional — a fourth category; mention it when relevant.

## 4. Presupposition triggers to recognise
Definite descriptions (*the king of France*), factive verbs (*know, regret, realise*),
change-of-state verbs (*stop, start, continue*), iteratives (*again, too*), clefts (*it
was Kim who…*), temporal clauses (*before/after X*), counterfactuals.
**Gotcha:** projection can be blocked ("If Kim used to smoke, Kim stopped") —
filtering and local accommodation are where analyses get subtle.

## 5. Ambiguity vs vagueness
- **Ambiguous** (two distinct meanings): "bank", "visiting relatives can be boring".
- **Test:** ellipsis/identity — "Kim went to the bank and so did Lee" can't mix
  readings (riverbank for one, finance for the other) if truly ambiguous.
- **Vague** ("tall", "near") is one meaning with fuzzy boundaries; the test allows
  mixed interpretations.
- Distinguish **lexical** from **structural** ambiguity and **scope** ambiguity
  ("Every student read a book": one book or many?).

## 6. Speech acts
- Locution (what's said), illocution (the act: promise, request, warning),
  perlocution (effect achieved).
- **Felicity conditions** (Searle): preparatory, sincerity, essential conditions.
  Analyse an indirect request ("Can you pass the salt?") by which condition it
  questions (hearer's ability).
- **Performative test:** insert "hereby" — "I hereby promise…" works; "I hereby
  convince you…" doesn't (convincing is perlocutionary).

## 7. Compositional semantics (pointer)
For truth-conditional analysis: give each word a type and denotation, combine by
function application; state truth conditions as "*S* is true iff …". Check each
proposed denotation against entailment data from §2.

## Verify
- [ ] Every inference you classify was run through cancellation, reinforcement and embedding.
- [ ] Presupposition claims cite the trigger.
- [ ] Implicature claims name the maxim or scale involved.
- [ ] Ambiguity claims pass the identity/ellipsis test.
- [ ] Speech-act analysis names the felicity condition at stake.

*Uncertainty:* cancellability of presuppositions is contested in the literature; present
it as a tendency.
