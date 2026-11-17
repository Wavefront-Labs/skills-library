---
id: computing-software.cloud-infrastructure-engineering.graylog.stream-data-routing
name: stream-data-routing
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [data-routing, stream-rules, intake, destinations, streams]
level: practitioner
status: docs-checked
description: "Use the per-stream Data Routing wizard: intake rules, attached pipelines and destinations such as search backend or Data Lake."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/data_routing.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# stream data routing

Open the **Streams** page, pick a stream, select **Data Routing**. Three steps:

1. **Intake**: stream rules that decide what moves from an input into the stream (Create Rule). Also lists pipeline rules from other streams that route messages into this one.
2. **Processing**: shows attached pipelines. Choose Edit pipelines connection, select a pipeline, then Update connections. If the stream came from an Illuminate content pack, its processing rules run before your own pipeline rules.
3. **Destinations**: where processed data goes. Send some or all of the data to one or more destinations, such as the search backend or the Data Lake.

Destination types: Data Lakes (Enterprise only; cheaper storage for data you keep but do not search in Graylog; the toggle is unavailable until a Data Lake backend is configured), OpenSearch index sets, and Outputs (forward to an external system or another Graylog instance). You can enable several destinations at once.

Filter rules per destination are exclusionary: enabling a destination sends all the stream's data there unless a filter rule excludes it. Each rule needs at least one condition (for example Field contains on `message`). To split data, exclude low-severity messages from the index set and exclude high-severity ones from the Data Lake. Finally, check the stream shows Running on the Streams page.

Streams and pipelines are covered in detail in their own articles.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/setting_up_graylog/data_routing.htm (read in full, Graylog 7.2 docs). Added destination types and the exclusionary filter-rule behaviour from the page.
