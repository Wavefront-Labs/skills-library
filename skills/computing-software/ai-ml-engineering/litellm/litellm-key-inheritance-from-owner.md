---
id: computing-software.ai-ml-engineering.litellm.litellm-key-inheritance-from-owner
name: litellm-key-inheritance-from-owner
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, virtual-keys, allowed-routes, key-owner]
level: sme
status: docs-checked
description: "What a virtual key inherits from its owning user (models, routes, MCP, limits) and how to override it on the key."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A key's owner is whoever its `user_id` points at, which is not always the creator. /key/generate stamps the caller's user_id automatically only when the caller is not a proxy admin; a proxy admin must pass user_id explicitly.

Inheritance differs per surface:

- Models: nothing when the key belongs to a team. On a key with no team_id, the owner's models list applies on top of the key's own list, and `no-default-models` on the owner denies everything outside a team. Override by setting `models` on the key (or `all-team-models`).
- Management routes (/key/*, /user/*, /team/*): the owner's role in full. If the owner is proxy_admin, every non-admin route restriction is skipped and the key can manage keys, users and teams. Override with `allowed_routes` on the key, which is enforced for every role.
- MCP servers and tools: the owner's MCP entitlement as a ceiling, never a grant; an empty key list inherits the team's servers unless `require_key_mcp_access_defined` is on. Admin ownership grants no MCP access at all.
- Budgets and rate limits: the owner's tpm_limit and rpm_limit whenever set, and the owner's max_budget for keys with no team. Override by setting the same fields on the key, or use a service account key to apply team limits only.

Model access and MCP access are always evaluated against the key row itself, while management-route access is decided by the owning user's role. So a key owned by a proxy admin can call admin routes.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/virtual_keys (What a key inherits from its owner section)
