---
id: computing-software.data-engineering.databricks.databricks-clean-rooms
name: databricks-clean-rooms
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-clean-rooms, privacy, delta-sharing, collaboration]
level: sme
status: docs-checked
description: "Run joint analysis with partners in Databricks Clean Rooms without exposing raw data: setup, assets, approved notebooks, output tables, and governance controls."
sources:
  - https://docs.databricks.com/aws/en/clean-rooms/
  - https://docs.databricks.com/aws/en/clean-rooms/create-clean-room
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Databricks Clean Rooms

**Goal:** two or more organisations analyse combined data (audience overlap, attribution, joint ML) where no party sees the others' raw rows.

## Prerequisites
- Each collaborator: Unity Catalog workspace, Delta Sharing (Databricks-to-Databricks) enabled, serverless compute available.
- Privileges: `CREATE CLEAN ROOM` on the metastore; collaborators exchange sharing identifiers.

## Flow
1. Creator creates the clean room (Catalog Explorer > Clean Rooms), adds collaborators by sharing identifier.
2. Each party adds **assets**: tables/views (often pre-aggregated or hashed-key views), volumes, and **notebooks** containing the agreed analysis.
3. Notebooks are reviewed; a party runs an approved notebook. It executes on serverless compute inside the clean room's isolated environment with read access to all assets.
4. Results are written to **output tables**, shared back to the runner (or designated party), not raw data.

## Design the assets
- Share views keyed on hashed identifiers (`sha2(lower(trim(email)), 256)`) with a salt agreed out-of-band.
- Remove unnecessary columns; aggregate where possible.
- Include threshold logic in notebooks (suppress groups under k individuals).

## Governance
- Every collaborator must approve a notebook before it can be run.
- Collaborators can see column names and types of shared tables, not the rows.

## Gotchas
- Output tables can still leak if the notebook returns row-level data; review notebook code like a contract.

## Verify
Run the approved overlap notebook: the output table contains only aggregates.

## Checked

- 2026-10-28: confirmed on the clean rooms overview and create pages (OpenSharing and serverless compute, collaborators see column names and types, notebook approval by all collaborators, output tables).
- Removed: `system.access.clean_room_events`, auto-approval rules, audit claims and the cross-cloud egress note (not in the fetched pages).

Method: documentation only; no commands were run.
