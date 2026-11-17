---
id: computing-software.cloud-infrastructure-engineering.graylog.data-lake-retention-and-retrieval
name: data-lake-retention-and-retrieval
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [lake-retention, lake-retrieve, restored-index, iso-8601]
level: practitioner
status: docs-checked
description: "Set global and per-stream Data Lake retention and retrieve logs back into the search backend; retrieval counts against license."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/set_data_retention_policy.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/retrieve_logs_from_data_lake.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# data lake retention and retrieval

**Retention.** Global: in Data Lake > Internal Lake Setup > Configuration, set Maximum number of days in the Data Lake (ISO 8601 duration). Per stream: Overview tab, the stream's Data Routing, then Data Retention; a stream policy overrides the global one for that stream only.

**Retrieval.** Needs administrator or the Data Lake User role. In Overview, find the stream, click Retrieve logs, set the time range and optional filters. External lakes retrieve by table.

- Restored data is indexed in the search backend, in an index with the prefix `restored-archive-data-lake`, within the Restored Archive index set (same as archive restores).
- Retrieval does not remove data from the lake.
- Retrieved data counts against license usage at retrieval.

## Checked

2026-11-04. Confirmed against the Data Lake pages. Nothing removed.

Method: documentation only; no commands were run.
