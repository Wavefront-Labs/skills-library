---
id: computing-software.ai-ml-engineering.llm-application-engineering.model-version-pinning-and-deprecation
name: model-version-pinning-and-deprecation
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, model-deprecation, model-pinning, model-lifecycle, model-migration, llm-ops]
level: practitioner
status: docs-checked
description: "Manage LLM model lifecycles: pinning exact model ids, tracking deprecation and retirement dates, config-driven model selection, migration runbooks and fallbacks."
sources:
  - https://docs.claude.com/en/docs/about-claude/model-deprecations
  - https://docs.claude.com/en/docs/about-claude/models/overview
  - https://platform.openai.com/docs/deprecations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Model version pinning and deprecation migrations

## Pin
- Use exact model ids in production config (the dated or exact id from the models overview, not an alias), not "latest" aliases that can change behaviour underneath you.
- Keep the model id in configuration (per route), not scattered through code, so a migration is a config change plus eval.
- Record model id and prompt version with every logged request.

## Track lifecycle
- Providers publish deprecation then retirement dates; after retirement, requests fail. Anthropic notifies customers with active deployments by email and in the docs, with at least 60 days' notice before retiring a publicly released model. Keep an inventory of every route's model.
- Query the Models API (`GET /v1/models`) in CI. Each model has a `lifecycle` of `active`, `deprecated` (callable for existing users, closed to new adopters) or `retired` (requests naming it fail), plus `deprecated_at` and a scheduled retirement date that can be revised.
- Calendar: start migration as soon as a deprecation is announced; evals and prompt changes take time.

## Migration runbook
1. Pick the successor; read the vendor's migration notes for API changes.
2. Run evals old vs new; fix prompts; re-tune effort and max_tokens.
3. Re-baseline cost (check the vendor's pricing page; tokenizers and prices can change).
4. Canary, monitor quality/latency/refusals, then switch default; keep rollback config until stable.

## Fallbacks
Configure a fallback model for outages or refusals (provider-side fallback options where available, or client-side retry on another model). Test the fallback path periodically; prompts must work on both.

## Verify
- [ ] Inventory lists each route, model id, deprecation date (if any), owner; CI fails on retired ids.

## Checked
2026-11-01. Confirmed on the Anthropic model deprecations page (email and docs notification, at least 60 days' notice) and the models overview (Models API `GET /v1/models`, `lifecycle` values and their meanings, `deprecated_at`, scheduled retirement date). Removed: specific model ids. The OpenAI deprecations page is listed as a further source for that provider and was not used for specifics.
Method: documentation only; no commands were run.
