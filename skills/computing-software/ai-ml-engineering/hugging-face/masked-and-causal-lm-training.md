---
id: computing-software.ai-ml-engineering.hugging-face.masked-and-causal-lm-training
name: masked-and-causal-lm-training
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, masked-language-modeling, causal-language-modeling, domain-adaptation, group-texts, perplexity, continued-pretraining]
level: practitioner
status: verified
description: "Adapt or pretrain language models with Trainer: tokenize and group_texts into blocks, MLM vs causal objectives, whole-word masking, perplexity evaluation and compute budgeting."
sources:
  - https://huggingface.co/learn/llm-course/chapter7/3
  - https://huggingface.co/learn/llm-course/chapter7/6
  - https://huggingface.co/docs/transformers/main/en/tasks/language_modeling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Masked and causal language model training

**Use cases:** domain-adapt an encoder (MLM on clinical/legal text before fine-tuning), continue pretraining a decoder on in-domain corpora, or train a small LM from scratch.

## Data: tokenize then pack into blocks
```python
block = 512
def tok(b): return tokenizer(b["text"])          # no truncation here
def group_texts(b):
    ids = sum(b["input_ids"], [])
    total = (len(ids) // block) * block
    out = {"input_ids": [ids[i:i + block] for i in range(0, total, block)]}
    out["attention_mask"] = [[1] * block for _ in out["input_ids"]]
    return out
tok_ds = ds.map(tok, batched=True, remove_columns=ds["train"].column_names)
lm_ds = tok_ds.map(group_texts, batched=True, remove_columns=tok_ds.column_names)   # drop the unpacked columns, row count changes
```
Add an EOS token between documents when tokenizing (`b["text"]` + eos) so the model sees boundaries.

Checked with bert-base-cased on 20 short documents and `block = 64`: tokenizing gives `input_ids`, `token_type_ids` and `attention_mask`. Without `remove_columns` on the second `map`, those columns keep their old length and `datasets` raises `pyarrow.lib.ArrowInvalid: Column 1 named token_type_ids expected length 27 but got length 20`, so the original snippet failed for BERT-style tokenizers. With the fix it produced 27 blocks of 64 tokens. Note that a tokenizer which adds BOS/EOS per document (BERT adds `[CLS]`/`[SEP]`) already marks boundaries.

## Objectives
- **MLM (encoders):** `DataCollatorForLanguageModeling(tokenizer, mlm_probability=0.15)`; `AutoModelForMaskedLM`. Whole-word masking helps for domain vocabulary split into subwords. In transformers 5.20 the separate `DataCollatorForWholeWordMask` class is gone (importing it fails); use `DataCollatorForLanguageModeling(tokenizer, whole_word_mask=True)`, whose examples must carry `offset_mapping` (tokenize with `return_offsets_mapping=True`, ideally also `return_special_tokens_mask=True`): checked, with offsets `Cardiomyopathy` was masked as one unit and without them the collator raised `IndexError`. Packed blocks from `group_texts` above would need the offsets packed too. The collator's `mask_replace_prob` (0.8) and `random_replace_prob` (0.1) arguments set the 80/10/10 rule.
- **Causal (decoders):** `mlm=False`; `AutoModelForCausalLM`; labels = inputs (shift is internal).

## Training
```python
args = TrainingArguments("out", per_device_train_batch_size=16, gradient_accumulation_steps=4,
                         learning_rate=5e-5, warmup_steps=0.03, lr_scheduler_type="cosine",   # warmup_steps < 1 is a ratio; `warmup_ratio=` raises TypeError in transformers 5.20
                         num_train_epochs=1, bf16=True, eval_strategy="steps", eval_steps=1000,
                         save_steps=1000, logging_steps=50)
```
Domain adaptation: lower LR than pretraining (1e-5 to 5e-5 is common practice, not tested here), one to a few epochs; watch for catastrophic forgetting on general benchmarks.

## Evaluate: perplexity
`math.exp(trainer.evaluate()["eval_loss"])` on held-out in-domain text (ran on a tiny randomly initialised BERT MLM: perplexity about 28,000, close to its 28,996-token vocabulary, as expected before training). Compare before and after; then confirm the downstream task actually improves (perplexity gains do not always transfer).

## Budgeting
Tokens processed = steps x batch x block x accumulation x devices. The Chinchilla paper (arXiv 2203.15556) reports that for compute-optimal training model size and training tokens should scale equally ("for every doubling of model size the number of training tokens should also be doubled"); the commonly quoted ratio of about 20 tokens per parameter is a derived rule of thumb, not stated in the abstract.

## Verify
- [ ] Inspect a decoded block to confirm document separators.
- [ ] Downstream fine-tune with and without adaptation on the same seed and splits.
