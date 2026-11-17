---
id: computing-software.ai-ml-engineering.hugging-face.repetition-control-in-generation
name: repetition-control-in-generation
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, repetition-penalty, no-repeat-ngram-size, encoder-repetition-penalty, generate, decoding, degeneration]
level: practitioner
status: verified
description: "Stop repetitive LLM output in Transformers generate: repetition_penalty, no_repeat_ngram_size, sampling, and loops caused by templates or greedy decoding."
sources:
  - https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
  - https://huggingface.co/docs/transformers/generation_strategies
  - https://arxiv.org/abs/1909.05858
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repetition control

Greedy and beam decoding on small or base models degenerate into loops ("I think I think I think"). Fix the cause first, then use penalties sparingly.

## Causes to rule out
- **Wrong chat template** or missing EOS handling: instruct models loop when prompts are not formatted with `apply_chat_template(..., add_generation_prompt=True)` or when `eos_token_id` does not include the turn-end token (e.g. `<|eot_id|>`, `<|im_end|>`). Pass `eos_token_id=[tok.eos_token_id, tok.convert_tokens_to_ids("<|eot_id|>")]`.
- **Greedy decoding** (`do_sample=False`) on open-ended text: switch to sampling with the model's recommended `temperature`/`top_p` from its `generation_config.json`.
- **Base (non-instruct) model** used for chat.
- **Quantization too aggressive** (2-3 bit) is often blamed for looping; not tested here.

## Penalties
```python
out = model.generate(**inputs, do_sample=True, temperature=0.7, top_p=0.9,
                     repetition_penalty=1.1, no_repeat_ngram_size=0, max_new_tokens=512)
```
- `repetition_penalty` (CTRL paper): divides positive logits / multiplies negative logits of every token already in the context (prompt included) by the penalty (checked with `RepetitionPenaltyLogitsProcessor(2.0)`: scores `[2, -2, 1]` for context tokens 0 and 1 became `[1, -4, 1]`). 1.0 = off; 1.05-1.2 typical. Too high damages grammar and makes the model avoid needed words (names, code identifiers, JSON keys).
- `no_repeat_ngram_size=n`: hard-bans any n-gram from appearing twice (checked with n=2: after context `[1, 2, 1]` token 2 got `-inf`). Useful for summarisation with beam search (n=3); harmful for code, lists, data and long text where repeats are legitimate.
- `encoder_repetition_penalty`: for encoder-decoder models, rewards tokens from the source.
- Frequency/presence penalties (OpenAI-style) are not fields of `GenerationConfig` in transformers 5.20 (its penalty fields are `repetition_penalty`, `encoder_repetition_penalty`, `length_penalty`, `exponential_decay_length_penalty`, `penalty_alpha`, `diversity_penalty`); whether vLLM and TGI expose `frequency_penalty`/`presence_penalty` was not checked here.

## Choosing by task
| Task | Settings |
|---|---|
| Chat / creative | sampling, repetition_penalty 1.0-1.1 |
| Summarisation (seq2seq) | beam 4, no_repeat_ngram_size 3, length_penalty |
| Code / JSON | no n-gram bans; low temperature; penalty 1.0 |
| Extraction | greedy, short max_new_tokens, stop sequences |

## Diagnose a loop
Inspect token-level output (`tok.convert_ids_to_tokens`) to see where it starts; check whether EOS appears with high probability but is not in `eos_token_id`; use `output_scores=True, return_dict_in_generate=True` to look at top tokens at the loop point.

## Verify
Generate for a fixed prompt set across settings and measure distinct-n (unique n-gram ratio) along with task quality; pick the mildest setting that removes loops.
