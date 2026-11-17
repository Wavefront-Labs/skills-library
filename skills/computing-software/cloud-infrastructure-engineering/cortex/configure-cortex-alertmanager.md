---
id: computing-software.cloud-infrastructure-engineering.cortex.configure-cortex-alertmanager
name: configure-cortex-alertmanager
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [alertmanager, notifications, cortextool, storage-backend, sharding]
level: practitioner
status: docs-checked
description: "Configure the multi-tenant Cortex Alertmanager storage backend and upload per-tenant configuration with the API or cortextool."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/alert-manager-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cortex Alertmanager configuration follows Prometheus Alertmanager syntax because it shares the codebase.

Storage backend: since Cortex 1.8 the backend uses a new configuration pattern. Unset the old flags: `-alertmanager.storage` and `-<prefix>.configs.url`, because the old pattern still takes precedence if present. When using `-alertmanager.sharding-enabled=true`, the `local` and `configdb` backends are not supported.

Uploading per-tenant configuration is done through the Set Alertmanager configuration API or with Cortex Tools (`cortextool`). Download the latest cortextool; `cortextool --help-long` shows all commands and flags. The flow is:

1. Write the Alertmanager configuration YAML (for example `amconfig.yml`).
2. Upload it: `cortextool alertmanager load ./amconfig.yml --address=http://localhost:8095 --id=100 --key=<yourKey>`, where `--id` is the user/org ID and `--key` is your basic auth or API key. No error means success. The Set Alertmanager configuration API with curl is the alternative.
3. Verify with `cortextool alertmanager get` using the same address, id and key.

Each tenant has its own configuration, so the tenant ID header or flag must match the tenant whose alerts you are routing.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Configuring Notification using Cortex Alertmanager (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
