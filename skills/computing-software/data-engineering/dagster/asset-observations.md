---
id: computing-software.data-engineering.dagster.asset-observations
name: asset-observations
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-observation, log-event, observable-source-asset, observe-sources, data-version]
level: practitioner
status: docs-checked
description: "Log AssetObservation events with metadata and partitions, which do not consume Dagster+ credits, and run observable source asset observations."
sources:
  - https://docs.dagster.io/guides/build/assets/metadata-and-tags/asset-observations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asset observations

Goal: record metadata about an asset without claiming it was mutated.

- An `AssetObservation` is not a materialization. Observations do not count toward Dagster+ credit usage; prefer them over materializations when reporting events from external systems.
- Log one from an op or asset with `context.log_event(...)`. The asset must be defined with `@asset` or already have materializations for the observation to display.
- Attach a metadata dict using `MetadataValue`; it shows in the event log and the Asset Activity table of **Asset Details**.
- Observing one slice (for example one day of a table) is done with the `partition` argument.

## Observable source assets
Use `observable_source_asset` with a function returning a `DataVersion` (the docs return a file hash). Each run emits an observation tagged with that version; downstream assets whose materialization used an older version are labeled in the UI, and `AutomationCondition` can rematerialize them. The **Observe sources** button shows only if some source asset has an observation function.

To observe on a schedule, include them in an asset job via `define_asset_job`. Gotcha: its `selection` must target only observable source assets; mixing regular assets and observable source assets raises an error.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/metadata-and-tags/asset-observations

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
