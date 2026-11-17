---
id: computing-software.ai-ml-engineering.vllm.prompt-embeds
name: prompt-embeds
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [prompt-embeds, enable-prompt-embeds, embedding-inputs, base64-tensor]
level: advanced
status: docs-checked
description: "Send precomputed prompt embeddings to vLLM offline or through Completions and Chat APIs."
sources:
  - https://docs.vllm.ai/en/latest/features/prompt_embeds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: skip the tokenizer and feed token embeddings directly.

Normally text becomes token ids, then a lookup in the learned embedding matrix yields prompt embeddings. This feature lets you supply those embeddings yourself.

Offline: use the `prompt_embeds` field, a torch tensor of shape `(sequence_length, hidden_size)`.

Online: start the server with `--enable-prompt-embeds`, which enables both the Completions and Chat Completions APIs:

```bash
vllm serve meta-llama/Llama-3.2-1B-Instruct --runner generate \
  --max-model-len 4096 --enable-prompt-embeds
```

Completions API: add a `prompt_embeds` key to the JSON body as a base64-encoded torch tensor. If both `prompt_embeds` and `prompt` are sent, the embeds are returned first. No chat template is applied here, so the caller must embed the already-templated prompt (system prompt, role markers, generation prompt).

Chat Completions API: use content parts such as `{"type": "prompt_embeds", "data": "<base64_encoded_tensor>"}`, shape `(num_tokens, hidden_size)`, interleaved with text parts in any message. Here the part must hold only content, not a templated conversation, because the server applies the template; embedding a full conversation double-applies it. Assistant messages can pass one `prompt_embeds` part as `reasoning`. For multimodal models, the parts can mix with image parts. The reasoning tensor holds only the reasoning content; use a chat template that renders `reasoning` (or its alias `reasoning_content`).

Warning: the engine may crash if the embedding shape is wrong. Enable the flag only for trusted users.

## Checked

Method: 2026-11-08 read the prompt embeddings page in full. Offline, Completions and Chat claims matched; unchanged apart from adding the reasoning-part template note.
