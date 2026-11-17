---
id: computing-software.ai-ml-engineering.hugging-face.writing-model-cards-with-metadata
name: writing-model-cards-with-metadata
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, model-card, model-card-metadata, model-index, responsible-ai, hub]
level: practitioner
status: gated
description: "Write Hugging Face model cards: YAML metadata (license, datasets, base_model, pipeline_tag, model-index results) plus intended use, limitations, training data and evaluation."
sources:
  - https://huggingface.co/docs/hub/model-cards
  - https://huggingface.co/docs/huggingface_hub/guides/model-cards
  - https://arxiv.org/abs/1810.03993
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing model cards with metadata

The `README.md` in a model repo is the model card. The YAML header drives Hub search, widgets, licence display and leaderboards; the body tells users whether the model fits their use.

## Metadata header
```yaml
---
license: apache-2.0
language: [en, de]
library_name: transformers
pipeline_tag: text-classification
base_model: microsoft/deberta-v3-base
datasets: [org/support-tickets-v3]
tags: [customer-support, intent-classification]
metrics: [f1, accuracy]
model-index:
- name: ticket-intent-deberta
  results:
  - task: {type: text-classification, name: Intent classification}
    dataset: {name: support-tickets-v3, type: org/support-tickets-v3, split: test}
    metrics:
    - {type: f1, value: 0.912, name: Macro F1}
---
```
- `base_model` links fine-tunes/adapters/quantisations to the parent (model tree on the Hub); the relation is inferred from the repo, and the Hub docs say you can set it explicitly, e.g. `base_model_relation: quantized` (values per the docs: adapter, merge, quantized, finetune). A `new_version` field points to a newer model.
- `pipeline_tag` and `library_name` enable the inference widget and code snippets.
- Gated access fields (`extra_gated_prompt`, `extra_gated_fields`) live here too.

## Body sections (Mitchell et al. structure)
1. **Model details**: architecture, size, developers, version, date, licence.
2. **Intended uses / out-of-scope uses**: concrete, including who should not use it.
3. **How to use**: minimal working code with pinned revision.
4. **Training data**: sources, size, time range, preprocessing, known gaps; link dataset cards.
5. **Training procedure**: hyperparameters, hardware, compute time (and estimated emissions if known).
6. **Evaluation**: datasets, metrics, results with confidence intervals; disaggregated results by relevant slices (language, demographic, domain).
7. **Bias, risks, limitations**: known failure modes, misuse risks, recommendations.
8. **Citation, contact**.

## Programmatic
```python
from huggingface_hub import ModelCard, ModelCardData
data = ModelCardData(language="en", license="apache-2.0", library_name="transformers", base_model="microsoft/deberta-v3-base")
card = ModelCard.from_template(data, model_id="org/ticket-intent", model_description="...")
card.push_to_hub("org/ticket-intent")
ModelCard.load("org/ticket-intent").data.to_dict()      # read metadata
```
Ran locally (huggingface_hub 2.2.0): `ModelCard.from_template` renders a card, `save`/`load` round-trip the metadata, `ModelCard(text).data.eval_results` parsed the `model-index` block above into an `EvalResult` (f1 0.912), and `card.validate()` returned without error (it checks the metadata against the Hub). `card.push_to_hub` needs an account and was not run (gated: unconfirmed, source is paywalled or blocked). `Trainer.push_to_hub()` auto-generates a card with hyperparameters and metrics; edit it, since generated cards lack intended use and limitations.

## Gotchas
- Invalid YAML: `ModelCard(text)` raises a `yaml.ParserError` locally (ran with an unclosed flow sequence), so load the card in CI before pushing; how the Hub page reacts to a pushed bad header was not tested (gated: unconfirmed, source is paywalled or blocked). Validate metadata with `ModelCard.load(...).validate()`.
- Don't claim benchmark numbers you didn't reproduce; state the evaluation setup (prompt format, shots, decoding).
- Licence must be compatible with the base model's and training data's terms.

## Verify
Open the repo page: licence badge, base model link, widget and evaluation results render; the usage snippet runs in a fresh environment.
