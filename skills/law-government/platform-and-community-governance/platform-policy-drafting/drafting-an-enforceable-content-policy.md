---
id: law-government.platform-and-community-governance.platform-policy-drafting.drafting-an-enforceable-content-policy
name: drafting-an-enforceable-content-policy
category: law-government
field: platform-and-community-governance
product: platform-policy-drafting
tags: [platform-policy-drafting, platform-and-community-governance, content-policy, community-guidelines, community-standards, acceptable-use-policy, aup, terms-of-service, house-rules, policy-definitions, enforcement-guidelines, internal-guidelines, policy-rationale, harassment-policy, hate-speech-policy, misinformation-policy, newsworthiness-exception, public-interest-exception, edge-cases, policy-launch, policy-change-log, santa-clara-principles, human-rights-based-approach, ungps, trust-and-safety, tns, content-governance]
level: practitioner
status: draft
description: "Write a platform content policy moderators can apply consistently: harm rationale, scope, operational definitions, prohibited vs allowed examples, exceptions, internal guidelines, testing and launch."
sources: ["Santa Clara Principles on Transparency and Accountability in Content Moderation (2018, revised 2021)", "UN Guiding Principles on Business and Human Rights", "Trust & Safety Professional Association, T&S curriculum (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drafting an enforceable content policy

**Goal:** a rule that users can understand, moderators can apply the same way every
time, and the platform can defend to users, regulators and the press. Applies to social
platforms, marketplaces, forums, games and app stores. Legal backdrops differ — e.g. US
(First Amendment does not bind private platforms; Section 230 shields most moderation
decisions), the EU Digital Services Act (clear terms and statements of reasons), the
UK Online Safety Act (duties around illegal content and children) — so legal review
for each market is required.

## 1. Start from the harm
Write a one-paragraph **rationale**: what harm, to whom, how it happens on this product,
and how severe/likely. Gather data: user reports, escalations, incidents, external
research, regulatory requirements. A rule without a harm rationale drifts and is hard to
explain.

## 2. Set scope and posture
- Which surfaces (posts, comments, DMs, profiles, ads, livestreams, usernames)?
- Who is protected (all users, minors, protected characteristics, public figures)?
- Posture: remove, restrict reach, label, age-gate, or allow with friction. Not every
  harm warrants removal; proportionate options reduce over-enforcement.
- Align with your human-rights commitments: legality, necessity, proportionality,
  non-discrimination.

## 3. Write operational definitions
A moderator must be able to decide in seconds from what is on screen.
- Replace subjective words ("offensive", "inappropriate") with observable criteria
  ("content that targets a person with a statement of inferiority based on a protected
  characteristic").
- Define every key term once, in a glossary used across all policies.
- Specify what signals the moderator may use (the content, captions, account context,
  external context) and what they may not assume.

## 4. Two layers: public and internal
| Public policy (community guidelines) | Internal enforcement guidelines |
|---|---|
| Plain language, examples, why the rule exists | Decision trees, detailed definitions, edge cases |
| Stable; changes announced | Updated as edge cases arise, versioned |
| Readable at a school reading level | Precise and exhaustive |
Keep them consistent: an internal rule with no public basis is a transparency and
regulatory risk.

## 5. Examples and exceptions
- For each rule give violating and non-violating examples, especially the near-misses
  (quoting hate to condemn it; news reporting; satire; reclaimed slurs; artistic nudity).
- Define exceptions narrowly with criteria (e.g. public-interest / newsworthiness:
  who decides, what factors, which content can never qualify — e.g. child sexual abuse
  material has no exceptions).

## 6. Test before launch
1. Label a sample of real past content (200+ items, including edge cases) with the draft
   policy using several reviewers independently.
2. Measure agreement; where reviewers disagree, the language is unclear — rewrite.
3. Estimate volume impact (how much more or less will be actioned?) and staffing needs.
4. Check for disparate impact on particular communities or languages.
5. Run legal, policy-communications and regional-expert review.

## 7. Launch and maintain
- Publish with an effective date, a summary of what changed and why, and notify users
  as required (the EU DSA requires informing users of significant changes to terms).
- Train moderators, update classifiers and automated rules, update appeal guidance.
- Keep a change log; review each policy at least annually and after major incidents.

## Gotchas
- Writing for the headline case and forgetting volume: the rule will be applied
  millions of times to ambiguous content.
- Policies that require knowledge moderators cannot have (intent, off-platform facts)
  without saying how to get it.
- Language and cultural gaps — slurs, symbols and coded terms vary by market.
- Shipping a rule without matching automated enforcement changes.

## Verify
- [ ] Harm rationale, scope and proportionate enforcement options written.
- [ ] Operational definitions in the shared glossary; no subjective-only tests.
- [ ] Public and internal versions consistent; examples include near-misses.
- [ ] Reviewer agreement tested on real content; volume and disparate impact estimated.
- [ ] Legal review per market; launch notice, training and change log done.
