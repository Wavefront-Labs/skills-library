---
id: computing-software.ai-ml-engineering.hugging-face.logits-processors-and-constrained-generation
name: logits-processors-and-constrained-generation
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, logits-processor, constrained-generation, bad-words-ids, force-words, sequence-bias, generate]
level: practitioner
status: gated
description: "Shape Transformers generation with logits processors: bad_words_ids, sequence_bias, force_words_ids with constrained beam search, custom LogitsProcessor classes and grammars."
sources:
  - https://huggingface.co/docs/transformers/internal/generation_utils#logitsprocessor
  - https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
  - https://huggingface.co/blog/constrained-beam-search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Logits processors and constrained generation

At each decoding step, `generate()` runs a list of **logits processors** that modify next-token scores before selection (temperature, top-p, repetition penalties are all processors).

## Built-in constraints via generation arguments
```python
bad = tok(["damn", " damn"], add_special_tokens=False).input_ids
out = model.generate(**inputs, bad_words_ids=bad, max_new_tokens=50)            # ban token sequences
bias = {tuple(tok(" Paris", add_special_tokens=False).input_ids): 5.0}
out = model.generate(**inputs, sequence_bias=bias)                              # boost or penalise (negative)
force = tok([" scikit-learn"], add_special_tokens=False).input_ids
out = model.generate(**inputs, force_words_ids=force, num_beams=5)              # must appear; needs beam search. In transformers 5.20 this raises ValueError (see below)
```
- Tokenise words with and without a leading space: `"word"` and `" word"` are different tokens in BPE vocabularies (checked with GPT-2: `[4775]` versus `[1573]`; `"damn"` is two tokens `[11043, 77]`, so `bad_words_ids` takes token-id sequences).
- `force_words_ids` uses constrained beam search. In transformers 5.20 that was moved out of core: the call above logs "Constrained Beam Search was moved to a `custom_generate` repo: https://hf.co/transformers-community/constrained-beam-search" and raises `ValueError: Constrained Beam Search requires trust_remote_code=True in your generate call`. The remote-code route was not run here (gated: unconfirmed, source is paywalled or blocked); on older releases it ran in core and accepted disjunctive lists (`[[ids_a, ids_b]]` = any of). `bad_words_ids`, `sequence_bias` and custom processors still run in core.
- Others (names taken from the generation docs; not exercised here): `suppress_tokens`, `begin_suppress_tokens`, `forced_bos_token_id`, `forced_eos_token_id`, `min_new_tokens`, `exponential_decay_length_penalty`.

## Custom processor
```python
from transformers import LogitsProcessor, LogitsProcessorList
class OnlyDigits(LogitsProcessor):
    def __init__(self, allowed_ids): self.mask = None; self.allowed = allowed_ids
    def __call__(self, input_ids, scores):
        if self.mask is None:
            self.mask = torch.full_like(scores[0], float("-inf")); self.mask[self.allowed] = 0
        return scores + self.mask
digit_ids = [tok.convert_tokens_to_ids(str(d)) for d in range(10)] + [tok.eos_token_id]
out = model.generate(**inputs, logits_processor=LogitsProcessorList([OnlyDigits(digit_ids)]))
```
- `scores` shape `(batch * num_beams, vocab)`; return modified scores, do not use in-place ops on shared tensors. Checked: the `OnlyDigits` processor above made a tiny random GPT-2 emit only digit ids (`555555`), `bad_words_ids` removed the greedy first token, and `sequence_bias={(5,): 100.0}` forced token 5.
- Custom processors run after the built-in ones created from `GenerationConfig`.
- Stopping logic belongs in `StoppingCriteria`, not processors.

## Structured output (JSON / regex / grammar)
Token masks from a grammar are the robust way to force valid JSON:
- Libraries such as `outlines`, `lm-format-enforcer` and `xgrammar` plug into generation as logits processors, and vLLM/TGI have built-in guided decoding; their current API names change between releases, so read their docs rather than copying a call from here (not run here).
- Validate output with the schema anyway.

## Gotchas
- Banning tokens can make the model produce odd spellings to route around the ban (different tokenisation of the same word).
- Constrained beam search is slow and changes outputs a lot; for "must mention X", prompting plus validation is often enough.
- Batch generation with left padding: processors see padded `input_ids`; account for pad tokens in custom logic.
