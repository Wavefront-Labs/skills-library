---
id: computing-software.data-engineering.dagster.configuring-assets-in-the-ui
name: configuring-assets-in-the-ui
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-config, launchpad, config, pydantic, run-config]
level: practitioner
status: docs-checked
description: "Make a Dagster asset configurable with a Config subclass and override values from the Launchpad when materializing."
sources:
  - https://docs.dagster.io/guides/build/assets/configuring-assets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuring assets in the UI

Goal: adjust parameters (for example a lookback time window) when manually materializing assets, backfilling historical data or debugging a production issue from the UI. The page assumes familiarity with assets and Pydantic.

## Steps
1. Define a run configuration schema that inherits from the Dagster `Config` class. The docs example is a lookback window field (`lookback_window_days: int = 30` in the example snippet).
2. Accept it in the asset function through the `config` parameter (`def forecast_model(config: ForecastModelConfig)` in the snippet).
3. In the UI, on any page with a **Materialize** button, click the **options menu > Open launchpad**.
4. In the Launchpad you can scaffold the config, customize its values and manually materialize the asset. You can provide a run config file as YAML or JSON that overrides the default configuration for your asset.

## Notes
- Run configurations reference an `op`, which is the underlying compute associated with an asset.
- In the snippet, a default value makes the field optional; its comment says that without a default the user must provide a value.

Next steps on the page: connect to external APIs and databases with resources.

## Checked
2026-11-08. Confirmed against the Dagster docs page Configuring assets in the UI (raw markdown) and the config-schema example snippet it embeds. Removed unsupported claims that the config is keyed under the op, applies to one run only, and should be used instead of config for connections.
Method: documentation only; no commands were run.
