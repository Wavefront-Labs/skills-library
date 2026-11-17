---
id: computing-software.ai-ml-engineering.llama-cpp.server-tokenize-detokenize-template
name: server-tokenize-detokenize-template
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, tokenize, detokenize, apply-template, tokenizer-endpoints]
level: practitioner
status: docs-checked
description: "Use /tokenize, /detokenize and /apply-template to inspect tokens and rendered chat prompts."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tokenizer and template endpoints

**POST /tokenize** turns text into token ids.

- `content` (required): the text.
- `add_special`: insert special tokens such as BOS, default false.
- `parse_special`: tokenize special tokens as such; default true. When false, special tokens are treated as plain text.
- `with_pieces`: return token pieces along with ids, default false.

The response is a JSON object with a `tokens` field. It holds either bare ids, or objects with `id` and `piece` when `with_pieces` is true. A piece is a string if it is valid unicode, otherwise a list of bytes.

```bash
curl http://localhost:9931/tokenize -H "Content-Type: application/json" \
  -d '{"content": "Hello world", "with_pieces": true}'
```

**POST /detokenize** takes `tokens`, the tokens to convert back to text.

**POST /apply-template** takes `messages` (required, same format as `/v1/chat/completions`), renders them through the server's chat template and returns the prompt string in the `prompt` field without running inference. The prompt can be edited (for example to insert "Sure!" at the start of the reply) and then sent to `/completion`.

These endpoints are useful for counting prompt length against the context size. For chat requests the dedicated counters are `/v1/chat/completions/input_tokens`, `/v1/responses/input_tokens` and `/v1/messages/count_tokens`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the llama.cpp server README sections for `/tokenize`, `/detokenize`, `/apply-template` and the token counting endpoints. Removed: the claim that `/detokenize` returns `content`, which the page does not state.
