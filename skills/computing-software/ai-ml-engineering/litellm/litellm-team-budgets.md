---
id: computing-software.ai-ml-engineering.litellm.litellm-team-budgets
name: litellm-team-budgets
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, team-budget, budget-duration, budget-exceeded]
level: practitioner
status: docs-checked
description: "Give a team a max_budget that resets on a budget_duration, create keys for it, and read the budget-exceeded error."
sources:
  - https://docs.litellm.ai/docs/proxy/team_budgets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisite: a Postgres database.

1. Create a team with `max_budget` (the dollar amount the team may spend) and `budget_duration` (how often the budget resets), via the API or Admin UI. The response carries `team_id`, `max_budget`, `budget_duration` and `budget_reset_at`.

Possible `budget_duration` values:

- "1s": every second
- "1m": every minute
- "1h": every hour
- "1d": every day
- "30d": every month

2. Create a key with that `team_id`; the team budget applies to it.

3. Test: once the team's spend passes the budget, the next request returns HTTP 422:

```
{"error": {"message": "Budget has been exceeded! Team=<team_id> Current cost: 3.5e-06, Max budget: 1e-09",
           "type": "budget_exceeded", "param": null, "code": "422"}}
```

To return 429 instead, set `budget_exceeded_status_code: 429` under `litellm_settings`.

Default budget for auto-created JWT teams: with JWT auth and `team_id_upsert: true` under `litellm_jwtauth`, newly created teams can receive defaults from `litellm_settings.default_team_settings`, a list entry keyed by `team_id` (for example `default-settings`).

Monitoring: with `success_callback: ["prometheus"]` and `failure_callback: ["prometheus"]` in litellm_settings, the metric `litellm_remaining_team_budget_metric{team_alias=...,team_id=...}` tracks the remaining team budget.

For per-model TPM/RPM limits across all keys in a team, see the team model rate limit docs.

## Checked

2026-11-03. Confirmed on the team budgets page (docs.litellm.ai/docs/proxy/team_budgets): Postgres prerequisite, max_budget, budget_duration values, the response fields, the 422 budget_exceeded error, budget_exceeded_status_code 429, default_team_settings with team_id_upsert, and the Prometheus callbacks and litellm_remaining_team_budget_metric. Removed a parenthetical the page does not state.

Method: documentation only; no commands were run.
