---
id: computing-software.cloud-infrastructure-engineering.graylog.upgrade-to-7-0-notes
name: upgrade-to-7-0-notes
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [release-notes-7-0, kafka-clients, mongodb-7, skip-preflight-checks, upgrade]
level: advanced
status: docs-checked
description: "Breaking changes when upgrading to Graylog 7.0: MongoDB 7.0 minimum, Kafka broker 2.1+, Data Warehouse renamed Data Lake."
sources:
  - https://go2docs.graylog.org/current/upgrading_graylog/upgrade_to_graylog_7.0.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# upgrade to 7 0 notes

Notable changes in the 7.0 upgrade notes:
- **Java**: Graylog now requires Java 21; earlier versions are unsupported. OS packages and container images ship the correct Java version.
- **MongoDB**: Graylog requires at least MongoDB 7.0. Upgrade MongoDB one minor release at a time (6.0, 7.0, 8.0), to the latest bug fix of each. If you cannot upgrade first, `skip_preflight_checks = true` lets Graylog start on older MongoDB, but this is not recommended.
- **Kafka inputs**: `kafka-clients` moved to 4.x, which drops Kafka brokers 2.0 and earlier. Kafka inputs now need brokers 2.1 or newer.
- **Enterprise theme colors**: the exact configured color is now the primary color for UI elements such as buttons and badges.
- **Rename**: Data Warehouse is now fully named Data Lake, in the UI and internally. This includes API endpoint URLs (now under `org.graylog.plugins.datalake/data_lake`), permissions (`data_lake...`) and the renamed MongoDB collections `data_lake_archive_config`, `data_lake_backends` and `data_lake_catalog`.
- **Defaults**: viewing the Cluster Configuration page moved from the `Reader` role to a new `Cluster Configuration Reader` role (existing Readers are migrated; new users need it assigned). Only admins can create API tokens, and new tokens expire after 30 days by default.
- **REST API**: unknown JSON properties are no longer silently accepted, and entity-creation APIs now take a `CreateEntityRequest` with the entity and a `share_request` kept separate. The API browser needs the `api_browser:read` permission (API Browser Reader role). `/system/urlwhitelist` endpoints were renamed to `/system/urlallowlist`.
- **Deprecations**: Elasticsearch and OpenSearch 1.x are deprecated as search backends and will be removed in Graylog 8.0; use Data Node or a supported OpenSearch.

Always read the notes for your own target version.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/upgrading_graylog/upgrade_to_graylog_7.0.htm (read in full).
