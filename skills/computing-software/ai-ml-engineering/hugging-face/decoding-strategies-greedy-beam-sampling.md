---
id: computing-software.ai-ml-engineering.hugging-face.decoding-strategies-greedy-beam-sampling
name: decoding-strategies-greedy-beam-sampling
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, decoding-strategies, top-p-sampling, beam-search, temperature]
level: practitioner
status: gated
description: "Choose generate() decoding in transformers: greedy, beam search, sampling with temperature, top-k, top-p and min-p, repetition penalties, and settings per task."
sources:
  - https://huggingface.co/docs/transformers/generation_strategies
  - https://huggingface.co/blog/how-to-generate
  - https://huggingface.co/docs/transformers/main_classes/text_generation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decoding strategies

## The options
| Strategy | Settings | Good for |
|---|---|---|
| Greedy | `do_sample=False, num_beams=1` | short factual answers, classification-style outputs, deterministic tests |
| Beam search | `num_beams=4-5, early_stopping=True, length_penalty=1.0` | translation, summarisation with smaller seq2seq models |
| Sampling | `do_sample=True, temperature=0.7, top_p=0.9` | chat, creative text, diverse candidates |
| Min-p sampling | `do_sample=True, min_p=0.05, temperature=1.0` | keeps diversity while cutting junk tokens at high temperature |
| Contrastive search | `penalty_alpha=0.6, top_k=4` | less repetition in open-ended text. In transformers 5.20 a plain call logs "Contrastive Search was moved to a `custom_generate` repo: https://hf.co/transformers-community/contrastive-search" and raises `ValueError` unless you pass `custom_generate=...` and `trust_remote_code=True`; that remote-code path was not run here (gated: unconfirmed, source is paywalled or blocked) |

```python
out = model.generate(**inputs, max_new_tokens=256, do_sample=True, temperature=0.7, top_p=0.9,
                     repetition_penalty=1.05, pad_token_id=tok.eos_token_id)
text = tok.decode(out[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)   # only new tokens
```

## What the knobs do
- `temperature`: divides logits; < 1 sharpens, > 1 flattens. 0 is not allowed with sampling (checked: `ValueError: temperature (=0.0) has to be a strictly positive float`); use greedy.
- `top_k`: keep the k most likely tokens. `top_p`: keep the smallest set with cumulative probability p. Applied after temperature.
- `repetition_penalty` (1.0-1.2) and `no_repeat_ngram_size` (e.g. 3) fight loops; too high hurts fluency and breaks code/data with legitimate repeats.
- `max_new_tokens` (not `max_length`, which counts the prompt too; if both are set `max_new_tokens` wins and a warning is logged, checked).
- `num_return_sequences=n` with sampling for n candidates (rerank or self-consistency).

## Model defaults
Many instruct models ship a `generation_config.json`. Read from the Hub: Llama-3.2-1B-Instruct (unsloth copy) has `do_sample=True, temperature=0.6, top_p=0.9`; Qwen2.5-7B-Instruct has `do_sample=True, temperature=0.7, top_p=0.8, top_k=20, repetition_penalty=1.05`. `generate()` uses it unless you override. A model without one (checked on a fresh GPT-2) has only the token ids, so it decodes greedily. Print `model.generation_config` before assuming greedy.

## Choosing
- Instruction-following LLMs: sampling with the model's recommended settings (see its `generation_config.json`); greedy can loop on long outputs.
- Evaluation/benchmarks: greedy (or fixed seed sampling) for reproducibility; report settings.
- Beam search with large LLMs: memory grows with the number of beams and it is rarely used for chat; not measured here.
- Structured output (JSON): greedy or low temperature plus constrained decoding (grammar/JSON-schema logits processors, e.g. Outlines).

## Gotchas
- Sampling parameters under greedy are ignored with a warning (transformers 5.20: "The following generation flags are not valid and may be ignored: ['temperature']").
- Batched generation needs left padding and an attention mask, or outputs are corrupted (checked: right-padded batch output differs from per-prompt output and a warning is logged).
- Set a seed (`transformers.set_seed`) for reproducible sampling (checked: same seed gave identical sampled ids).

## Verify
Generate for a fixed prompt set under each candidate setting and score with a task metric or human review; don't tune by eyeballing one prompt.
