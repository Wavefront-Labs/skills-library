---
id: computing-software.ai-ml-engineering.litellm.litellm-context-window-pre-call-checks
name: litellm-context-window-pre-call-checks
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, enable-pre-call-checks, context-window-fallbacks, max-input-tokens]
level: advanced
status: docs-checked
description: "Reject or reroute over-long prompts before the provider call with enable_pre_call_checks, max_input_tokens and context_window_fallbacks."
sources:
  - https://docs.litellm.ai/docs/proxy/reliability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Failure mode: without `enable_pre_call_checks: true` in router_settings, requests are sent to the provider regardless of input token count, so context-window enforcement does not happen.

```
router_settings:
  enable_pre_call_checks: true
model_list:
  - model_name: gpt-6.1-sol
    litellm_params:
      model: openai/gpt-6.1-sol
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      max_input_tokens: 10   # override: reject prompts over 10 tokens
```

Both settings are required for a custom limit. Over the limit, LiteLLM raises ContextWindowExceededError with details like `Model=gpt-6.1-sol, Max Input Tokens=10, Got=306`.

For Azure deployments set `model_info.base_model` (for example `azure/gpt-4.1`) so the context size is known.

Same group: with pre-call checks on, deployments with smaller context windows are filtered out for a long prompt.

Different groups:

```
litellm_settings:
  context_window_fallbacks: [{"small-model": ["large-model", "claude-opus"]}]
```

Precedence after retries: a matching `context_window_fallbacks` chain for the requested group is used before later `order` levels and generic fallbacks. With no matching rule, the router tries later order levels, then generic fallbacks. A context rule for another group does not disable these routes. `num_retries: 0` disables sibling retries.

If the test prompt is rate limited by a small TPM quota, the proxy can report a context window error instead of the rate limit.

## Checked

Method: docs-checked 2026-11-09 against the full LiteLLM Fallbacks (proxy/reliability) page, context error precedence and pre-call checks sections.
