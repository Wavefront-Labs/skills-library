---
id: computing-software.ai-ml-engineering.ollama.systemone-decision-api
name: systemone-decision-api
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [systemone, nimble, choice-questions, confidence, v1systemone]
level: advanced
status: docs-checked
description: "Score text with POST /v1/systemone: typed questions (choice, yes/no, score) answered with probabilities and confidence."
sources:
  - https://docs.ollama.com/api/systemone.md
  - https://docs.ollama.com/capabilities/decision.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: classify text with a decision model over HTTP.

`/v1/systemone` answers typed questions against a `state`. Models are System One decision models such as Nimble (local v0.35.0 or later; cloud models need v0.40.5 or later).

```
curl http://localhost:11434/v1/systemone -H 'Content-Type: application/json' -d '{
  "model": "nimble",
  "state": "Our checkout has returned 500 errors since 9am.",
  "questions": {
    "label": {
      "type": "choice",
      "instructions": "Which label fits this ticket?",
      "criteria": {"billing": "Payments and refunds", "bug": "Software errors", "account": "Login and account access"}
    }
  }
}'
```

The response has `answers` keyed by your question names, each with `type`, the selected `choice` (or answer or score), `probabilities` and `confidence`, plus `usage` with `input_tokens` and `output_tokens`. Example: `{"billing": 0.0125, "bug": 0.9781, "account": 0.0093}`.

Question types: `choice` (2 to 26 named options; returns the likeliest option and each probability), `noul` (yes/no; descriptions for `"false"` and `"true"`, returns P(true)) and `score` (2 to 10 ordered descriptions; returns the probability-weighted average of zero-based levels). `confidence` for choice and score shows how strongly one answer is favoured, 0 to 1, and does not guarantee correctness. `state` may be text or JSON.

Limits: one JSON response; streaming, video, tools and generation controls are unsupported. Locally, text and schema (excluding images) must fit in 64 KiB and the whole request in 32 MiB, and the input must fit the loaded context window; input is never truncated. Cloud models need a paid plan or usage credits and accept up to 64 questions (names up to 100 ASCII letters, digits, `_`, `.`, `-`), up to 4 images (4 MiB and 16 megapixels each, 8 MiB total), requests up to 13 MiB and input within the 65,536-token window. Clef models also take base64 PNG, JPEG or WebP `images` (no URLs); `state` is still required.

Errors documented: 400, 401, 402, 404, 413, 500.

## Checked

Method: 2026-11-08 read the decision guide in full and the System One reference header and error section (request schema part skimmed). Original claims matched; added question types, cloud billing and error codes.
