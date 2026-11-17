---
id: computing-software.search-and-information-retrieval.typesense.api-key-actions
name: api-key-actions
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [key-actions, resource-verb, permissions, typesense]
level: advanced
status: docs-checked
description: "Typesense API key actions in resource:verb form: collections, documents, aliases, synonym and curation sets, analytics, operations, models."
sources: ["https://typesense.org/docs/30.2/api/api-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API key actions

Actions follow `resource:verb` with verbs `create`, `delete`, `get`, `list`, `search` or `*`. A sample list from the docs:

- Collections: `collections:create|delete|get|list|*`.
- Documents: `documents:search|get|create|upsert|update|delete|import|export|*`.
- Aliases: `aliases:list|get|create|delete|*`.
- Synonym sets: `synonym_sets:list|get|create|delete|*` and items under `synonym_sets/items:list|get|upsert|delete|*`.
- Curation sets: `curation_sets:list|get|upsert|delete|*` and `curation_sets/items:...`. The two scopes are separate: `curation_sets:*` does not include `curation_sets/items:*`.
- Stopwords: `stopwords:list|get|create|delete|*`.
- Keys: `keys:list|get|create|delete|*`.
- Analytics: `analytics:*` family, `analytics/rules:...`, and `analytics/events:create`.
- Misc: `metrics.json:list`, `stats.json:list`, `debug:list`, and `*` for everything.
- Presets: `presets:get|list|upsert|delete`.
- Stemming dictionaries: `stemming/dictionaries:get|list|create|delete`.
- Operations: `operations/snapshot:create`, `operations/vote:create`, `operations/cache/clear:create`, `operations/db/compact:create`, `operations/reset_peers:create`, `operations/schema_changes:get`.
- Models: `conversations/models:create|get|list|upsert|delete` and `nl_search_models:...`.
- Config: `config:create` (POST /config).

Grant the narrowest set the application needs.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page API Keys (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
