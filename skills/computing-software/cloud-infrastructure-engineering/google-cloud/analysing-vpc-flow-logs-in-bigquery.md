---
id: computing-software.cloud-infrastructure-engineering.google-cloud.analysing-vpc-flow-logs-in-bigquery
name: analysing-vpc-flow-logs-in-bigquery
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-observability, flow-logs-analysis, flow-logs-bigquery, log-analytics, egress-cost]
level: advanced
status: gated
description: "Route VPC Flow Logs to BigQuery or Log Analytics and answer real questions with SQL: top talkers, egress by destination, unexpected ports, inter-zone traffic cost drivers."
sources: ["https://cloud.google.com/vpc/docs/flow-logs", "https://cloud.google.com/vpc/docs/using-flow-logs", "https://cloud.google.com/logging/docs/export/bigquery", "https://cloud.google.com/network-intelligence-center/docs/flow-analyzer/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analysing VPC Flow Logs in BigQuery

## 1. Get the logs somewhere queryable
Enable on subnets (choose sampling and aggregation interval to balance detail against volume):
```bash
gcloud compute networks subnets update app --region=<R> --enable-flow-logs \
  --logging-flow-sampling=0.5 --logging-aggregation-interval=interval-5-min --logging-metadata=include-all
```
Then either upgrade the log bucket to **Log Analytics** (query in place, linked BigQuery dataset), or a sink:
```bash
gcloud logging sinks create flowlogs-bq bigquery.googleapis.com/projects/<P>/datasets/flowlogs \
  --log-filter='log_id("compute.googleapis.com/vpc_flows")' --use-partitioned-tables
```
Grant the sink writer identity `bigquery.dataEditor` on the dataset. Flow Analyzer (Network Intelligence Center) gives a UI on the same data.

## 2. Queries
Top talkers out of the VPC (last day):
```sql
SELECT jsonPayload.connection.src_ip AS src, jsonPayload.dest_location.country AS dst_country,
       SUM(CAST(jsonPayload.bytes_sent AS INT64)) / POW(1024,3) AS gib
FROM `<P>.flowlogs.compute_googleapis_com_vpc_flows`
WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND jsonPayload.reporter = 'SRC' AND jsonPayload.dest_vpc.vpc_name IS NULL
GROUP BY src, dst_country ORDER BY gib DESC LIMIT 20;
```
Cross-zone traffic (billable):
```sql
SELECT jsonPayload.src_instance.zone AS src_zone, jsonPayload.dest_instance.zone AS dst_zone,
       SUM(CAST(jsonPayload.bytes_sent AS INT64))/POW(1024,3) AS gib
FROM `<P>.flowlogs.compute_googleapis_com_vpc_flows`
WHERE jsonPayload.src_instance.zone != jsonPayload.dest_instance.zone
GROUP BY 1,2 ORDER BY gib DESC;
```
Unexpected ports: group by `jsonPayload.connection.dest_port` (gated: unconfirmed, source is paywalled or blocked) for a sensitive subnet.

## Gotchas
- Byte counts are sampled: multiply mentally by 1/sampling for absolute volumes (or compare relatively).
- Each flow may be reported by both ends (`reporter` SRC and DEST); filter one to avoid double counting.
- Flow logs at 1.0 sampling with include-all metadata on busy subnets is costly in logging ingestion.

## Verify
- [ ] Queries return data for the last hour; top-talker results match billing SKU trends for egress.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the sampling range and aggregation interval limits. Gated: the exported field path jsonPayload.connection.dest_port was not found in the fetched pages.

Method: documentation only; no commands were run.
