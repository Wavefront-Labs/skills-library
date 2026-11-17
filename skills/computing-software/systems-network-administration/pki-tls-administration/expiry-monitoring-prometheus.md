---
id: computing-software.systems-network-administration.pki-tls-administration.expiry-monitoring-prometheus
name: expiry-monitoring-prometheus
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [expiry-monitoring-prometheus, pki-lifecycle, monitoring, blackbox-exporter, x509-exporter, expiry-alerts, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Alert on certificate expiry with the Prometheus blackbox exporter (served certs) and x509-certificate-exporter (files, Kubernetes secrets)."
sources:
  - https://github.com/prometheus/blackbox_exporter
  - https://github.com/enix/x509-certificate-exporter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expiry monitoring and alerting
Goal: failed renewals are noticed days before an outage.

## Two complementary sources
- Blackbox exporter probes what a server actually presents. It uses the multi-target pattern: Prometheus passes the target to the exporter via relabelling, and a `module` parameter picks the probe (HTTP, HTTPS via the `http` prober, DNS, TCP, ICMP, gRPC). The TCP prober has a `tls` option (and `starttls` query steps) for TLS-wrapped services, and an option to check each certificate in the chain against its CRL (`probe_ssl_crl_*` metrics). Its README example:
```yaml
scrape_configs:
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets: [https://prometheus.io]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9115   # the exporter's real host:port
```
  HTTP probes accept a `hostname` parameter that sets the Host header and TLS SNI. Secure the exporter's endpoints with TLS and basic auth and do not expose it to the internet.
- x509-certificate-exporter (Enix) reads certificates where they are stored: TLS Secrets and ConfigMaps in Kubernetes, PKCS#12 and JKS keystores, CRLs, admission caBundles, kubeconfigs and files on disk (with glob patterns). Every certificate in a PEM chain becomes its own series, so intermediates and roots appear next to leaves.

## Alert on the x509 exporter's series
`x509_cert_not_after` is the Unix timestamp of NotAfter and is always emitted; the project's own examples are:
```promql
# days remaining for every cert in scope
(x509_cert_not_after - time()) / 86400
# anything expiring in the next 14 days
(x509_cert_not_after - time()) / 86400 < 14
# exclude trust roots in kube-public
(x509_cert_not_after - time()) / 86400 < 14 unless x509_cert_not_after{secret_namespace="kube-public"}
```
- `x509_cert_expired` (on by default) is 1 once expired. `x509_cert_expires_in_seconds` needs `metrics.exposeRelative: true`.
- Alert on the exporter's own health: `x509_source_up == 0` (pair with a short `for:` because the series is absent during start-up), `x509_source_errors_total` increasing, and `x509_source_bundles` for sizing.
- Stale CRLs: `x509_crl_next_update` and `x509_crl_stale` are emitted when a CRL is parsed.
- Use two thresholds (warning and critical) and scale them to certificate lifetime; with short-lived certificates a 14 day warning is too late (practitioner guidance).

## Gotchas
- Monitoring only leaf certificates misses expiring intermediates and the OCSP signing certificate; the x509 exporter's per-chain series help with the first.
- A probe that checks only the served leaf says nothing about unused copies in Secrets or files; run both sources.

## Verify
- [ ] A test certificate with 10 days left fires the warning alert.
- [ ] Alerts route to a person on call.

## Checked
Method: docs-checked 2026-11-09 against the blackbox_exporter README and CONFIGURATION.md and the x509-certificate-exporter README and docs/metrics.md (raw GitHub).
Removed as unconfirmed: the `tcp_tls` module name, `probe_ssl_earliest_cert_expiry` and `probe_ssl_last_chain_expiry_timestamp_seconds` metric names and the blackbox alert rule built on them, the 1/3-lifetime threshold rule for 47-day certificates, and the `openssl x509 -checkend` shell fallback.
