---
id: sales-marketing.market-research-consumer-insights.segmentation-studies.needs-based-segmentation-and-activation
name: needs-based-segmentation-and-activation
category: sales-marketing
field: market-research-consumer-insights
product: segmentation-studies
tags: [segmentation-studies, market-segmentation, customer-segmentation, needs-based-segmentation, attitudinal-segmentation, behavioural-segmentation, cluster-analysis, k-means, latent-class, factor-analysis, maxdiff, segment-sizing, personas, typing-tool, golden-questions, discriminant-analysis, activation, targeting, crm-append, consumer-insights]
level: advanced
status: draft
description: "Design and run a needs-based market segmentation: choose bases, collect data, cluster, judge solutions, size segments, and build a typing tool so sales and marketing can use them."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Needs-based segmentation and activation

**Goal:** split a market into a handful of groups that differ in what they need
and how they behave, are big enough to matter, and can be *found* by sales and
marketing — then hand over the tools to find them. A segmentation nobody can
apply is the commonest failure in this work.

## 1. Pick the basis for the decision
- **Needs/benefits sought** — best for product and proposition design.
- **Attitudes** — useful for communication, harder to target.
- **Behaviour/value** (spend, frequency, channel) — easy to target from CRM data,
  says little about why.
- **Demographics/firmographics** — easy to find, usually weak at explaining choice.
Most commercial work clusters on needs + attitudes, then **profiles** segments on
behaviour and demographics for targeting.

## 2. Collect the data
- Survey of n ≈ 1,500–3,000 category buyers (enough for 5–7 segments with ≥ 150
  each). Representative quotas; see unbiased-questionnaire-and-significance-reads.
- Needs battery of 20–40 statements. **MaxDiff** (best–worst) on needs avoids
  everyone rating everything "important" and handles scale-use differences across people.
- Include profiling variables you *can* target on: demographics, media,
  channel, brand used, CRM-matchable fields (with consent).

## 3. Build the solution
1. Prepare: for rating data, consider factor analysis or standardising within
   respondent to reduce scale-use bias; MaxDiff utilities can go straight in.
2. Cluster with several methods/seeds — k-means for speed, latent class for
   mixed data and fit statistics (BIC), hierarchical to suggest k.
   Tools: R (`kmeans`, `poLCA`, `mclust`), Python (`scikit-learn`), SPSS, Q/Displayr,
   Sawtooth for MaxDiff + latent class.
3. Run k = 3 to 8. Judge each solution on:
   - **Distinctness** — needs profiles clearly different (index each segment's
     mean vs total; > 120 or < 80 stands out);
   - **Size** — no segment < ~8% unless strategically vital;
   - **Stability** — re-run on random halves; segments should replicate;
   - **Actionability** — different enough in behaviour/profile to target;
   - **Story** — can you name each segment in one line?
   Statistics narrow the choice; business usability decides it.

## 4. Size and value
Weight to the population; report each segment's share of people, share of
category spend, growth potential, and your brand's share within it. A small
segment holding 35% of spend may be the target.

## 5. Activation (the part that gets skipped)
- **Typing tool / golden questions**: 6–12 survey questions that classify a new
  respondent into a segment with ~75–85% accuracy (discriminant analysis,
  multinomial logit or a decision tree on the original data). Use it in every
  future study so segments stay consistent.
- **CRM append**: model segment membership from data you hold on customers
  (purchase, demographics) to score your database. Accuracy will be lower — report it.
- **Personas and playbooks**: one page per segment — needs, triggers, barriers,
  channels, proposition, example verbatims. Workshop with sales, product, media.

## Gotchas
- Too many statements produce segments that differ only in "agreeing with
  everything" — fix scale bias or use MaxDiff.
- Clusters always appear even in data with no real structure; check stability.
- Segments drift; refresh every 2–4 years and keep the typing tool constant meanwhile.
- **Uncertain:** the accuracy and size thresholds above are practitioner norms, not standards.

## Verify
- [ ] Basis chosen to match the decision; profiling variables collected.
- [ ] Multiple k and methods tested; stability checked on split halves.
- [ ] Each segment ≥ ~8%, distinct on needs, nameable in one line.
- [ ] Segments sized by people and by spend.
- [ ] Typing tool built with stated accuracy; playbooks handed over.
