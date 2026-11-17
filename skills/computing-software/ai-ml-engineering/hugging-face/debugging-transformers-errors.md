---
id: computing-software.ai-ml-engineering.hugging-face.debugging-transformers-errors
name: debugging-transformers-errors
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers-debugging, transformers, error-messages, minimal-reproduction, forum-help, trainer-debugging]
level: practitioner
status: gated
description: "Debug Hugging Face Transformers failures the course chapter 8 way: read tracebacks bottom-up, check the pipeline piece by piece, build minimal repros and ask good questions."
sources:
  - https://huggingface.co/learn/llm-course/chapter8/1
  - https://huggingface.co/learn/llm-course/chapter8/4
  - https://huggingface.co/learn/llm-course/chapter8/5
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging Transformers errors and asking for help

## Read the traceback
Start from the **last line** (exception type and message), then walk up to the first frame in *your* code. Common messages:
| Message | Usual cause |
|---|---|
| `OSError: <id> is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'` (typo) / `OSError: You are trying to access a gated repo ... 401 Client Error` (gated or private repo, no token) | repo id typo, private/gated repo without token, no network (`HF_HUB_OFFLINE`); both messages seen on transformers 5.20.2, the older "Can't load config for 'x'" wording is not what a missing repo gives there |
| `ValueError: expected sequence of length 3 at dim 1 (got 8)` (ran) | unpadded batch: tokenizer without `padding`, or `default_data_collator` instead of `DataCollatorWithPadding` |
| `IndexError: index out of range in self` (Embedding; ran with id 99999 on a 30k-vocab BERT) | token ids >= vocab size: tokenizer and model mismatch, or added tokens without `resize_token_embeddings` |
| `Expected all tensors to be on the same device` | inputs not moved: `inputs.to(model.device)` (needs a GPU to reproduce, not run) (gated: unconfirmed, source is paywalled or blocked) |
| `CUDA error: device-side assert triggered` | label out of range (num_labels wrong, -100 handling) or ids out of vocab; rerun on CPU for a readable error: a label of 5 with `num_labels=2` gave `IndexError: Target 5 is out of bounds.` on CPU (ran); the CUDA message itself was not reproduced (gated: unconfirmed, source is paywalled or blocked) |
| `ValueError: The model did not return a loss from the inputs, only the following keys: logits` | `labels` key missing or misnamed in the batch (ran both: a dataset without `labels` and one with the column named `label_id`) |
| `KeyError: 'extra'` in Trainer | `remove_unused_columns=True` dropped a column your collator needs (ran with a custom collator reading a column that is not a model input; set `remove_unused_columns=False`) |

## Debug the training pipeline step by step (course 8.4)
```python
batch = next(iter(trainer.get_train_dataloader()))   # 1. does the collator produce tensors with the right keys/shapes? (all four steps ran on 5.20.2)
{k: v.shape for k, v in batch.items()}
tokenizer.decode(batch["input_ids"][0])             # 2. is the text what you expect?
outputs = trainer.model(**batch.to(trainer.model.device))   # 3. forward pass and loss
outputs.loss.backward(); trainer.create_optimizer(); trainer.optimizer.step()   # 4. one optimisation step
```
Then evaluation: `trainer.evaluate()` on a few examples and call `compute_metrics` on dummy predictions to check its shapes.

## Silent problems
- Loss not decreasing: overfit one small batch (repeat it for 50 steps); if loss does not go near 0, there is a bug (labels, LR, frozen params, wrong head).
- Metrics stuck at chance: label mapping (`id2label`), shuffled labels, `num_labels` mismatch, or evaluating with `model.train()`.
- On transformers 5.x the old "Some weights of ... were not initialized" warning is replaced by a load report table with `MISSING` (newly initialised, expected for a new classification head) and `UNEXPECTED` (checkpoint tensors that were dropped, harmless for a different head) rows; `MISSING` rows are unexpected when loading a fine-tuned checkpoint (wrong class or base model).

## Make a minimal reproduction
- Smallest model (`hf-internal-testing/tiny-random-*` repos or `sshleifer/tiny-*`), a few hard-coded examples, no private data.
- Pin and report versions: `transformers env` (ran on 5.20.2: prints a block to paste into the issue). `python -m transformers.commands.transformers_cli env` no longer exists there (`No module named 'transformers.commands'`); it was the 4.x form.
- Try latest release / main: `pip install -U transformers` or `pip install git+https://github.com/huggingface/transformers` before filing.

## Ask well
- Forum (discuss.huggingface.co) for usage questions; GitHub issues for bugs with a repro.
- Include: what you tried, full traceback as text (not screenshot), minimal code, versions, expected vs actual.
- Search existing issues by the error string first.

## Useful switches
`TRANSFORMERS_VERBOSITY=debug`, `transformers.logging.set_verbosity_info()`, `CUDA_LAUNCH_BLOCKING=1` for CUDA errors (not run: no GPU) (gated: unconfirmed, source is paywalled or blocked), `TrainingArguments(debug="underflow_overflow")` to find layers producing inf/nan (constructs on 5.20.2; detection itself not exercised).
