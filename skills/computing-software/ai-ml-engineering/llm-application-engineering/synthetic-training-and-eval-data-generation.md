---
id: computing-software.ai-ml-engineering.llm-application-engineering.synthetic-training-and-eval-data-generation
name: synthetic-training-and-eval-data-generation
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, model-selection, synthetic-data-generation, self-instruct, data-augmentation, decontamination, data-diversity]
level: practitioner
status: docs-checked
description: "Generate synthetic training and eval data with LLMs: seeds and attribute-driven diversity, quality filtering, dedup, decontamination, and mixing with real data."
sources:
  - https://arxiv.org/abs/2212.10560
  - https://arxiv.org/abs/2304.12244
  - https://ekzhu.com/datasketch/lsh.html
  - https://arxiv.org/abs/2305.17493
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthetic training and eval data generation

**Goal:** fill data gaps (rare intents, edge cases, new languages, cold-start tasks) with LLM-generated examples that actually improve the target model or eval coverage.

## Generate for diversity, not volume
- **Seeds:** start from real examples (Self-Instruct, Wang et al. 2022, bootstraps off a model's own generations and filters invalid or similar ones before fine-tuning).
- **Attribute grids:** explicitly vary persona, intent, difficulty, length, tone, domain, language, typos/noise: sample combinations and ask for one example per combination. Asking "generate 100 diverse examples" in one call yields repetitive outputs.
- **Evolve** (Evol-Instruct, Xu et al. 2023): starting from an initial set of instructions, rewrite them step by step into more complex ones to cover the difficult tail.
- Use high temperature and several generator models/prompts to avoid one model's style dominating.

## Filter hard
1. Validators: schema, length, label constraints, language ID.
2. Quality judge with a rubric (and spot-checked by humans); drop low scores.
3. Deduplicate: exact hash + near-duplicate (MinHash LSH or embedding similarity) within the synthetic set and against real data.
4. **Decontaminate** against eval/test sets: synthetic data generated from or near eval items inflates scores.
5. Label check: for synthetic classification data, have a different model or a human verify labels on a sample.

## Use it well
- Mix with real data; keep real data as the majority where you have it. Track performance with and without synthetic data (ablation).
- Eval sets: synthetic cases are useful for coverage but tend to be easier and cleaner than real traffic - report metrics on real and synthetic slices separately.
- Repeatedly training models on model-generated data can degrade diversity and tails (model collapse: tails of the original distribution disappear, Shumailov et al. 2023); keep refreshing with real data.
- Check generator model terms of use for training other models.

## Verify
- [ ] Diversity measured (distinct n-grams/embedding spread, attribute coverage) not just count.
- [ ] Dedup and decontamination steps logged with counts removed.
- [ ] Ablation shows synthetic data improves the target metric on real held-out data.

## Checked
2026-11-01. Confirmed from the arXiv abstracts: Self-Instruct (2212.10560), WizardLM / Evol-Instruct (2304.12244), The Curse of Recursion (2305.17493); datasketch MinHash LSH page (Jaccard-threshold lookup). The rest is workflow advice with no figures. Removed: seed-set and constraint-type specifics the abstracts do not state.
Method: documentation only; no commands were run.
