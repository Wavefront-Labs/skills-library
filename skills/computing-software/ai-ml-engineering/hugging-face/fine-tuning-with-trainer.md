---
id: computing-software.ai-ml-engineering.hugging-face.fine-tuning-with-trainer
name: fine-tuning-with-trainer
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, trainer, trainingarguments, autotokenizer, automodelforsequenceclassification, datasets, dataset-map, datacollatorwithpadding, fine-tuning, eval-strategy, peft, lora, qlora, push-to-hub, save-pretrained, pipeline, gradient-accumulation, bf16, nlp, text-classification, evaluate]
level: practitioner
status: gated
description: "Fine-tune a Hugging Face Transformers model with Trainer: tokenise with datasets.map, dynamic padding, key TrainingArguments, eval/save strategy, LoRA via PEFT, save/push and pipeline inference."
sources:
  - https://huggingface.co/docs/transformers/index
  - https://huggingface.co/docs/datasets/index
  - https://huggingface.co/docs/peft/index
  - https://huggingface.co/docs/transformers/main_classes/trainer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fine-Tuning with the Hugging Face Trainer — from checkpoint to pipeline

**Goal:** fine-tune a pretrained Transformers model on your labelled data with sensible defaults, evaluate it properly, and reload it for inference.

## 1. Load model and tokenizer from the same checkpoint
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
ckpt = "distilbert-base-uncased"
tok = AutoTokenizer.from_pretrained(ckpt)
model = AutoModelForSequenceClassification.from_pretrained(
    ckpt, num_labels=3, id2label=id2label, label2id=label2id)
```
- The warning that some weights are "newly initialized" is expected: the classification head is new.
- Always pair tokenizer and model from the same checkpoint; a mismatched vocabulary trains without error and performs badly.
- Setting `id2label`/`label2id` now makes later pipeline output readable instead of `LABEL_0`.

## 2. Tokenise with datasets.map
```python
from datasets import load_dataset
ds = load_dataset("csv", data_files={"train": "train.csv", "validation": "val.csv"})
def tok_fn(b): return tok(b["text"], truncation=True, max_length=256)
ds = ds.map(tok_fn, batched=True, remove_columns=["text"])
ds = ds.rename_column("label_id", "labels")   # Trainer looks for "labels"
```
- `batched=True` is many times faster (fast tokenizers process lists). Add `num_proc=` for large sets.
- Do not pad here. `DataCollatorWithPadding(tok)` pads each batch to its longest item — dynamic padding — which saves a lot of compute versus `padding="max_length"`.
- `map` results are cached on disk keyed by the function; editing a closure variable may not invalidate the cache — pass `load_from_cache_file=False` while iterating.

## 3. TrainingArguments that matter
```python
from transformers import TrainingArguments, Trainer, DataCollatorWithPadding
args = TrainingArguments(
    output_dir="out", learning_rate=2e-5, num_train_epochs=3,
    per_device_train_batch_size=16, gradient_accumulation_steps=2,
    per_device_eval_batch_size=64, weight_decay=0.01,
    warmup_steps=0.06, lr_scheduler_type="linear",
    eval_strategy="epoch", save_strategy="epoch",
    load_best_model_at_end=True, metric_for_best_model="f1",
    save_total_limit=2, bf16=True, logging_steps=50,
    report_to="none", seed=42)
```
- `warmup_steps` takes an int (exact steps) or a float in [0, 1) read as a fraction of total steps; the old `warmup_ratio` argument is gone in transformers 5.x (`TypeError: unexpected keyword argument`; run on 5.20.2). Pin `transformers<5` if you must keep it.
- Encoder fine-tuning LRs are typically 1e-5 to 5e-5; LoRA adapters tolerate ~1e-4 to 3e-4.
- Effective batch = per-device × accumulation × number of GPUs.
- `eval_strategy` was named `evaluation_strategy` in older releases; on 5.20.2 the old name raises `TypeError`. `load_best_model_at_end=True` raises `ValueError` unless `save_strategy` matches `eval_strategy` (or is `"best"`).
- `bf16=True` on Ampere+; `fp16=True` on older GPUs. `gradient_checkpointing=True` trades compute for memory (the `TrainingArguments` docstring quotes about 20% slower). `bf16`/`fp16` need a supporting GPU (not run here: CPU only) (gated: unconfirmed, source is paywalled or blocked).
- `report_to` defaults to `"none"` in 5.x (`TrainingArguments(...).report_to == []`; older 4.x releases defaulted to every installed integration); set it explicitly when you want `"mlflow"` or `"tensorboard"`.

## 4. Metrics and training
```python
import numpy as np, evaluate
f1 = evaluate.load("f1")
def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=-1)
    return {"f1": f1.compute(predictions=preds, references=p.label_ids, average="macro")["f1"]}
trainer = Trainer(model=model, args=args, train_dataset=ds["train"],
                  eval_dataset=ds["validation"], processing_class=tok,
                  data_collator=DataCollatorWithPadding(tok),
                  compute_metrics=compute_metrics)
trainer.train()          # resume: trainer.train(resume_from_checkpoint=True)
```
`processing_class=` replaced the older `tokenizer=` argument; 5.20.2's `Trainer.__init__` has no `tokenizer` parameter. Keep a held-out test split that you evaluate once with `trainer.evaluate(ds["test"])` at the end.

## 5. Parameter-efficient fine-tuning (LoRA)
For large models, wrap with PEFT so only small adapter matrices train:
```python
from peft import LoraConfig, get_peft_model
cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type="SEQ_CLS",
                 target_modules=["q_lin", "v_lin"])   # names depend on architecture
model = get_peft_model(model, cfg); model.print_trainable_parameters()
```
`target_modules` names differ per architecture (e.g. `q_proj`, `v_proj` in Llama-style models) — print `model` to find them. QLoRA loads the base in 4-bit via `bitsandbytes` to fit large models on one GPU. Saving a PEFT model saves only the adapter; inference needs the base checkpoint too, or merge with `merge_and_unload()`. Memory sizing: computing-software.ai-ml-engineering.ml-platform-engineering.gpu-training-compute.

## 6. Save, share, infer
```python
trainer.save_model("final"); tok.save_pretrained("final")
trainer.push_to_hub()      # needs `hf auth login` or HF_TOKEN=<API_KEY>; `huggingface-cli` now only prints "deprecated and no longer works" (needs a Hub account, not run here) (gated: unconfirmed, source is paywalled or blocked)
from transformers import pipeline
clf = pipeline("text-classification", model="final")   # device=0 for the first GPU
clf(["great product", "never again"])
```
Check each base model's licence before pushing or deploying derivatives.

## Verify
- [ ] Tokenizer and model load from the same checkpoint; `labels` column exists and has the right dtype.
- [ ] Batches are dynamically padded (collator), not padded to `max_length`.
- [ ] Validation metric is computed every epoch and the best checkpoint is reloaded at the end.
- [ ] A held-out test set is evaluated exactly once.
- [ ] `pipeline(...)` on the saved directory returns human-readable labels matching expected predictions.
