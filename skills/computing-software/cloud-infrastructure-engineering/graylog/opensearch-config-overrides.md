---
id: computing-software.cloud-infrastructure-engineering.graylog.opensearch-config-overrides
name: opensearch-config-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [opensearch-overrides, datanode-conf, allowlist-overrides, unsupported]
level: advanced
status: docs-checked
description: "Override OpenSearch settings in Data Node with an overrides properties file, and know which settings are allowlisted."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/data_node_configuration_overrides.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# opensearch config overrides

Overrides are unsupported by Graylog and should be tested outside production. Any override not on Graylog's allowlist raises a system warning notification.

Steps:
1. Create a Java properties file, one setting per line, for example:
   `cluster.routing.allocation.disk.watermark.low = 80%`
   `plugins.security.ssl.transport.enforce_hostname_verification = false`
2. Store it beside `datanode.conf` (default `/etc/graylog/datanode/`), for example `overrideconfig.conf`.
3. In `datanode.conf` set `opensearch_configuration_overrides_file` to its path.
4. Restart: `sudo systemctl restart graylog-datanode`.

Allowlisted properties include `cluster.routing.allocation.disk.watermark.*`. Allowlisted means tested with Graylog, not supported. Review the OpenSearch reference for each setting before use.

## Checked

2026-11-04. Confirmed against the Data Node Configuration Overrides page. Nothing removed.

Method: documentation only; no commands were run.
