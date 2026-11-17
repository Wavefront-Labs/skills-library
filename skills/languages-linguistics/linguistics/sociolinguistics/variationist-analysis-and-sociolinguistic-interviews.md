---
id: languages-linguistics.linguistics.sociolinguistics.variationist-analysis-and-sociolinguistic-interviews
name: variationist-analysis-and-sociolinguistic-interviews
category: languages-linguistics
field: linguistics
product: sociolinguistics
tags: [sociolinguistics, variationist-sociolinguistics, labov, linguistic-variable, variants, sociolinguistic-interview, observers-paradox, style-shifting, mixed-effects-regression, rbrul, goldvarb, r, lme4, dialectology, language-attitudes, matched-guise, code-switching, social-networks, apparent-time, sampling, ethics, consent]
level: practitioner
status: draft
description: "Run a variationist study: define a linguistic variable, design and conduct sociolinguistic interviews, code tokens consistently, and model variation with mixed-effects regression in R."
sources: ["Labov, Sociolinguistic Patterns", "Tagliamonte, Analysing Sociolinguistic Variation", "Johnson, Getting off the GoldVarb standard (2009, Language and Linguistics Compass)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Variationist analysis and sociolinguistic interviews

**Goal:** show, with defensible numbers, how a speech community's choice between
alternative ways of saying the same thing is conditioned by linguistic context and
social factors.

## 1. Define the variable (most studies fail here)
- A **linguistic variable** = two or more **variants** with the same referential
  meaning: `(ing)` → `[ɪŋ]` vs `[ɪn]`; `(t/d)` deletion in "west side"; quotative
  *be like* vs *say*.
- Circumscribe the **variable context**: every place the variable *could* occur.
  Exclude contexts where variation is impossible (e.g. "-ing" in monomorphemic
  "thing" if your community never varies there) and **say what you excluded and why**.
- Morphosyntactic and discourse variables need careful equivalence arguments.

## 2. Sampling
- Stratify by the social factors you'll test (age, gender, class, ethnicity,
  neighbourhood), but expect cells to be uneven; mixed models handle that.
- **Apparent time:** comparing age groups at one moment as a proxy for change —
  state the age-grading caveat.
- Networks or communities of practice are alternatives to demographic categories.

## 3. The sociolinguistic interview
- 45–90 minutes, one or two speakers, conversational.
- Modules: personal history, neighbourhood, childhood games, **danger-of-death /
  personal-narrative questions** (narratives elicit more vernacular speech), then
  reading passage, word list and minimal pairs for **style** contrast.
- **Observer's paradox:** you want speech as it is when not observed; lower
  self-monitoring with topics speakers care about, peer groups, and long sessions.
- Recording: lavalier mic, quiet room, WAV 44.1 kHz/16-bit or better; note metadata.
- **Ethics:** informed consent covering storage, anonymity and reuse; ethics approval
  from your institution; option to withdraw.

## 4. Extraction and coding
1. Transcribe (orthographic), time-aligned (ELAN or Praat TextGrid).
2. Extract **every** token in the variable context, not a sample of salient ones.
3. Cap tokens per speaker or per lexical item if a few frequent words dominate
   (e.g. "going to"); document the cap.
4. Code: dependent variant + linguistic predictors (preceding/following segment,
   stress, morphological class, lexical item) + social predictors.
5. Code a subset twice (or by a second coder); report agreement (Cohen's κ).

## 5. Statistics
- Classic: Goldvarb / Varbrul logistic regression (factor weights). Still cited, but
  can't model speaker and word as random effects.
- Current practice: **mixed-effects logistic regression** in R, e.g.
  `glmer(variant ~ following_seg + age + gender + (1|speaker) + (1|word), family = binomial)`
  with `lme4`, or Rbrul as a front-end.
- Report: N tokens, N speakers, distribution by cell, model coefficients with
  significance, random-effect variance. Check collinearity between social factors.
- Treat **continuous age** as continuous where possible.

## 6. Beyond the variable
- **Language attitudes:** matched-guise or verbal-guise experiments (same speaker,
  different varieties, rated on traits).
- **Code-switching:** distinguish insertion vs alternation; analyse by discourse
  function or structural constraints.
- **Dialectology:** isoglosses from questionnaires or corpora; dialectometry for
  aggregated distances.

## Verify
- [ ] Variable context defined, with exclusions listed.
- [ ] Interviews include a vernacular-eliciting module and style contrasts.
- [ ] All tokens extracted; per-speaker/word caps documented.
- [ ] Inter-coder agreement reported.
- [ ] Model includes speaker (and word) random effects; Ns reported per cell.
- [ ] Consent and ethics approval documented.
