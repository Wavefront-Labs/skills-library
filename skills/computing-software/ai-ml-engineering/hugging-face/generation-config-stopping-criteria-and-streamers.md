---
id: computing-software.ai-ml-engineering.hugging-face.generation-config-stopping-criteria-and-streamers
name: generation-config-stopping-criteria-and-streamers
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, generation-config, textstreamer, stopping-criteria, stop-strings]
level: practitioner
status: verified
description: "Control transformers generation with GenerationConfig files, eos and stop_strings, custom StoppingCriteria, and stream tokens with TextStreamer or TextIteratorStreamer."
sources:
  - https://huggingface.co/docs/transformers/main_classes/text_generation
  - https://huggingface.co/docs/transformers/internal/generation_utils#transformers.TextIteratorStreamer
  - https://huggingface.co/docs/transformers/generation_strategies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generation config, stopping criteria and streamers

## GenerationConfig
```python
from transformers import GenerationConfig
print(model.generation_config)                     # loaded from generation_config.json in the repo
gc = GenerationConfig.from_pretrained(repo)
gc.update(max_new_tokens=512, temperature=0.6, top_p=0.9, do_sample=True)
gc.save_pretrained("out/")                          # ship your defaults with the model
out = model.generate(**inputs, generation_config=gc)
```
kwargs passed to `generate()` override the config for that call (checked: a config with `max_new_tokens=5` gave 5 new tokens, and `generate(..., generation_config=gc, max_new_tokens=2)` gave 2; a saved config reloads with `temperature` 0.6). Setting generation parameters on `model.config` is not just ignored in transformers 5.20: `generate()` raises `ValueError: You have modified the pretrained model configuration to control generation`, so use `generation_config`.

## Stopping
- `eos_token_id` can be a list. Chat models often end turns with a special token (`<|eot_id|>`, `<|im_end|>`) that differs from the tokenizer's `eos_token`; include it or generation runs to `max_new_tokens`:
```python
eos = [tok.eos_token_id, tok.convert_tokens_to_ids("<|eot_id|>")]   # checked with a list of two ids: generation ended at the first of them
model.generate(**inputs, eos_token_id=eos, pad_token_id=tok.eos_token_id)
```
- `stop_strings=["\n\nUser:", "</answer>"]` with `tokenizer=tok` passed to generate: stops when the decoded text contains a string, even across token boundaries (checked: generation stopped after 2 new tokens of a 20-token budget; without `tokenizer=` it raises `ValueError`).
- `max_time=10.0` caps wall-clock seconds (checked with `max_time=0.01`: generation ended before the 100-token budget).
- Custom criteria:
```python
from transformers import StoppingCriteria, StoppingCriteriaList
class StopOnBalancedJSON(StoppingCriteria):
    def __call__(self, input_ids, scores, **kw):
        text = tok.decode(input_ids[0, prompt_len:])
        return torch.tensor([text.count("{") > 0 and text.count("{") == text.count("}")], device=input_ids.device)
model.generate(**inputs, stopping_criteria=StoppingCriteriaList([StopOnBalancedJSON()]))
```
Return a bool tensor per batch row (recent API; the class above ran in transformers 5.20); stopped rows are padded while others continue (not tested with a batch).

## Streaming
```python
from transformers import TextStreamer, TextIteratorStreamer
model.generate(**inputs, streamer=TextStreamer(tok, skip_prompt=True, skip_special_tokens=True))   # prints to stdout
streamer = TextIteratorStreamer(tok, skip_prompt=True, skip_special_tokens=True, timeout=30)
thread = threading.Thread(target=model.generate, kwargs={**inputs, "streamer": streamer, "max_new_tokens": 512})
thread.start()
for piece in streamer:            # yields text chunks as they decode; feed to SSE / websocket / Gradio
    send(piece)
thread.join()
```
Streamers support batch size 1 only (checked: `TextStreamer only supports batch size 1`). They emit text in chunks that avoid broken words/UTF-8 (not tested on multi-byte text). Checked on a tiny random GPT-2: `TextStreamer` stdout and the joined `TextIteratorStreamer` pieces both equal `tok.decode` of the new tokens.

## Gotchas
- Output includes the prompt tokens; slice `out[:, inputs["input_ids"].shape[1]:]` before decoding.
- `pad_token_id` warnings for models without a pad token: pass `pad_token_id=tok.eos_token_id`.
- Stop strings remain in the output (checked); strip them in post-processing.

## Verify
A test prompt that should stop at a stop string or end-of-turn token finishes well before `max_new_tokens` (check `out.shape`), and the streamed concatenation equals the non-streamed decode.
