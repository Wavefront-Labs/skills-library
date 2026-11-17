---
id: computing-software.web-development.hasura.hasura-api-limits
name: hasura-api-limits
category: computing-software
field: web-development
product: hasura
tags: [hasura, security, api-limits, rate-limit, depth-limit]
level: advanced
status: docs-checked
description: "Apply depth, node, time, batch and rate limits to Hasura queries globally or per role with set_api_limits, including Redis for rate limiting."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/security/api-limits.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/api-reference/metadata-api/api-limits.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: guard against abusive or expensive requests.

Limit types: `depth_limit`, `node_limit`, `time_limit` (seconds), `batch_limit` and `rate_limit`, each with a `global` value and an optional `per_role` map.

Metadata API:

```json
{
  "type": "set_api_limits",
  "args": {
    "disabled": false,
    "depth_limit": { "global": 5, "per_role": { "user": 3 } },
    "rate_limit": {
      "per_role": { "user": { "unique_params": "IP", "max_reqs_per_min": 20 } },
      "global": { "unique_params": ["x-hasura-user-id"], "max_reqs_per_min": 100 }
    }
  }
}
```
Use `remove_api_limits` to clear. `disabled` defaults to `false`; with no limits set, none apply.

Facts: `unique_params` is `IP` or a list of session variables; rate limiting uses a sliding window; the Enterprise Edition needs `HASURA_GRAPHQL_RATE_LIMIT_REDIS_URL` (or `--rate-limit-redis-url`). Introspection queries are excluded from the depth limit and the admin role is exempt from all limits. A node is a field with a selection set. On Hasura Cloud Free and Professional projects the time limit is 60 seconds (error code `tenant-time-limit-exceeded`). Feature is for Pro, Enterprise and self-hosted EE.

Gotcha: with a `unique_params` value set, the role and the parameter together key the rate limit, so a different role from the same IP is not limited together.

## Checked

2026-11-04. Confirmed against the cited pages: security/api-limits and metadata-api api-limits pages: limit types, set/remove_api_limits, disabled default, unique_params, sliding window, Redis var, introspection and admin exemptions, 60 s Cloud limit. Removed or corrected: `api_limits.yaml` file name, load-balancer timeout gotcha and the Verify step.

Method: documentation only; no commands were run.
