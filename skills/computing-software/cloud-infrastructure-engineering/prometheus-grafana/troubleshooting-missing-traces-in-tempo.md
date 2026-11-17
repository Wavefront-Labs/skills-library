---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.troubleshooting-missing-traces-in-tempo
name: troubleshooting-missing-traces-in-tempo
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [tempo-missing-traces, tempo-troubleshooting, tempo, tempo-cli, discarded-spans]
level: advanced
status: docs-checked
description: "Find why traces are missing or incomplete in Tempo: sampling, exporter failures, discarded spans (rate, trace too large), tenant headers, search vs trace-by-ID and retention."
sources: ["https://grafana.com/docs/tempo/latest/troubleshooting/", "https://grafana.com/docs/tempo/latest/troubleshooting/querying/unable-to-see-trace/", "https://grafana.com/docs/tempo/latest/operations/tempo_cli/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting missing traces in Tempo

Work from the producer to the query.

## 1. Was it produced and exported?
- SDK sampling: most SDKs use a probabilistic sampler by default, so as few as one in a thousand records may be picked up; check the tracer's sampling rate.
- Pipeline drops: on Grafana Alloy, `exporter_send_failed_spans_ratio_total` and `receiver_refused_spans_ratio_total` should both be 0. Also check protocol, port and endpoint settings.

## 2. Did Tempo accept it?
```promql
sum(rate(tempo_distributor_spans_received_total[5m])) by (tenant)
sum(rate(tempo_receiver_refused_spans[5m]))     # should be 0
```
If `tempo_receiver_refused_spans` is above 0, spans are being dropped, likely by rate limiting; raise `max_traces_per_user` in the override limits if you need more ingest volume (see the ingestion limits page).

## 3. Querying correctly?
- Multi-tenant: query with the same `X-Scope-OrgID` the data was written with (Grafana data source header).
- Trace by ID 404 shortly after ingest: search across ingesters and backend should find it; if not, check `query_frontend`/querier errors.
- Search (TraceQL) shows nothing for recent data: time range too narrow, or the attribute is on the resource rather than the span (for example `resource.service.name`).
- Old traces missing: block retention (`compactor.compaction.block_retention`) expired.

## 4. Incomplete traces (missing spans)
- Broken context propagation between services (orphan root spans in one service).
- Spans from one service sampled differently (non-parent-based samplers).
- Clock skew makes spans appear outside the trace window.

## Tools
```bash
tempo-cli query api trace-id <API_ENDPOINT> <trace-id> --org-id <TENANT_ID>
tempo-cli query trace-id <trace-id> <tenant-id> --backend=<BACKEND> --bucket=<BUCKET>   # read straight from the backend; see the tempo-cli page for all flags
```

## Verify
- [ ] A test trace sent from a known-good generator is retrievable by ID within seconds.

## Checked
- 2026-10-28. Confirmed against the Tempo troubleshooting page (unable to see trace: probabilistic SDK sampling, Alloy `exporter_send_failed_spans_ratio_total` and `receiver_refused_spans_ratio_total`, `tempo_receiver_refused_spans`, `tempo_distributor_spans_received_total`, `max_traces_per_user`), the tempo-cli page (`query api trace-id`, `--org-id`, `query trace-id <trace-id> <tenant-id>`, `--backend`) and the configuration page (`block_retention`).
- Fixed: `tempo-cli query blocks` does not exist (the command is `query trace-id`).
- Removed: `tempo_discarded_spans_total` and its reason names, `otelcol_*` metric names, `span.service.name`, the `OTEL_TRACES_SAMPLER` reference and telemetrygen.
Method: documentation only; no commands were run.
