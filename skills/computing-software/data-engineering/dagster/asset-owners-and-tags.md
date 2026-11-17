---
id: computing-software.data-engineering.dagster.asset-owners-and-tags
name: asset-owners-and-tags
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, owners, tags, asset-metadata, team, key-value]
level: practitioner
status: docs-checked
description: "Attach owners (email or team:name) and string key-value tags to Dagster assets for organization, filtering and alerts."
sources:
  - https://docs.dagster.io/guides/build/assets/metadata-and-tags/index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asset owners and tags

Goal: record who is responsible for an asset and organize it for search.

## Owners
Pass `owners` to the asset. Each owner must be an email address or a team name prefixed `team:` (for example `team:data-eng`). With Dagster+ Pro, asset-based alerts can notify owners and permissions can apply to definitions users and teams own.

## Groups
Every asset belongs to exactly one group; group names can be nested to build a hierarchy rendered as nested boxes in the asset graph.

## Tags
Tags are string key-value pairs set with the `tags` argument, for example `{"domain": "marketing", "pii": "true"}`. They show in the UI and filter the Asset catalog. Keys and values must be strings. A tag with an empty-string value renders as a label rather than a key-value pair.

## Checked

2026-11-09. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/metadata-and-tags/index

Confirmed: owners format (email or team: prefix), one group per asset with nested names, string-only tags, empty-string tag rendered as a label, Dagster+ Pro alerts and permissions.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
