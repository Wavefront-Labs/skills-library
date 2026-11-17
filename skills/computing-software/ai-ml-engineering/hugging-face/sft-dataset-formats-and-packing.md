---
id: computing-software.ai-ml-engineering.hugging-face.sft-dataset-formats-and-packing
name: sft-dataset-formats-and-packing
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, sft-packing, trl, sfttrainer, conversational-datasets, completion-only-loss, assistant-only-loss]
level: practitioner
status: verified
description: "Prepare SFT data for TRL: standard vs conversational and prompt-completion formats, chat templates, completion-only/assistant-only loss, packing strategies and max_length."
sources:
  - https://huggingface.co/docs/trl/main/en/dataset_formats
  - https://huggingface.co/docs/trl/main/en/sft_trainer
  - https://huggingface.co/docs/trl/main/en/reducing_memory_usage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SFT dataset formats, completion-only loss and packing

## Formats SFTTrainer understands
| Type | Columns | Example row |
|---|---|---|
| Language modeling | `text` | `{"text": "..."}` |
| Prompt-completion | `prompt`, `completion` | `{"prompt": "Translate: hi", "completion": "hola"}` |
| Conversational | `messages` | `{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}` |
| Conversational prompt-completion | `prompt`, `completion` as message lists | |
Conversational data is rendered with the tokenizer's chat template; make sure the tokenizer has one (base models may not: set `tokenizer.chat_template` or use a template-bearing tokenizer).

## What the loss covers
- Prompt-completion datasets: loss on the completion only by default (`completion_only_loss=None` resolves to completion-only for this format; checked: prompt tokens get label -100). `text` and plain `messages` rows train on the whole sequence.
- Conversational: `assistant_only_loss=True` trains only on assistant turns; requires a chat template with generation markers (`{% generation %}...{% endgeneration %}`). Without them TRL 1.16 raises `ValueError: The chat template is not training-compatible`. With them, label ids were -100 except on the assistant reply (ran on a tiny Llama, CPU).
- Training on user/system tokens wastes capacity and can teach the model to imitate users.

## Packing
```python
cfg = SFTConfig(output_dir="sft", max_length=4096, packing=True,
                padding_free=True, bf16=True)   # padding_free needs FlashAttention 2/3 per the SFTConfig docs (not run: no GPU)
```
- Packing concatenates examples into full-length sequences: big speedups when examples are short. `packing_strategy` defaults to `"bfd"` (best-fit decreasing, truncates overflow); the others are `"bfd_split"` and `"wrapped"`. Packed rows gain a `seq_lengths` column (observed: 8 rows of 6 tokens became one 48-token row), and `bfd` turns padding-free on regardless of the `padding_free` flag.
- With FlashAttention and position-id resets (`padding_free`/BFD packing), examples do not attend to each other. Naive packing without that lets attention cross example boundaries (usually tolerated in pretraining, worse for SFT).
- `max_length` truncates; check the length distribution first (`np.percentile(lengths, [50, 95, 99])`) to avoid cutting answers.

## Data hygiene
- Deduplicate, remove empty/refusal-only answers if undesired, balance tasks.
- Hold out an eval split from the same distribution plus a general benchmark.
- Keep a consistent system prompt policy between training and inference.

## Verify
- [ ] Decode a training batch and print which tokens have labels != -100 to confirm the masking.
- [ ] Throughput (tokens/s) with and without packing.
