---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-cluster-gossip-tls
name: alertmanager-cluster-gossip-tls
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [cluster-tls-config, gossip-encryption, alertmanager-cluster, alertmanager-ha, mtls]
level: advanced
status: docs-checked
description: "Encrypt and authenticate Alertmanager cluster gossip with --cluster.tls-config (mutual TLS between peers), plus web TLS for the API."
sources: ["https://github.com/prometheus/alertmanager/blob/main/docs/https.md", "https://prometheus.io/docs/alerting/latest/https/", "https://github.com/prometheus/alertmanager#high-availability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager cluster gossip TLS

Peer gossip listens on port 9094 by default (`--cluster.listen-address`), and both TCP and UDP are needed from Alertmanager 0.15. Mutual TLS for gossip is configured with `--cluster.tls-config` (Alertmanager's TLS support is marked experimental).

## Gossip TLS
```bash
alertmanager --cluster.tls-config=/etc/alertmanager/cluster-tls.yml ...
```
```yaml
# cluster-tls.yml
tls_server_config:
  cert_file: /etc/alertmanager/tls/peer.crt
  key_file: /etc/alertmanager/tls/peer.key
  client_auth_type: RequireAndVerifyClientCert
  client_ca_file: /etc/alertmanager/tls/ca.crt
tls_client_config:
  cert_file: /etc/alertmanager/tls/peer.crt
  key_file: /etc/alertmanager/tls/peer.key
  ca_file: /etc/alertmanager/tls/ca.crt
```
The `client_auth_type` default is `NoClientCert`, so set it explicitly to require client certificates.

## Web/API TLS
`--web.config.file=web.yml` with `tls_server_config` and optional `basic_auth_users` (same format as Prometheus). Prometheus then needs `scheme: https` and `tls_config` in `alerting.alertmanagers`.

## Certificates
- One CA for the cluster; peer certs with SANs for each peer DNS name (`alertmanager-0.alertmanager-operated.monitoring.svc`) or IP.
- cert-manager in Kubernetes; rotate before expiry.

## Gotchas
- Mixed TLS/non-TLS peers cannot gossip; switch all peers in a quiet window.
- NetworkPolicy restricting 9094 to peer pods is a simpler first step and worth doing anyway.

## Checked
2026-10-31. Confirmed in the Alertmanager https.md and high-availability docs: `--cluster.tls-config` and its `tls_server_config` / `tls_client_config` layout, `client_auth_type` default `NoClientCert`, `client_ca_file`, experimental TLS note, `--cluster.listen-address` default 0.0.0.0:9094, TCP and UDP both needed. Removed: gossip-over-TCP-only claim, metric name and split-brain claim (not in the docs).
Method: documentation only; no commands were run.

## Verify
- [ ] Every replica still lists all peers after enabling TLS; a peer without a client cert cannot join.
