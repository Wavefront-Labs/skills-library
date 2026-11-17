---
id: computing-software.ai-ml-engineering.litellm.litellm-fallback-access-and-budget-enforcement
name: litellm-fallback-access-and-budget-enforcement
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, enforce-fallback-model-access, enforce-fallback-budget, disable-fallbacks]
level: sme
status: docs-checked
description: "How fallbacks respect key model access and budget, how to turn that off, and how to disable fallbacks per request or key."
sources:
  - https://docs.litellm.ai/docs/proxy/reliability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Model access: the proxy applies the calling key's, team's and project's model access checks to every fallback target before it is tried, so a fallback never serves a model the caller could not call directly. A key created with `"models": ["openai-only"]` calling a failing gpt-5.6 gets the OpenAI error instead of a claude-sonnet-5 completion. Requests with no virtual key, such as health checks, are not restricted. If the access lookup itself fails, the fallback is skipped.

```
general_settings:
  enforce_fallback_model_access: false   # run every configured fallback whatever the caller's access
```

Failure mode: earlier releases ran a fallback even when the caller could not call the fallback model; if you rely on that, grant access to the fallback models or set the flag false.

Budget: the budget is checked once at authentication, against the requested model, so the proxy also re-checks the key's and user's budget against every fallback target. Over-budget targets are skipped; this needs no configuration. A user over max_budget can still call a free model, but if it fails they get its error rather than a billed fallback.

```
general_settings:
  enforce_fallback_budget: false
```

A team key does not inherit the key owner's personal max_budget unless `general_settings.apply_user_budget_to_team_keys` is set.

Disable fallbacks per request with `"disable_fallbacks": true` in the body, or per key with `"metadata": {"disable_fallbacks": true}`. Both cover every fallback for that request, including the mid-stream one when a stream fails before its first chunk on /chat/completions, /v1/messages or /v1/responses.

## Checked

Method: docs-checked 2026-11-09 against the full LiteLLM Fallbacks (proxy/reliability) page, Enforce Key Model Access, Enforce Budget and Disable Fallbacks sections.
