---
id: computing-software.cloud-infrastructure-engineering.graylog.datanode-conf-settings
name: datanode-conf-settings
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [datanode-conf, opensearch-heap, password-secret, mongodb-uri, node-name]
level: advanced
status: docs-checked
description: "Key datanode.conf properties: password_secret, mongodb_uri, node_name, node_id_file, tiering credentials and skip_preflight_checks."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/data_node_configuration_file.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/configuration_settings.htm
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/debian_installation.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# datanode conf settings

Default location: `/etc/graylog/datanode/datanode.conf`.

Cluster properties:
- `password_secret` (required, no default): at least 64 characters, for example from `pwgen -N 1 -s 96`. It must be identical on all Graylog and Data Node nodes; changing it later invalidates sessions and encrypted values such as access tokens.
- `mongodb_uri` (default `mongodb://localhost/graylog`).
- `mongodb_version_probe_attempts` (default 0, retry indefinitely).
- `node_name`: set when the looked-up hostname is not what you want.
- `node_id_file` (default `data/node-id`): use an absolute path when started from init scripts.
- `config_location`: source directory for additional config files and certificates.
- `skip_preflight_checks` (default false).

Tiering properties include Azure keys (`azure_client_default_account` plus either `azure_client_default_key` or `azure_client_default_sas_token`; key wins if both set), `s3_client_default_*` and `gcs_credentials_file`.

`opensearch_heap` (default 1g): initial and maximum heap must be identical or OpenSearch fails to boot. The Debian install guide says to add it to the file manually, at half of system memory up to 31 GB.

## Checked

2026-11-04. Confirmed against the Data Node Configuration Settings Reference (password_secret, mongodb_uri, mongodb_version_probe_attempts, node_name, node_id_file, config_location, skip_preflight_checks, Azure/S3/GCS tiering keys, opensearch_heap default 1g), the Configuration Settings page (default file location) and the Debian installation guide (heap advice). Fixed: the draft said opensearch_heap is not in the reference; the reference lists a 1g default.

Method: documentation only; no commands were run.
