---
id: computing-software.ai-ml-engineering.litellm.litellm-key-budget-self-serve-and-restrictions
name: litellm-key-budget-self-serve-and-restrictions
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, self-serve-budget-policy, key-generation-settings, temp-budget-increase]
level: advanced
status: docs-checked
description: "Control who can change key budgets and who can create keys, and raise a key budget temporarily."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Temporary increase: use /key/update with a datetime expiry (an ISO date, not a duration):

```
curl -L -X POST 'http://localhost:4000/key/update' \
-H "Authorization: Bearer $LITELLM_API_KEY" \
-H 'Content-Type: application/json' \
-d '{"key": "sk-...", "temp_budget_increase": 100, "temp_budget_expiry": "2026-10-15"}'
```

Self-serve budget edits: by default any change to max_budget or budget_limits on /key/update, or to budget_duration on a key with a max_budget, needs a proxy admin, team admin or org admin; anyone else gets 403.

```
general_settings:
  self_serve_budget_policy: lower_only
```

- disabled (default): every budget change needs an admin.
- lower_only: owner may add budget windows, lower caps or clear budget_duration; raising caps, removing max_budget, dropping or renaming a window, and setting or changing budget_duration still need an admin.
- ceiling: lower_only plus raising or removing max_budget/budget_limits or setting a new budget_duration, if the owner could have created the key with that budget via /key/generate.

The owner is the caller whose user_id matches both the key's user_id and its created_by. A team member still needs the /key/update team member permission to edit a team key.

Restricting key creation:

```
litellm_settings:
  key_generation_settings:
    team_key_generation:
      allowed_team_member_roles: ["admin"]
      required_params: ["tags"]
    personal_key_generation:
      allowed_user_roles: ["proxy_admin"]
```

team_key_generation applies when team_id is in the request; personal_key_generation maps to Default Team in the UI. Roles: proxy_admin, proxy_admin_viewer, org_admin, internal_user, internal_user_viewer, team, customer.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/virtual_keys (temporary budget, self-serve policy and key generation settings sections)
