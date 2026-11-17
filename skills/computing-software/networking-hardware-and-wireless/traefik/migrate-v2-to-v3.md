---
id: computing-software.networking-hardware-and-wireless.traefik.migrate-v2-to-v3
name: migrate-v2-to-v3
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, migration, v2-to-v3, defaultrulesyntax, v3-upgrade, rollout]
level: practitioner
status: docs-checked
description: "Migrate Traefik v2 to v3 in three steps using core.defaultRuleSyntax v2 for compatibility, then convert routing rules gradually."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/migrate/v2-to-v3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# migrate v2 to v3
The docs describe a low-risk path of three steps. Step 1: update the install configuration for changed options and test v3. Step 2: migrate production instances. Step 3: progressively migrate routing configuration.

For compatibility keep the v2 rule syntax at first:

```yaml
# install configuration
core:
  defaultRuleSyntax: v2
```
This lets existing v2 rules keep working while v3 is running. Step 3 of the guide removes this setting again once the routing configuration is migrated. A per-router `ruleSyntax` option also exists and inherits its default from `core.defaultRuleSyntax`.

Step 1 test from the guide: start the test instances; if there are no error logs you can proceed, otherwise follow the remaining migration options highlighted in the logs.

Gotchas: step 3 is optional and can be done later, because v3 is compatible with the v2 format for routing configuration; enable Traefik logs to see any deprecated option in use. The guide's end state is no deprecated warnings in the logs. Breaking changes are minimal and mainly in install options.

## Checked
2026-11-03. Confirmed against the Traefik v2 to v3 migration page: the three steps, `core.defaultRuleSyntax: v2`, removal of that setting in step 3, the log-based testing advice and the minimal-breaking-changes statement. Removed: the claim that per-router `ruleSyntax` is deprecated, the claim about regexp matchers behaving differently, the reference to a details page, and the replay-traffic Verify step.
Method: documentation only; no commands were run.

