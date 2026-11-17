---
id: computing-software.ai-ml-engineering.litellm.litellm-guardrails-config-modes
name: litellm-guardrails-config-modes
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, guardrails, guardrail-mode, pre-call-post-call]
level: practitioner
status: docs-checked
description: "Define guardrails in config.yaml, pick event-hook modes (pre_call, post_call, during_call, logging_only) and apply them per request."
sources:
  - https://docs.litellm.ai/docs/proxy/guardrails/quick_start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Define guardrails in a top-level `guardrails` list. Each item has `guardrail_name` (required), `litellm_params` (required, including the guardrail's `mode`) and an optional `guardrail_info` dictionary returned by `GET /guardrails/list`.

Supported `mode` values (event hooks):

- `pre_call`: run before the LLM call, on input.
- `post_call`: run after the LLM call, on input and output.
- `during_call`: run during the LLM call, on input; like pre_call but in parallel with the LLM call. The response is not returned until the guardrail check completes.
- `logging_only`: scan logged input and output after the call finishes, on the background logging worker, without changing the client response or adding latency.

A list runs several modes: `mode: [pre_call, post_call]`.

Start the proxy with `litellm --config config.yaml --detailed_debug`.

Apply a guardrail by naming it in the request body:

```
"guardrails": ["aporia-pre-guard", "aporia-post-guard"]
```

A guardrail that blocks returns an HTTP 400 error body.

Dynamic parameters use the dictionary form (Enterprise): `"guardrails": {"aporia-pre-guard": {"extra_body": {"success_threshold": 0.9}}}`.

Return results to the caller: add `"include_guardrail_response": true` to get a top-level `guardrail_information` list on the response. It is `[]` when no guardrail ran, and only the exact JSON boolean true enables it.

Test without a model call by sending `mock_response` with the request.

## Checked

2026-11-03. Confirmed on the guardrails quick start (docs.litellm.ai/docs/proxy/guardrails/quick_start): guardrail_name, litellm_params and guardrail_info, the four mode values and their semantics, mode lists, the request-body guardrails list, dynamic parameters as an Enterprise feature, include_guardrail_response and guardrail_information, and mock_response testing.

Method: documentation only; no commands were run.
