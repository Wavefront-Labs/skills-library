---
id: computing-software.ai-ml-engineering.hugging-face.batched-generation-left-padding
name: batched-generation-left-padding
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, batched-generation, left-padding, padding-side, generate, decoder-only, pad-token]
level: practitioner
status: verified
description: "Run batched generate() with decoder-only models correctly: left padding, pad_token setup, attention masks, decoding only new tokens, and when to use a serving engine instead."
sources:
  - https://huggingface.co/docs/transformers/main/en/llm_tutorial#wrong-padding-side
  - https://huggingface.co/docs/transformers/main/en/main_classes/text_generation
  - https://huggingface.co/docs/transformers/main/en/pad_truncation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Batched generation with left padding

**Why left:** decoder-only models generate from the last position. With right padding, the last position of shorter prompts is a pad token, so generation continues after padding and outputs degrade.

## Correct setup
```python
tok = AutoTokenizer.from_pretrained(name, padding_side="left")   # GPT-2's tokenizer has pad_token None, hence the eos fallback below
if tok.pad_token is None:
    tok.pad_token = tok.eos_token          # common for Llama-style models
model = AutoModelForCausalLM.from_pretrained(name, dtype=torch.bfloat16, device_map="auto")   # `torch_dtype=` still works but warns that it is deprecated

prompts = [tok.apply_chat_template([{"role": "user", "content": q}], tokenize=False,
                                   add_generation_prompt=True) for q in questions]
enc = tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(model.device)
out = model.generate(**enc, max_new_tokens=256, do_sample=False, pad_token_id=tok.pad_token_id)
texts = tok.batch_decode(out[:, enc["input_ids"].shape[1]:], skip_special_tokens=True)
```
- Pass `attention_mask` (via `**enc`) so pads are ignored; position ids are derived from the mask. Checked with a tiny random GPT-2 (greedy, `max_new_tokens=10`): with left padding the batched output of two prompts of different length equals each prompt generated alone; with right padding it does not, and transformers logs "A decoder-only architecture is being used, but right-padding was detected! For correct generation results, please set `padding_side='left'`".
- Slice off the prompt (all rows share the padded prompt length) before decoding.
- `add_special_tokens=False` when the chat template already adds BOS (avoids a double BOS).

## Training vs inference
Training usually uses right padding (labels align naturally); switch the tokenizer's `padding_side` for inference or keep two tokenizer instances.

## Encoder-decoder models
T5/BART pad on the right; padding side does not matter for the encoder.

## Throughput
- Sort prompts by length before batching to reduce padding.
- Static KV cache + `torch.compile` can speed up fixed-shape batches (not tested here).
- For production or large offline jobs use vLLM/TGI/SGLang (continuous batching, paged KV cache); `generate()` batching is fine for evals and small jobs.

## Verify
- [ ] Output for a prompt is identical whether generated alone or in a padded batch (greedy decoding; this held for the tiny random model, but small numeric differences between batch shapes can flip a near-tie on real models).
