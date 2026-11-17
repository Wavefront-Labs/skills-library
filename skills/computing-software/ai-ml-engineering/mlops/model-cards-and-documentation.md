---
id: computing-software.ai-ml-engineering.mlops.model-cards-and-documentation
name: model-cards-and-documentation
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-governance, model-cards, model-documentation, intended-use, hugging-face-model-card, sagemaker-model-cards]
level: practitioner
status: draft
description: "Write model cards for reviewers and users: Mitchell et al. sections, intended and out-of-scope use, per-slice evaluation, limitations, generated from pipeline metadata."
sources:
  - https://arxiv.org/abs/1810.03993
  - https://huggingface.co/docs/hub/model-cards
  - https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html
  - https://www.nist.gov/itl/ai-risk-management-framework
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Model cards and documentation

**Goal:** every production model has a short, current document saying what it does, how well, for whom, and where it should not be used.

## Sections (after Mitchell et al., 2019)
1. **Model details:** owner/contact, version, date, architecture, training procedure summary, licence.
2. **Intended use:** primary use cases and users; **out-of-scope uses** stated explicitly ("not for credit decisions", "not validated for patients under 18").
3. **Factors:** groups, environments and instruments that affect performance (demographics, devices, languages, regions).
4. **Metrics:** which metrics and thresholds, and why they match the use (decision costs).
5. **Evaluation data:** source, time range, how it differs from training data.
6. **Training data:** source, time range, preprocessing, known gaps (at the level of detail you can share).
7. **Quantitative analyses:** results overall **and per slice/factor**, with confidence intervals.
8. **Ethical considerations and risks:** potential harms, mitigations, human oversight.
9. **Caveats and recommendations:** known failure modes, monitoring in place, retraining cadence.

## Generate, don't hand-write
Fill the factual parts automatically from the pipeline: version, data versions, metrics and slice tables from the evaluation step, link to the training run. Humans write intended use, limitations and risks. Regenerate on every model version so the card can't go stale.

Formats/tools: Hugging Face `README.md` model cards with YAML metadata (`model-index` for results), SageMaker Model Cards (linked to model packages), or a markdown template in your repo rendered into the registry description.

## Reviews
Make the card part of the promotion checklist: risk/compliance reviewers read the card, not the code. Under NIST AI RMF and regulations like the EU AI Act, documentation of intended purpose, data and performance is expected for higher-risk systems.

## Verify
- [ ] Card exists for every production model version and links to its training run.
- [ ] Out-of-scope uses and per-slice results included.
- [ ] Card regenerated automatically on new versions.
