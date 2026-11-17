---
id: social-sciences.political-science.political-methodology.ideal-points-and-text-scaling
name: ideal-points-and-text-scaling
category: social-sciences
field: political-science
product: political-methodology
tags: [political-methodology, ideal-point-estimation, roll-call-analysis, nominate, dw-nominate, voteview, wnominate, pscl, bayesian-irt, item-response-theory, emirt, text-as-data, text-scaling, wordscores, wordfish, quanteda, manifesto-project, marpor, party-positions, chapel-hill-expert-survey, ches, event-data, icews, gdelt, scaling-validation, polarization, ideology-measurement]
level: advanced
status: draft
description: "Estimating political positions: roll-call ideal points (NOMINATE, Bayesian IRT), text scaling (Wordscores, Wordfish) and validating against known positions."
sources: ["Poole & Rosenthal, Ideology and Congress", "Clinton, Jackman & Rivers, 'The Statistical Analysis of Roll Call Data' (2004)", "Laver, Benoit & Garry, 'Extracting Policy Positions from Political Texts Using Words as Data' (2003)", "Slapin & Proksch, 'A Scaling Model for Estimating Time-Series Party Positions from Texts' (2008)", "Grimmer & Stewart, 'Text as Data: The Promise and Pitfalls' (2013)", "quanteda documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ideal points and text scaling

**Goal:** place legislators, parties or other actors on latent ideological dimensions
from their votes or their words — and show the scale measures what you claim.

## 1. Roll-call ideal points
- Data: a legislator × vote matrix (yea=1, nay=0, abstain/absent=NA). US Congress
  data and DW-NOMINATE scores are on **Voteview**; other legislatures need scraping
  or national archives.
- Methods:
  - **W-NOMINATE / DW-NOMINATE** (`wnominate` R package): spatial utility model;
    DW links scores across sessions.
  - **Bayesian IRT** (`pscl::ideal`, `emIRT` for speed, Stan): gives uncertainty
    intervals; easy to add covariates or dynamics.
- Preprocessing: drop **lopsided votes** (e.g. <2.5% minority) and members with very
  few votes; they add noise, not information.
- **Identification:** the scale's direction is arbitrary. Fix it by constraining a
  known left legislator negative and a known right one positive, or post-hoc flipping.
- **Gotcha:** in strong-party parliaments (Westminster systems), roll calls reflect
  party discipline and government–opposition, not ideology. The first dimension
  often just separates government from opposition — don't call it left–right.
- Agenda control means votes are not a random sample of issues.

## 2. Text scaling
Prepare text with `quanteda` (R) or similar: tokenize, lowercase, remove punctuation
and numbers; decide carefully on stopwords and stemming (they can change results).
Build a document-feature matrix; trim very rare features.
- **Wordscores (supervised):** assign scores to reference texts (e.g. from expert
  surveys), score virgin texts by word overlap. Results depend heavily on reference
  choice; raw virgin scores shrink toward the middle and need rescaling.
- **Wordfish (unsupervised):** Poisson model estimating one latent dimension from word
  frequencies. Good for one-dimensional debates within one language and genre; it
  will happily find *some* dimension (e.g. topic or time), which may not be ideology.
- **Manifesto Project (MARPOR):** hand-coded quasi-sentences of party platforms;
  the RILE left–right index is widely used but critiqued (saliency logic, fixed
  categories).
- **Expert surveys** (Chapel Hill Expert Survey) provide benchmarks.

## 3. Event data
For conflict/cooperation between actors, use coded events (ICEWS, GDELT, PHOENIX)
and aggregate to actor-pair-period scores (e.g. Goldstein scale). Deduplicate stories
and beware news-coverage bias.

## 4. Validation is the job
- **Face validity:** do known extremists land at the extremes?
- **Convergent validity:** correlate with expert surveys, other methods, roll calls.
- **Predictive validity:** does the measure predict defections, coalition formation?
- Report uncertainty intervals; overlapping intervals mean you can't rank actors.
- Grimmer & Stewart's rule: "validate, validate, validate" — automated methods are
  not self-justifying.

*Uncertainty:* lopsided-vote cutoffs vary (2.5% is the W-NOMINATE default as commonly
documented); check package defaults for your version.

## Verify
- [ ] Vote matrix coding and exclusion rules (lopsided votes, low-attendance members) reported.
- [ ] Scale direction identified with named anchors.
- [ ] Text preprocessing choices stated and robustness checked.
- [ ] Scores validated against at least one independent benchmark.
- [ ] Uncertainty intervals shown for estimated positions.
