---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-configuration-basics
name: grafana-mimir-configuration-basics
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [configuration, yaml, cli-flags, common-config, config-validation]
level: practitioner
status: docs-checked
description: "Covers Mimir configuration via YAML and CLI flags, the common block and its precedence order, single-file practice and mimir -modules validation."
sources: ["https://grafana.com/docs/mimir/latest/configure/about-configurations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mimir configuration basics

Mimir is configured with a YAML file or CLI flags; the file is preferred. `mimir -help` shows the common flags, `mimir -help-all` all of them. The startup configuration cannot change at runtime; the separate runtime configuration is reloaded dynamically. Inspect live state with the `/config` and `/runtime_config` endpoints.

## The common block

Settings repeated across components, such as the object storage backend, go in `common` or `-common.*` flags. Common values are applied first, so specific values override them.

```yaml
common:
  storage:
    backend: s3
    s3:
      region: us-east
      bucket_name: mimir
blocks_storage:
  s3:
    bucket_name: mimir-blocks
```

Precedence, each overriding the previous: YAML common, YAML specific, CLI common, CLI specific.

## Operational advice

Use one configuration file for all replicas and all components. Parameters that look single-component may be used elsewhere, and passing an ingester setting to a querier is harmless because it is ignored. The usual use of CLI flags is `-target` to run microservices.

## Validate

```sh
mimir -modules -config.file <path-to-config-file>
```

Exits with code zero and prints the available modules when the file is valid, so it suits CI.

## Checked

Confirmed against the page: YAML versus flags, `-help` and `-help-all`, startup versus runtime configuration, `/config` and `/runtime_config`, common block and precedence order, single-file advice, `-target`, `mimir -modules` validation. Nothing removed.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir about-configurations page (grafana/mimir main), read in full.
