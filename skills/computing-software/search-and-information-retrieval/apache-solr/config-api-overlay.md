---
id: computing-software.search-and-information-retrieval.apache-solr.config-api-overlay
name: config-api-overlay
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [config-api, configoverlay, request-parameters-api, paramsets, set-property]
level: practitioner
status: docs-checked
description: "Edit Solr config at runtime with the Config API and Request Parameters API: configoverlay.json, set-property, add-requesthandler, paramsets, useParams, _invariants_."
sources:
  - https://solr.apache.org/guide/solr/latest/configuration-guide/config-api.html
  - https://solr.apache.org/guide/solr/latest/configuration-guide/request-parameters-api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# config-api-overlay

The Config API edits `solrconfig.xml` behavior without touching that file. Changes are stored in `configoverlay.json` and override `solrconfig.xml`. Endpoints are per collection: `/config` (merged effective config; GET to read, POST to run commands), `/config/overlay` (overlay only), `/config/params`.

Read one section by path (query, requestHandler, searchComponent, updateHandler, indexConfig and others), one component with `componentName=/select`, and add `expandParams=true` to see implicit handlers.

Commands: `set-property` and `unset-property` for predefined common properties, for example `{"set-property":{"updateHandler.autoCommit.maxTime":15000}}`; `set-user-property`; `add-`, `update-` and `delete-` for `requesthandler` and `searchcomponent`; `add-initparams`. Modified overlay or schema files reload the core.

Request Parameters API: `/config/params` with `set`, `update` (a putAll merge) and `delete`. Each paramset needs a name and is stored in `params.json` (ZooKeeper in SolrCloud). Use it by name in a request, or from a handler through `useParams`. Paramsets can hold `_invariants_` and `_appends_`.

Changing `params.json` updates params without a core reload.

## Checked

2026-11-04. Confirmed against the Config API and Request Parameters API pages: `configoverlay.json`, endpoints, commands, paramsets, `useParams`, `_invariants_` and `_appends_`, no reload for small parameter changes. Nothing removed.

Method: documentation only; no commands were run.
