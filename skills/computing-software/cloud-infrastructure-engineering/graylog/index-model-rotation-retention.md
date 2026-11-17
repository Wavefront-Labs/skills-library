---
id: computing-software.cloud-infrastructure-engineering.graylog.index-model-rotation-retention
name: index-model-rotation-retention
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [index-set, rotation, deflector, retention-strategy, index-model]
level: practitioner
status: docs-checked
description: "How Graylog index sets work: write alias, rotation criteria, maximum indices and the retention strategies that close, delete or export old indices."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/index_model.html
  - https://go2docs.graylog.org/current/setting_up_graylog/set_data_retention_policy.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# index model rotation retention

Each index set has an index alias that always points to the one current write-active index. A background task checks the rotation criterion (number of documents, index size or index age). When met, a new index is created and prepared, then the alias switches. Nodes write to the alias without knowing the concrete index.

Reads normally use a time range. Graylog records the time range each index covers and queries only the relevant indices.

Data Tiering is the default and recommended approach; the legacy rotation and retention strategies are deprecated.

Retention: each index set has a maximum number of indices. When reached, the oldest indices are closed, deleted or exported depending on the retention strategy. The Graylog leader node performs deletion in a background thread.

Related: the Data Lake has its own retention. Set a global Maximum number of days in the Data Lake (ISO 8601 duration) in the Internal Lake Setup configuration; a per-stream value overrides it for that stream only.

## Checked

2026-11-04. Confirmed against the Index Model page. Added that Data Tiering is the default and the legacy strategies are deprecated.

Method: documentation only; no commands were run.
