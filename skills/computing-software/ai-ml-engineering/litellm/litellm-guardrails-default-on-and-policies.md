---
id: computing-software.ai-ml-engineering.litellm.litellm-guardrails-default-on-and-policies
name: litellm-guardrails-default-on-and-policies
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, guardrails, default-on, x-litellm-applied-guardrails]
level: practitioner
status: docs-checked
description: "Run a guardrail on every request with default_on: true and verify with the x-litellm-applied-guardrails header."
sources:
  - https://docs.litellm.ai/docs/proxy/guardrails/quick_start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `default_on: true` in the guardrail's config to run it on every request, without callers naming it:

```
guardrails:
  - guardrail_name: "aporia-pre-guard"
    litellm_params:
      default_on: true
```

Failure mode to know: default-on guardrails run even when the user specifies a different guardrail or an empty guardrails array, so a client cannot opt out by sending `"guardrails": []`.

Verify: the response headers include `x-litellm-applied-guardrails`, for example `x-litellm-applied-guardrails: aporia-pre-guard`.

Discovery: `GET /guardrails/list` returns the available guardrails and the optional `guardrail_info` you attach (supported parameters, description).

Further controls from the same page:

- Guardrail Policies group guardrails into reusable policies, enable or disable them for specific teams, keys or models, and inherit from existing policies and override specific guardrails.
- Per API key (Enterprise): set which guardrails run for one key when creating it.
- Model-level guardrails (Enterprise): attach guardrails to specific models in model_list, for example to stop PII reaching a hosted model but not an on-prem one.
- Disable team control (Enterprise): setting a team's `metadata` to `{"guardrails": {"modify_guardrails": false}}` stops the team turning guardrails off per call; an attempt such as `"metadata": {"guardrails": {"hide_secrets": false}}` returns a 403.
- Monitoring: connect a logging provider and check it for the guardrail trace of successes and failures.

Order is stable: editing a guardrail (for example a description-only PUT) no longer reorders execution.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/guardrails/quick_start (default_on, policies, per-key, model-level, team control and monitoring sections)
