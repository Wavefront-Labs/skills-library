---
id: computing-software.cloud-infrastructure-engineering.graylog.compatibility-matrix-check
name: compatibility-matrix-check
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [compatibility-matrix, supported-os, release-lifecycle, mongodb-version, opensearch-version]
level: practitioner
status: docs-checked
description: "Check Graylog, MongoDB, OpenSearch and Linux OS version compatibility, plus release support dates, before installing or upgrading."
sources:
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/compatibility_matrix.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/supported_versions.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# compatibility matrix check

Consult the compatibility matrix before any install or upgrade.

MongoDB (with Data Node), per the 7.2 docs: Graylog 7.0.x, 7.1.x and 7.2.x need MongoDB 7.x minimum and 8.2.x maximum. Graylog 6.2.x and 6.3.x allow 5.0.7 to 8.2.x.

Self-managed OpenSearch: minimum 1.1.x for all listed versions. Maximum is 2.19.6 for 6.2 to 7.1 and 3.7.x for 7.2. OpenSearch 3.x is supported for new installs and upgrades only if no indices were created under a version older than 2.0.

Official DEB and RPM repositories cover: Debian 12; Ubuntu 22.04 and 24.04; RHEL, AlmaLinux and Rocky Linux 8 and 9; SUSE Linux Enterprise Server 15. Official Docker images exist.

Release support: the Supported Versions page lists, per version, the release date, end of release support (bug fixes and security patches) and end of Enterprise support. Plan upgrades before a version nears these dates.

## Checked

2026-11-04. Confirmed against the Compatibility Matrix page (MongoDB min/max per Graylog version, OpenSearch maxima 2.19.6 and 3.7.x, OpenSearch 3.x incompatible-index note, supported OS list, official Docker images) and the Supported Versions page (lifecycle columns). Nothing removed.

Method: documentation only; no commands were run.
