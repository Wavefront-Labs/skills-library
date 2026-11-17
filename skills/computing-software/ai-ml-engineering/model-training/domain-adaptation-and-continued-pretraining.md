---
id: computing-software.ai-ml-engineering.model-training.domain-adaptation-and-continued-pretraining
name: domain-adaptation-and-continued-pretraining
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, domain-adaptation, continued-pretraining, dapt, tapt, catastrophic-forgetting]
level: practitioner
status: draft
description: "Adapt pretrained models to a new domain: continued pretraining (DAPT/TAPT) on unlabelled in-domain text, unsupervised adaptation, data mixing to limit forgetting, and evaluation."
sources:
  - https://arxiv.org/abs/2004.10964
  - https://huggingface.co/learn/llm-course/chapter7/3
  - https://arxiv.org/abs/1505.07818
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Domain adaptation and continued pretraining

When target data (legal contracts, clinical notes, code in a niche language, satellite images) differs from pretraining data, fine-tuning on a small labelled set leaves performance on the table.

## Continued pretraining (DAPT / TAPT)
Keep training the base model with its original self-supervised objective on unlabelled in-domain data, then fine-tune on the task.
- **DAPT**: large in-domain corpus (GBs). **TAPT**: the task's own unlabelled text (cheap, surprisingly effective). Gururangan et al. (2020) found both help and combine well.
```python
from transformers import AutoModelForMaskedLM, DataCollatorForLanguageModeling, Trainer, TrainingArguments
model = AutoModelForMaskedLM.from_pretrained("roberta-base")
collator = DataCollatorForLanguageModeling(tok, mlm_probability=0.15)
Trainer(model=model, args=TrainingArguments("dapt", learning_rate=5e-5, num_train_epochs=1, warmup_ratio=0.06,
        per_device_train_batch_size=32, bf16=True), train_dataset=tokenized_domain_text, data_collator=collator).train()
```
Decoder LLMs: same idea with causal LM loss (`mlm=False`), often with LoRA for cost.

## Limit catastrophic forgetting
- Mix in 5-30% general-domain data (replay) during continued pretraining.
- Lower peak LR than original pretraining (rewarm then decay); short warmup.
- For LLMs, keep instruction-following: continued pretraining a chat model erodes chat behaviour; either adapt the base model and re-instruct, or interleave instruction data.
- Evaluate general benchmarks before/after to quantify forgetting.

## Vocabulary
Domain terms split into many sub-tokens reduce efficiency. Extending the tokenizer (`tok.add_tokens`, `model.resize_token_embeddings`) requires enough continued pretraining for new embeddings to learn; initialise new embeddings as the mean of their sub-token embeddings.

## Unsupervised domain adaptation (labels only in source)
- Domain-adversarial training (DANN, gradient reversal layer), feature alignment (CORAL, MMD), self-training with confident pseudo-labels on target data.
- Test-time adaptation (e.g. updating BN stats on target batches) for vision under covariate shift.
- Importance weighting when shift is covariate-only: weight source samples by a domain classifier's p(target|x)/p(source|x).

## Measuring shift and gains
- Domain classifier AUC between source and target features: near 0.5 means little shift.
- Always keep a labelled in-domain test set, even small, for the final decision.
- Compare: (a) fine-tune only, (b) TAPT + fine-tune, (c) DAPT + fine-tune, same budgets and seeds.

## Verify
Masked-LM / LM perplexity on held-out domain text should drop after continued pretraining while general-domain perplexity rises only slightly; downstream task metric improves over fine-tune-only across seeds.
