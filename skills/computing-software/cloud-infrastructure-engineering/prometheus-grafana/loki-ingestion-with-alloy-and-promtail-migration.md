---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-ingestion-with-alloy-and-promtail-migration
name: loki-ingestion-with-alloy-and-promtail-migration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-alloy, loki-ingest, alloy-loki-source-kubernetes, alloy-loki-process, promtail, promtail-pipeline-stages, promtail-scrape-config, promtail-to-alloy-migration, alloy-convert, syslog-receiver, journal-scraping]
level: practitioner
status: gated
description: "Collect Kubernetes, journal and syslog logs into Loki with Alloy (loki.source.*, loki.process stages), read legacy Promtail pipelines, and migrate with alloy convert."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/loki/", "https://grafana.com/docs/alloy/latest/set-up/migrate/from-promtail/", "https://grafana.com/docs/loki/latest/send-data/promtail/stages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki ingestion with Alloy, and Promtail migration

Promtail reached end of life on 2 March 2026 (Loki docs); new setups use Alloy.

## Alloy: Kubernetes pod logs
```alloy
discovery.kubernetes "pods" {
  role = "pod"
}

discovery.relabel "pods" {
  targets = discovery.kubernetes.pods.targets

  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    target_label  = "namespace"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_label_app_kubernetes_io_name"]
    target_label  = "app"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_container_name"]
    target_label  = "container"
  }
}

// tails via the Kubernetes API; or use loki.source.file on /var/log/pods
loki.source.kubernetes "pods" {
  targets    = discovery.relabel.pods.output
  forward_to = [loki.process.default.receiver]
}

loki.process "default" {
  stage.cri {}

  stage.json {
    expressions = { level = "level", trace_id = "trace_id" }
  }

  stage.labels {
    values = { level = "" }
  }

  stage.structured_metadata {
    values = { trace_id = "" }
  }

  stage.drop {
    source = "level"
    value  = "debug"
  }

  stage.multiline {
    firstline     = "^\\d{4}-\\d{2}-\\d{2}"
    max_wait_time = "3s"
  }

  forward_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url       = "http://loki-gateway/loki/api/v1/push"
    tenant_id = "prod"
  }
}
```
## Journal and syslog
```alloy
loki.source.journal "system" {
  forward_to    = [loki.write.default.receiver]
  labels        = { job = "systemd-journal" }
  relabel_rules = loki.relabel.journal.rules
}

loki.relabel "journal" {
  forward_to = []

  rule {
    source_labels = ["__journal__systemd_unit"]
    target_label  = "unit"
  }
}

loki.source.syslog "net" {
  listener {
    address  = "0.0.0.0:1514"
    protocol = "tcp"
    labels   = { job = "syslog" }
  }
  forward_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url = "http://loki-gateway/loki/api/v1/push"
  }
}
```
Use rsyslog/syslog-ng in front to normalise legacy devices into RFC5424 over TCP (gated: unconfirmed, source is paywalled or blocked): no syslog sender was run.

## Reading Promtail configs
Promtail `scrape_configs` (with `kubernetes_sd_configs`, `relabel_configs`) map to discovery + relabel components;
`pipeline_stages` (`docker`, `cri`, `regex`, `json`, `labels`, `structured_metadata`, `timestamp`, `output`, `match`, `drop`,
`multiline`) map to `stage.*` blocks (the converter handled `cri`, `multiline`, `json`, `labels`, `structured_metadata` and `timestamp`).

## Migrate
```bash
alloy convert --source-format=promtail --output=config.alloy promtail.yaml
alloy convert --source-format=promtail --report=report.txt --bypass-errors promtail.yaml   # see unsupported bits
alloy run config.alloy        # UI on 127.0.0.1:12345 by default (--server.http.listen-addr) shows the component graph and health
```
Run both side by side on a test node; compare stream counts in Loki before switching. Positions files differ, so
expect a re-read or gap at cut-over (`loki.source.file` has `tail_from_end`).

## Verify
- [ ] Alloy UI shows all components healthy; `loki_write_sent_entries_total` increasing.
- [ ] Same streams/labels in Loki as from Promtail; no `level=debug` lines if dropped.

## Checked
Ran Alloy v1.21.1 on Windows: the two corrected blocks pass `alloy validate` (the original blocks failed with `expected TERMINATOR, got IDENT`: attributes in a block must be on separate lines). The Kubernetes block was validated only, not run (no cluster); the same `loki.process` stages ran against a local Loki 3.7.9 on a CRI-format file (labels, structured metadata, `stage.drop`, multiline). `alloy convert --source-format=promtail --output=config.alloy promtail.yaml` and `--report=report.txt --bypass-errors` ran on a Promtail file with `kubernetes_sd_configs`, relabeling and the page's pipeline stages and printed the Promtail-metrics warning in the report. The default UI address is shown in `alloy run --help`. `loki.source.journal` (Linux-only) and `loki.source.syslog` were validated, not run; `syslog_format`, `tail_from_end`, `relabel_rules` and `loki.relabel` exports were read in the Alloy v1.21.1 reference. Promtail EOL date from the Loki docs source (send-data/promtail).
