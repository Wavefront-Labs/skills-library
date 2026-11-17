---
id: computing-software.cloud-infrastructure-engineering.rook.cephcluster-crd-dashboard-and-monitoring
name: cephcluster-crd-dashboard-and-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [dashboard, urlprefix, sslcertificateref, prometheus, metricsdisabled, exporter]
level: practitioner
status: docs-checked
description: "CephCluster dashboard and monitoring fields: port, urlPrefix, ssl certificate secret, ServiceMonitor, scrape interval and the Ceph exporter."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/ceph-cluster-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dashboard settings under `spec.dashboard`:
- `enabled`: serve the Ceph dashboard.
- `urlPrefix`: serve under a subpath, useful behind a reverse proxy.
- `port`: change the default port.
- `ssl`: serve over SSL.
- `sslCertificateRef`: a Secret of type `kubernetes.io/tls` holding the certificate pair; if unset a self-signed certificate is used.

Monitoring settings under `spec.monitoring`:
- `enabled`: create the Prometheus ServiceMonitor for an internal cluster, or an endpoint port for metrics on an external cluster. Default false.
- `metricsDisabled`: when true, disables both the prometheus mgr module and the Ceph exporter. Default false.
- `port`: the port of the prometheus mgr module; it may need changing when host networking is enabled.
- `interval`: scrape interval of the module.
- `scrapeTimeoutSeconds`: must not exceed the interval; defaults to the Prometheus global value.
- `externalMgrEndpoints` and `externalMgrPrometheusPort`: for external clusters.

Exporter settings under `spec.monitoring.exporter`:
- `perfCountersPrioLimit`: maps to the `--prio-limit` flag; 0 exports all counters, default 5.
- `statsPeriodSeconds`: maps to `--stats-period`, default 5.

See the dashboard and Prometheus monitoring guides for the full setup.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-cluster-crd) against this skill: 18 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 3 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
