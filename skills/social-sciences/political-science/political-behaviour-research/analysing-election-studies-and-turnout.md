---
id: social-sciences.political-science.political-behaviour-research.analysing-election-studies-and-turnout
name: analysing-election-studies-and-turnout
category: social-sciences
field: political-science
product: political-behaviour-research
tags: [political-behaviour-research, political-behaviour, voting-behaviour, elections, turnout, election-studies, anes, bes, cses, ces, cces, survey-weights, validated-vote, vote-overreporting, social-desirability, partisanship, party-identification, economic-voting, polling-analysis, poll-aggregation, house-effects, electoral-systems, duverger, ecological-inference, voter-file, srvyr, survey-package]
level: practitioner
status: draft
description: "Analysing voting and turnout with election studies (ANES, BES, CSES): weights, validated vote, over-reporting, poll aggregation and turnout models."
sources: ["ANES, BES and CSES user guides and codebooks", "Lumley, Complex Surveys: A Guide to Analysis Using R (2010)", "Ansolabehere & Hersh, 'Validation: What Big Data Reveal About Survey Misreporting' (2012)", "Cox, Making Votes Count (1997)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Analysing election studies and turnout

**Goal:** answer who votes, for whom and why, using national election studies and
polls correctly — weights, misreporting and all.

## 1. Know the main sources
- **ANES** (US, since 1948; pre/post-election, face-to-face and online modes).
- **BES** (British Election Study; large internet panel waves plus a probability
  face-to-face post-election survey).
- **CSES** (Comparative Study of Electoral Systems; a common module fielded in
  national studies — use for cross-national micro-level comparison).
- **CES (formerly CCES)**, US, very large opt-in online sample with vote validation.
- National voter files / registers (where legal) for turnout validation.
Download the codebook and the methodology report with the data — every study has
quirks (split samples, question versions by wave).

## 2. Weights and design
- Always apply the supplied weight; note which one (pre vs post, panel vs
  cross-section, face-to-face vs web). Using the wrong weight is a common silent bug.
- For probability samples, account for clusters and strata (`survey` / `srvyr` in R,
  `svy:` in Stata) to get honest standard errors.
- Missing codes (−9, −8, 98, 99...) must be set to NA before analysis.

## 3. Turnout over-reporting
Self-reported turnout is reliably higher than official turnout — partly social
desirability, partly that survey respondents are more political. Responses:
- Use **validated vote** where available (matched to voter records).
- Compare survey turnout to official figures; report the gap.
- Use question wordings that offer face-saving options ("I thought about voting but
  didn't").
Gotcha: validation itself has match errors; non-matches are not all non-voters.

## 4. Standard models
- Turnout: logit on resources (education, age, income), mobilisation (contacted),
  attitudes (interest, efficacy, partisanship strength), and institutional context.
- Vote choice: multinomial logit for multiparty systems; party ID, leader evaluations,
  economic perceptions (sociotropic vs pocketbook), issue positions.
- Party ID is endogenous to vote choice in many systems; treat causal claims carefully
  and prefer panel data.

## 5. Electoral-system effects
District magnitude, thresholds and formula shape party numbers (Duverger's tendency
toward two-party competition under plurality). Use CSES or district-level data and
measure the **effective number of parties** (1/Σ vote-shares²).

## 6. Polling analysis
- Aggregate polls weighting by sample size and recency; estimate **house effects**
  (systematic lean of each pollster).
- Margin of error applies to each share, and is larger for the *lead*.
- Polls measure intention; turnout screens ("likely voter" models) move results.

## 7. Aggregate data
District or precinct results + census data invite **ecological inference** errors:
group-level correlations don't tell you how individuals voted. Use EI methods with
stated assumptions or avoid individual-level claims.

*Uncertainty:* study modes and validation availability change by year — check the
specific release.

## Verify
- [ ] Correct weight variable used and design-based SEs computed where applicable.
- [ ] Missing-value codes converted before analysis.
- [ ] Self-reported turnout compared to official/validated figures.
- [ ] Multiparty vote choice modelled appropriately (not binary by default).
- [ ] No individual-level conclusions drawn from aggregate correlations.
