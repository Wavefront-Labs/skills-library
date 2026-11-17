---
id: computing-software.ai-ml-engineering.litellm.litellm-guardrails-tag-based-modes
name: litellm-guardrails-tag-based-modes
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, guardrails, tag-based-mode, user-agent]
level: sme
status: docs-checked
description: "Choose guardrail modes by request tag such as the User-Agent header, with default modes as fallback (Enterprise)."
sources:
  - https://docs.litellm.ai/docs/proxy/guardrails/quick_start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enterprise feature. Goal: run different guardrail modes for different clients. The docs' example: run pre-call checks for OpenWebUI but only mask in logs for Claude CLI.

The `mode` is a structure with `tags` (a map from a tag to a mode) and `default`. Both the default and each tag value accept either a single mode string or a list of modes.

Specification examples from the docs:

```
# single default mode
mode = Mode(
    tags={"User-Agent: claude-cli": "logging_only"},
    default="logging_only"
)

# multiple default modes
mode = Mode(
    tags={"User-Agent: claude-cli": "logging_only"},
    default=["pre_call", "post_call"]
)

# multiple modes on a tag value
mode = Mode(
    tags={"User-Agent: claude-cli": ["pre_call", "post_call"]},
    default="logging_only"
)
```

Config placement: it goes in the guardrail's `litellm_params` under `mode`, in a `guardrails` entry with a `guardrail_name`, such as `guardrails_ai-guard`.

Modes available are the ordinary event hooks: pre_call, post_call, during_call and logging_only.

Request parameter forms for choosing guardrails:

- Simple list: `"guardrails": ["aporia-pre-guard", "aporia-post-guard"]`
- Dictionary: `"guardrails": {"aporia-pre-guard": {"extra_body": {...}}}`, where the key is the `guardrail_name`.

The `guardrails` parameter can be passed to any proxy endpoint: /chat/completions, /completions, /embeddings.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/guardrails/quick_start (tag-based mode and specification sections)
