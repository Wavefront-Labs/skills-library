---
id: law-government.platform-and-community-governance.platform-policy-drafting.writing-enforceable-content-policies-and-community-guidelines
name: writing-enforceable-content-policies-and-community-guidelines
category: law-government
field: platform-and-community-governance
product: platform-policy-drafting
tags: [platform-and-community-governance, platform-policy-drafting, content-policy, community-guidelines, community-standards, acceptable-use-policy, aup, terms-of-service, policy-writing, trust-and-safety, t-and-s, hate-speech-policy, harassment-policy, misinformation-policy, violent-extremism, adult-content, definitions, protected-characteristics, exceptions, newsworthiness, public-interest-exception, enforcement-guidelines, internal-guidance, edge-cases, policy-launch, santa-clara-principles, policy-changelog]
level: practitioner
status: draft
description: "Draft platform rules moderators can apply consistently: harm rationale, precise definitions, bright lines vs. standards, exceptions, public vs. internal guidance, case-set testing, launch."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing enforceable content policies and community guidelines

**Goal:** a rule that users can understand, moderators can apply the same way
thousands of times a day, and that targets the actual harm without sweeping up
legitimate speech.

## 1. Start from the harm and the evidence
Before drafting, write a one-page **policy rationale**: what harm (to whom, how
severe, how likely, at what scale), the evidence (incident data, researcher and civil
society input, user reports), affected communities, and the speech interests at stake
(news reporting, counter-speech, art, self-expression). Note legal floors:
illegal-content duties **vary by jurisdiction** and must be handled (see the
platform-regulatory-response skill) but are usually narrower than platform policy.

## 2. Structure the rule
Use a consistent template for every policy:
1. **Policy rationale** (public, short).
2. **Do not post** — the prohibited content, as concrete categories.
3. **Definitions** of every key term ("protected characteristic", "credible threat",
   "dangerous organisation", "graphic").
4. **Exceptions / allowed contexts** — condemnation, news, education, documentary,
   satire, self-referential reclaimed terms. Say how context is shown.
5. **Enforcement** — remove, label, age-gate, reduce distribution, account penalties.
6. **Internal guidance** (non-public): decision trees, examples, lists, thresholds.

## 3. Drafting technique
- **Bright lines vs. standards.** Bright lines ("images of X are removed") give
  consistency and speed but over/under-include; standards ("content that
  glorifies…") fit context but drift between reviewers. Use bright lines for high-
  volume, high-severity categories; standards with detailed internal examples elsewhere.
- **Write for the reviewer's view.** A moderator sees the post, maybe the account, for
  30 seconds, often in a second language. If the rule requires knowing intent or
  off-platform facts, say what signals count as evidence.
- One concept per sentence; define, don't stack adjectives ("severe, egregious" means
  nothing to a reviewer).
- Avoid lists of slurs/groups in the public text; keep them in internal guidance
  with regular updates.
- Specify **object of the rule**: post, comment, profile, username, group, ad, DM —
  different surfaces may need different rules.

## 4. Test before launch
- **Case set:** collect 100–300 real, de-identified examples including hard edges
  (satire, quotes, news, reclaimed terms, other languages).
- Have several reviewers label them with the draft; measure **agreement**. Low
  agreement means the rule or guidance is ambiguous — fix the text, not the reviewers.
- Red-team for evasion (misspellings, coded language, images of text).
- Estimate volume impact and over-enforcement on vulnerable groups.
- Consult affected communities and experts; record what you changed.

## 5. Launch and maintain
- Update public guidelines with a dated **changelog**; give notice for significant
  changes where feasible.
- Train reviewers and update classifiers/keyword lists at the same time.
- Monitor appeals overturn rates, prevalence and reviewer questions for the first
  weeks; a spike in overturns usually reveals a drafting gap.
- The **Santa Clara Principles** (numbers, notice, appeal) are a widely cited
  benchmark for transparency around rules.

## Gotchas
- Rules written in reaction to one viral incident often over-reach — test against the
  wider case set.
- Translation: localise examples and slurs with native speakers, not machine translation.
- Policy written to satisfy a regulator in one country often leaks globally; decide
  deliberately between geo-blocking and a global rule.

## Verify
- [ ] Rationale names the harm, evidence and speech interests.
- [ ] Every key term defined; exceptions explicit.
- [ ] Reviewer agreement measured on a real case set and acceptable.
- [ ] Public text, internal guidance and enforcement actions all updated together.
- [ ] Changelog and post-launch monitoring in place.
