---
id: computing-software.data-science-and-analytics.apache-superset.feature-flags
name: feature-flags
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [feature-flags, lifecycle, stable, deprecated, configuration]
level: intro
status: docs-checked
description: "Enable Superset features through the FEATURE_FLAGS dict and read flag lifecycle stages: development, testing, stable and deprecated."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/feature-flags.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn optional capabilities on safely.

Superset uses feature flags to control the availability of features, allowing gradual rollout and experimental features. Enable one in `superset_config.py`:

```python
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}
```

Lifecycle stages (each flag in `superset/config.py` carries an `@lifecycle` annotation, and the page is generated from those annotations):
- **Development**: experimental, under active development, may be incomplete or unstable; use only in development environments.
- **Testing**: feature complete but still being tested; usable but may have bugs.
- **Stable**: production-ready, safe for all deployments.
- **Deprecated**: scheduled for removal; migrate away.

A new flag in `config.py` is annotated with a description, `@lifecycle: development | testing | stable | deprecated`, an optional `@docs` link and an optional `@category: runtime_config | path_to_deprecation` for stable flags.

Runtime flags: `SEMANTIC_LAYERS` defaults to False. Hosts can supply runtime decisions through `IS_FEATURE_ENABLED_FUNC` and `GET_FEATURE_FLAGS_FUNC`, but changing static configuration still requires a restart. When `SEMANTIC_LAYERS` is disabled, semantic API routes return 404, and disabling it rolls back availability without deleting stored semantic layers, views or charts.

Check a flag's stage before enabling it in production.

## Checked

2026-11-08: read feature-flags.mdx in full (the generated flag table is not in the source). Removed claims not on the page: dict merged over defaults, restart for every edit, flags needing Celery, role-grant advice, example flags.
Method: documentation only; no commands were run.
