---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.certificate-expiry-alerting
name: certificate-expiry-alerting
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, certificate-expiry-alerts, cert-expiry, blackbox-exporter, cert-manager, x509-certificate-exporter, tls]
level: practitioner
status: gated
description: "Alert on expiring TLS certificates from blackbox_exporter probes, cert-manager metrics and file/secret exporters, with sensible thresholds and renewal-failure detection."
sources: ["https://github.com/prometheus/blackbox_exporter", "https://cert-manager.io/docs/devops-tips/prometheus-metrics/", "https://github.com/enix/x509-certificate-exporter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate expiry alerting

## Sources of expiry timestamps
| Source | Metric | Sees |
|---|---|---|
| blackbox_exporter http/tcp with TLS | `probe_ssl_earliest_cert_expiry` (unix ts of soonest-expiring cert in chain) | what clients actually get |
| cert-manager controller | `certmanager_certificate_expiration_timestamp_seconds`, `certmanager_certificate_ready_status` | Certificate resources |
| x509-certificate-exporter | `x509_cert_not_after` | Secrets and files on nodes (kubelet, etcd certs) |
| kube-apiserver | `apiserver_client_certificate_expiration_seconds_bucket` | client certs used against the API |

## Rules
```yaml
- alert: TLSCertExpiresSoon
  expr: (probe_ssl_earliest_cert_expiry - time()) / 86400 < 21
  for: 1h
  labels: {severity: ticket}
  annotations:
    summary: "{{ $labels.instance }} cert expires in {{ $value | humanize }} days"
- alert: TLSCertExpiresVerySoon
  expr: (probe_ssl_earliest_cert_expiry - time()) / 86400 < 7
  for: 10m
  labels: {severity: page}
- alert: CertManagerRenewalStuck
  expr: certmanager_certificate_ready_status{condition="False"} == 1
  for: 1h
```
- Let's Encrypt renews at 30 days left (cert-manager default `renewBefore` = 1/3 of duration), so "< 21 days" (gated: unconfirmed, source is paywalled or blocked)
  means automatic renewal has already failed for 9 days: that is the useful signal.
- Page only at < 7 days; earlier is a ticket.

## Gotchas
- `probe_ssl_earliest_cert_expiry` covers the whole served chain: an expiring intermediate triggers it too.
- Behind a CDN/LB, the probe sees the edge cert, not the origin's; probe the origin separately.
- Probes need SNI: blackbox uses the target hostname; for IP targets set `tls_config.server_name` in the module.
- `time()` in rules is evaluation time; no clock issues unless the Prometheus host clock is wrong.

## Verify
- [ ] Test with a short-lived cert (e.g. 8 days) and see the ticket alert fire.
- [ ] Every public hostname has a probe target (compare with DNS/Ingress inventory).

## Checked

2026-11-02

- Confirmed: blackbox_exporter README, cert-manager Prometheus metrics page and the enix x509-certificate-exporter README were fetched.
- Removed or gated: Metric names such as probe_ssl_earliest_cert_expiry, certmanager_certificate_expiration_timestamp_seconds and x509_cert_not_after and the 21/9-day thresholds were not all located on the fetched pages; gated, confirm in each exporter's metrics reference. Thresholds are choices, not documented values.

Method: documentation only; no commands were run.
