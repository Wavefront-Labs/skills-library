---
id: computing-software.ai-ml-engineering.hugging-face.assisted-and-speculative-decoding
name: assisted-and-speculative-decoding
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, speculative-decoding, assisted-generation, prompt-lookup-decoding, draft-model]
level: practitioner
status: gated
description: "Speed up transformers generation with assisted (speculative) decoding: pick a draft model, prompt lookup decoding, universal assisted decoding, and when it does not help."
sources:
  - https://huggingface.co/docs/transformers/generation_strategies#speculative-decoding
  - https://huggingface.co/blog/assisted-generation
  - https://arxiv.org/abs/2211.17192
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assisted / speculative decoding

A small draft model proposes several tokens; the large model verifies them in one forward pass and accepts the longest correct prefix. Output distribution is identical to the large model's (exactly for greedy; for sampling with the rejection scheme, per the transformers docs and arXiv 2211.17192). Ran on a tiny Llama (assistant = copy of the target, CPU): greedy output with `assistant_model` and with `prompt_lookup_num_tokens=10` was token-identical to plain greedy. Speedup depends on hardware and acceptance rate and was not measured here; no fixed figure is claimed.

## Draft model
```python
target = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct", dtype=torch.bfloat16, device_map="cuda")   # `torch_dtype=` still works but warns "deprecated" on 5.20.2
draft = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct", dtype=torch.bfloat16, device_map="cuda")
out = target.generate(**inputs, assistant_model=draft, max_new_tokens=256)          # greedy
out = target.generate(**inputs, assistant_model=draft, do_sample=True, temperature=0.7)  # sampling
```
- The draft must share the tokenizer (same family) for classic assisted generation.
- Different tokenizers: universal assisted decoding, pass `tokenizer=target_tok, assistant_tokenizer=draft_tok` (docs example pairs a main model with `double7/vicuna-68m`). Passing `assistant_tokenizer` when both models share a tokenizer raises `ValueError: assistant_tokenizer is not required when the main and assistant models use the same tokenizer`. Llama 3.x gated models, GPU runs and a real different-tokenizer pair were not run (gated: unconfirmed, source is paywalled or blocked).
- The draft length is controlled by `num_assistant_tokens` and `num_assistant_tokens_schedule` on the assistant's generation config, and `assistant_confidence_threshold` stops drafting early on low confidence. On 5.20.2 all three read `None` on a fresh `GenerationConfig`, so the effective defaults are applied inside `generate`; check the docs for your version before relying on a default value.

## Prompt lookup decoding (no draft model)
```python
out = target.generate(**inputs, prompt_lookup_num_tokens=10, max_new_tokens=256)
```
Drafts by copying n-grams from the prompt and falls back to normal decoding when there is no match (docs). Very effective when output repeats input: summarisation, extraction, code editing, RAG answers quoting sources.

## When it helps and when not
- Helps: batch size 1-4, memory-bandwidth-bound decode, predictable text (code, structured or extractive answers), high acceptance rate.
- Doesn't help: large batches (GPU already compute-bound), very creative high-temperature sampling (low acceptance), draft too large relative to target (the docs say "significantly smaller"; the old "10-20x" figure was not sourced and is removed).
- Assisted generation does not support batched inputs in transformers (docs: "supports greedy search and sampling but not batched inputs", also true of prompt lookup and MTP); serving engines (vLLM, TGI, SGLang) implement speculative decoding (draft models, n-gram, EAGLE, Medusa heads) for production throughput.

## Measuring
Track acceptance rate and tokens/s. Rule from Leviathan et al. (arXiv 2211.17192, Theorem 3.8): expected walltime improvement = (1 - a^(k+1)) / ((1 - a)(k c + 1)) with acceptance rate a, k drafted tokens per step and draft/target cost ratio c (the numerator over (1 - a) is the expected tokens per step, accepted + 1). Example: a=0.8, k=4, c=0.05 gives 2.8x; with a draft as costly as the target (c=1) it gives 0.67x, a slowdown.

## Verify
With greedy decoding, outputs with and without the assistant must be identical token for token (small numeric differences in bf16 can rarely flip a token; use fp32 for the equality test). Then compare wall-clock latency on representative prompts.
