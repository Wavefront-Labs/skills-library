---
id: computing-software.cybersecurity-defensive.splunk.splunk-edge-processor-spl2-pipelines
name: splunk-edge-processor-spl2-pipelines
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, edge-processor, ingest-processor, spl2, data-pipelines, log-reduction, data-masking, data-onboarding]
level: advanced
status: draft
description: "Filter, mask and route data before indexing with Splunk Edge Processor and Ingest Processor SPL2 pipelines, including pipeline structure, testing and deployment."
sources: ["https://docs.splunk.com/Documentation/SplunkCloud/latest/EdgeProcessor/AboutEdgeProcessorSolution", "https://docs.splunk.com/Documentation/SplunkCloud/latest/IngestProcessor/AboutIngestProcessorSolution", "https://docs.splunk.com/Documentation/SCS/current/SearchReference/Introduction"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Edge Processor and Ingest Processor pipelines

Edge Processor (EP) is a customer-hosted data processing node managed from Splunk Cloud; Ingest
Processor (IP) is the Splunk-hosted equivalent inside Splunk Cloud. Both run SPL2 pipelines that
transform data in motion: drop, mask, extract, convert logs to metrics, route to Splunk indexes or S3.

## Topology
- EP instances run on Linux hosts near sources; forwarders send S2S to EP (`outputs.conf` pointing at
  EP on port 9997), syslog/HEC sources send directly. EP forwards to Splunk Cloud indexers or S3.
- Group EP nodes into an Edge Processor (cluster) behind a load balancer; config is pushed from the
  cloud tenant, so nodes need outbound HTTPS to the tenant.

## Pipeline anatomy (SPL2)
```
$pipeline = | from $source
  | rex field=_raw /action=(?P<action>\w+)/
  | where NOT (sourcetype == "pan:traffic" AND action == "allow" AND dest_port == 53)
  | eval _raw = replace(_raw, /(\d{4}-){3}\d{4}/, "XXXX-XXXX-XXXX-XXXX")
  | into $destination;
```
- `$source` is defined by a partition (sourcetype/host/source filter); events not matched by any
  pipeline go to the default destination, so nothing is lost by accident.
- Branch with `| branch [...] [...]` (IP) or create two pipelines on the same partition for
  "full copy to S3, reduced copy to index".

## Workflow
1. Pipelines > New pipeline, pick partition, pick sample data (snapshot from live traffic).
2. Write SPL2; the preview shows before/after per event and estimated volume change.
3. Save and apply to one Edge Processor; watch node metrics (events in/out, dropped, queue).
4. Promote to other EP groups.

## Gotchas
- SPL2 is not SPL: regexes are `/.../` literals, comparison is `==`, `where` replaces `search`.
- Index-time props on indexers still run after EP; double timestamp/linebreak logic causes drift.
- EP nodes buffer to disk when the destination is down; size disk for the outage you must survive.
- Masking in EP is the only place PII never touches Splunk storage; masking at search time is not.

## Verify
Compare `| tstats count where index=<idx> by sourcetype` before and after; check the EP
dashboard shows zero dropped-on-error events; search for the masked pattern returns nothing.
