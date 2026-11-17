---
id: computing-software.data-engineering.data-modelling.entity-resolution-and-matching
name: entity-resolution-and-matching
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, entity-resolution, record-linkage, deduplication, fuzzy-matching, splink, fellegi-sunter, blocking, master-data-management]
level: advanced
status: gated
description: "Resolve duplicate records across sources: standardisation, blocking, comparison functions, probabilistic (Fellegi-Sunter) scoring with Splink, thresholds, clustering and evaluation."
sources:
  - https://moj-analytical-services.github.io/splink/
  - https://moj-analytical-services.github.io/splink/topic_guides/theory/fellegi_sunter.html
  - https://moj-analytical-services.github.io/splink/topic_guides/blocking/blocking_rules.html
  - https://recordlinkage.readthedocs.io/en/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entity resolution and matching

**Goal:** decide which records refer to the same real-world person/company/product, at scale, with a measurable error rate.

## 1. Standardise first
Most matching quality comes from cleaning:
- names: lower-case, strip punctuation/titles/legal suffixes (`ltd`, `gmbh`, `inc`), normalise whitespace and accents; split first/last;
- emails: lower-case, trim; optionally strip `+tag` and dots for Gmail;
- phones: E.164 (`libphonenumber`) (gated: unconfirmed, not re-checked);
- addresses: parse and standardise (libpostal or a postal API); postcode upper-case without spaces;
- dates: ISO; flag placeholder values (`1900-01-01`, `test@test.com`) as NULL.

## 2. Deterministic rules
Exact matches on strong identifiers (tax ID, verified email, passport) link immediately. Keep them as the first pass — they're explainable and cheap.

## 3. Blocking (avoid n² comparisons)
Compare only pairs that share a cheap key: same postcode, same first 3 letters of surname + birth year, same email domain + first initial. Use several blocking rules (OR'ed) to catch pairs one rule misses. Check the number of comparisons each rule generates before running.

## 4. Probabilistic scoring with Splink
The code below runs on splink 4.0.17 (400 synthetic rows with 100 planted duplicates gave 300 clusters). Splink 5.0.0 (2026-09-28) removed the `db_api=` argument of `Linker` and Amazon Athena support and requires Python 3.10+: register the input first, `db_api = DuckDBAPI(); linker = Linker(db_api.register(df), settings)` (this form ran on 5.0.0 with the same result). Pin the major version you test.
```python
import splink.comparison_library as cl
from splink import DuckDBAPI, Linker, SettingsCreator, block_on

settings = SettingsCreator(
    link_type="dedupe_only",
    blocking_rules_to_generate_predictions=[block_on("postcode"), block_on("surname", "dob")],
    comparisons=[
        cl.JaroWinklerAtThresholds("first_name", [0.9, 0.8]),
        cl.JaroWinklerAtThresholds("surname", [0.9, 0.8]),
        cl.DateOfBirthComparison("dob", input_is_string=True),
        cl.ExactMatch("postcode").configure(term_frequency_adjustments=True),
        cl.EmailComparison("email"),
    ],
)
linker = Linker(df, settings, db_api=DuckDBAPI())          # Spark backend for big data (Athena support was removed in Splink 5)
linker.training.estimate_probability_two_random_records_match([block_on("email")], recall=0.7)
linker.training.estimate_u_using_random_sampling(max_pairs=1e7)
linker.training.estimate_parameters_using_expectation_maximisation(block_on("dob"))
preds = linker.inference.predict(threshold_match_probability=0.5)
clusters = linker.clustering.cluster_pairwise_predictions_at_threshold(preds, 0.95)
```
- Fellegi-Sunter: each comparison level contributes a match weight from m (P(agree | match)) and u (P(agree | non-match)) probabilities; rare values (term frequency) count more than common ones.
- Pairwise links → clusters via connected components; a cluster = one entity.

## 5. Thresholds and review
- Choose two thresholds: auto-match above (e.g. 0.95), auto-reject below (e.g. 0.5), clerical review in between.
- Watch for transitive over-merging: A~B and B~C linking A and C that clearly differ. Inspect large clusters first.
- Never merge irreversibly: store pair scores and cluster assignments so merges can be split.

## 6. Evaluate
- Label a sample of pairs (including near-threshold ones) → precision/recall at each threshold.
- Splink charts (4.0.17 `linker.visualisations`): `waterfall_chart` (why a pair scored), `m_u_parameters_chart`, `match_weights_chart`, `cluster_studio_dashboard` for review.
- Track over time: cluster count, average cluster size, review queue volume.

## Verify
- [ ] Precision and recall measured on labelled pairs at the chosen thresholds.
- [ ] Largest clusters manually reviewed for over-merging.
- [ ] Results are reproducible (fixed seeds, versioned settings JSON).
