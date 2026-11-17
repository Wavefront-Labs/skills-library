---
id: computing-software.ai-ml-engineering.hugging-face.generation-scores-and-transition-scores
name: generation-scores-and-transition-scores
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, compute-transition-scores, output-scores, logprobs, generate, sequence-scores, confidence]
level: practitioner
status: verified
description: "Get token log-probabilities from generate(): return_dict_in_generate, output_scores vs output_logits, compute_transition_scores, sequence likelihood and scoring fixed candidates."
sources:
  - https://huggingface.co/docs/transformers/main/en/internal/generation_utils
  - https://huggingface.co/docs/transformers/main/en/main_classes/text_generation#transformers.GenerationMixin.compute_transition_scores
  - https://huggingface.co/docs/transformers/main/en/generation_strategies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Token scores and logprobs from generate()

**Uses:** confidence estimates, highlighting uncertain tokens, ranking candidate outputs, calibration of LLM classifiers, debugging sampling.

## Get per-token logprobs of generated tokens
```python
out = model.generate(**enc, max_new_tokens=50, do_sample=False,
                     return_dict_in_generate=True, output_scores=True)
trans = model.compute_transition_scores(out.sequences, out.scores, normalize_logits=True)
gen_tokens = out.sequences[:, enc["input_ids"].shape[1]:]
for tok_id, lp in zip(gen_tokens[0], trans[0]):
    print(f"{tokenizer.decode(tok_id)!r:15} logprob={lp.item():.3f} p={lp.exp().item():.2%}")
```
- `out.scores`: tuple (one per step) of processed scores, i.e. after temperature/top-k/top-p/repetition penalty. `output_logits=True` gives raw logits.
- `normalize_logits=True` applies log_softmax so values are log-probabilities.
- Beam search: pass `out.beam_indices` as the third argument of `compute_transition_scores` to follow the right beam (ran with `num_beams=3`); `out.sequences_scores` holds the beam scores (shape `(batch,)`), described in the docs as length-normalised with the default `length_penalty`. `output_logits=True` returned one logits tensor per step (ran).

## Sequence score
Sum of token logprobs (or mean, to avoid favoring short outputs). Exclude pad tokens after EOS (their transition scores are not meaningful: mask them using the generated ids).

## Scoring fixed candidates (no generation)
For classification-by-likelihood, run a forward pass on prompt + candidate and sum logprobs of candidate tokens:
```python
ids = tokenizer(prompt + candidate, return_tensors="pt").input_ids
logits = model(ids).logits[:, :-1]
lp = logits.log_softmax(-1).gather(-1, ids[:, 1:, None]).squeeze(-1)
cand_lp = lp[:, -n_candidate_tokens:].sum()
```
Watch tokenization boundaries: tokenize prompt and candidate together, then locate candidate tokens by offsets. The forward-pass snippet gives a tensor of shape `(1, n_tokens - 1)` (ran).

## Caveats
- Processed scores reflect the sampling transform, not the model's true distribution.
- Token probability is not calibrated correctness; calibrate on labeled data before using as confidence.

## Verify
- [ ] Greedy output token at each step equals the argmax of the corresponding score row (checked on a tiny random GPT-2; `compute_transition_scores` value for step 0 also equalled `log_softmax(out.scores[0])[token]` to 1e-5).
