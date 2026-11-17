---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.stored-scripts-and-search-templates
name: stored-scripts-and-search-templates
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, stored-scripts, search-template, mustache]
level: practitioner
status: docs-checked
description: "Store mustache search templates with PUT _scripts, render them with _render/template and run them by id with params via _search/template."
sources:
  - https://www.elastic.co/docs/solutions/search/search-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stored scripts and search templates (Elasticsearch)

**Goal:** keep query bodies out of client code and let users pass only parameters.
- Create or update: `PUT _scripts/my-search-template {"script":{"lang":"mustache","source":{"query":{"match":{"message":"{{query_string}}"}},"from":"{{from}}","size":"{{size}}"}}}`. `lang` must be `mustache`; `source` takes the same parameters as a search request body. Putting the same id again updates it.
- Preview: `POST _render/template {"id":"my-search-template","params":{"query_string":"hello world","from":20,"size":10}}` returns `template_output`. Inline templates can be rendered with `source` instead of `id`. The endpoint is `_render/template`, not `_render/search_template`.
- Run: `GET my-index/_search/template {"id":"my-search-template","params":{"query_string":"hello world","from":0,"size":10}}`; the response has the same shape as a normal search. Several at once: `GET my-index/_msearch/template`.
- Read one: `GET _scripts/my-search-template`; list all stored scripts: `GET _cluster/state/metadata?pretty&filter_path=metadata.stored_scripts`; delete: `DELETE _scripts/my-search-template`.
- Templates are stored in cluster state and compiled in the template script context; settings that limit or disable scripts also affect search templates.
- Mustache helpers: default `{{from}}{{^from}}0{{/from}}`; `{{#url}}...{{/url}}` URL-encodes; `{{#join}}emails{{/join}}` concatenates (custom delimiter allowed); `{{#toJson}}tags{{/toJson}}` passes arrays or objects (write `source` as a string so the JSON stays valid); conditions `{{#cond}}...{{/cond}}` with else `{{^cond}}...{{/cond}}`; partials are not supported.
- Failure mode: a variable with no value in `params` renders as an empty string (a `match` on `""`), not an error.
- Failure mode: looping a list with `{{#items}}"x",{{/items}}` leaves a trailing comma and invalid JSON; add a `last` flag and `{{^last}},{{/last}}`.
- OpenSearch: not covered; its search-template pages could not be read.

## Verify
- [ ] Render shows the substituted query; the search returns the expected hits.

## Checked
Checked 2026-11-08 against the Elasticsearch page "Search templates". Only Elasticsearch was checked. Fixed: the render endpoint (was `_render/search_template`, page uses `_render/template`). Removed: the claim that hand-built templates let user input change query shape (not on the page).
Method: documentation only; no commands were run.
