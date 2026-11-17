---
id: computing-software.ai-ml-engineering.hugging-face.chat-templates-apply-chat-template
name: chat-templates-apply-chat-template
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, tokenizers, chat-template, apply-chat-template, add-generation-prompt, assistant-mask, special-tokens]
level: practitioner
status: verified
description: "Format conversations correctly with apply_chat_template: generation prompts, tool definitions, training vs inference use, double-BOS bugs and assistant-only loss masks."
sources:
  - https://huggingface.co/docs/transformers/main/en/chat_templating
  - https://huggingface.co/learn/llm-course/chapter11/2
  - https://huggingface.co/docs/transformers/main/en/chat_templating_writing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chat templates and apply_chat_template

**Goal:** feed chat models the exact prompt format they were trained on - a wrong format quietly degrades output quality.

## Inference
```python
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
messages = [{"role": "system", "content": "You are terse."},
            {"role": "user", "content": "Capital of Peru?"}]
inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to(model.device)
out = model.generate(**inputs, max_new_tokens=64)
print(tok.decode(out[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```
- `add_generation_prompt=True` appends the assistant-turn header so the model answers instead of continuing the user message (Qwen2.5 output ends `<|im_start|>assistant
`; the generate/decode snippet ran with a tiny random Qwen2 model, so the plumbing is checked but not the answer quality).
- `tokenize=False` returns the formatted string - print it once to see exactly what the model receives.
- Tools: `apply_chat_template(messages, tools=[get_weather], ...)` renders function schemas (from type hints + docstrings) in the model's expected format.
- `continue_final_message=True` lets you prefill the start of the assistant answer.

## Double BOS
For templates that start with a BOS token the output already contains it, and tokenising that string again with `tok(text)` adds a second one (default `add_special_tokens=True`). Checked with Llama-3.2-1B-Instruct: `tok(text)` gives `[128000, 128000, 128006, ...]`, `tok(text, add_special_tokens=False)` and `apply_chat_template(..., tokenize=True)` give `[128000, 128006, ...]`. Qwen2.5 has no BOS token (`tok.bos_token` is None), so it is not affected. Either use `apply_chat_template(..., tokenize=True)` directly or call `tok(text, add_special_tokens=False)`.

## Training
- Apply the same template at training and inference. TRL's `SFTTrainer` does this for conversational datasets (a `messages` column, per the TRL SFT docs); `SFTConfig(assistant_only_loss=True)` needs `{% generation %}` keywords in the template, which TRL patches for some known families such as Qwen3.
- Loss only on assistant tokens: `apply_chat_template(..., return_assistant_tokens_mask=True, return_dict=True)` adds `assistant_masks` and works when the template marks assistant content with `{% generation %}` blocks (checked on the Qwen2.5 template, which has none: transformers logs "return_assistant_tokens_mask==True but chat template does not contain `{% generation %}` keyword"); otherwise use TRL's `assistant_only_loss` / completion-only options or mask by searching for the assistant header tokens.
- Base models have no chat template (or a generic one). When fine-tuning a base model into a chat model, set `tok.chat_template` deliberately and save it with the tokenizer, plus make sure the end-of-turn token is the generation EOS.

## Where it lives
`tokenizer_config.json` -> `"chat_template"` (Jinja2), or a separate `chat_template.jinja` (checked on the Hub: unsloth/Llama-3.2-1B-Instruct has `chat_template.jinja`, Qwen/Qwen2.5-7B-Instruct has no separate file). Inspect it; templates differ in system-prompt support, whitespace, and tool formats.

## Verify
- [ ] Printed formatted prompt matches the model card's documented format.
- [ ] Exactly one BOS in `input_ids`.
- [ ] Generation stops at the end-of-turn token (set `eos_token_id` / `generation_config` accordingly).
