---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.mtls-client-auth-for-scraping
name: mtls-client-auth-for-scraping
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, client-auth-type, mtls-scraping, client-ca-file, tls-config, node-exporter, cert-manager]
level: advanced
status: verified
description: "Require client certificates on exporters (client_auth_type, client_ca_file, allowed SANs) and configure Prometheus scrape tls_config to present one: end-to-end mTLS scraping."
sources: ["https://github.com/prometheus/exporter-toolkit/blob/master/docs/web-configuration.md", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#tls_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mTLS scraping

## Exporter side (web.yml)
```yaml
tls_server_config:
  cert_file: /etc/node_exporter/tls/server.crt
  key_file: /etc/node_exporter/tls/server.key
  client_auth_type: RequireAndVerifyClientCert   # NoClientCert (default) | RequestClientCert | RequireAnyClientCert | VerifyClientCertIfGiven | RequireAndVerifyClientCert
  client_ca_file: /etc/node_exporter/tls/clients-ca.crt
  client_allowed_sans: [prometheus.monitoring.svc]   # optional: restrict which client cert SANs are accepted
```
The exporter-toolkit docs say `RequireAndVerifyClientCert` is the value to use for client authentication; the other values are insecure.
`node_exporter --web.config.file=/etc/node_exporter/web.yml`

## Prometheus side
```yaml
scrape_configs:
  - job_name: node
    scheme: https
    tls_config:
      ca_file: /etc/prometheus/tls/servers-ca.crt     # verifies the exporter
      cert_file: /etc/prometheus/tls/client.crt       # presented to the exporter
      key_file: /etc/prometheus/tls/client.key
      server_name: node.internal                      # when targets are IPs not matching the cert SAN
      # insecure_skip_verify: false                   # never true in prod
    static_configs: [{targets: ['10.0.0.5:9100']}]
```

## Certificates
- Issue the client cert with `extendedKeyUsage = clientAuth`, server certs with `serverAuth`; Go rejects wrong EKU
  (`x509: certificate specifies an incompatible key usage`). That text appears in the exporter's log; Prometheus
  itself only sees `remote error: tls: bad certificate`.
- With cert-manager: one `Certificate` for Prometheus (`usages: [client auth]`), one per exporter or a
  wildcard (`usages: [server auth]`), both from the same `Issuer`/CA.
- Server certs for IP targets need IP SANs, or set `server_name` and put that DNS name in the SAN.
- Files are re-read on change; rotation needs no restart on either side (tested: swapping the Prometheus client cert
  turned a `bad certificate` target `up`, and swapping the exporter's server cert changed the certificate it served).

## Troubleshooting
| `/targets` error | Meaning |
|---|---|
| `remote error: tls: certificate required` | Prometheus sent no client cert (cert_file missing) |
| `remote error: tls: unknown certificate authority` | Client cert not signed by `client_ca_file` |
| `remote error: tls: bad certificate` | Server rejected the client cert after the handshake: SAN not in `client_allowed_sans` (exporter log: `could not find allowed SANs in client cert`) or wrong key usage (`serverAuth`-only cert) |
| `tls: failed to verify certificate: x509: certificate is valid for X, not Y` | Target address not in server SAN; set `server_name` |
| `tls: failed to verify certificate: x509: cannot validate certificate for 127.0.0.1 because it doesn't contain any IP SANs` | Scraping by IP a server cert with only DNS SANs; add an IP SAN or set `server_name` |
| `tls: failed to verify certificate: x509: certificate signed by unknown authority` | Wrong `ca_file` on Prometheus |

## Verify
- [ ] `curl https://host:9100/metrics` without a client cert fails with a TLS alert.
- [ ] `curl --cert client.crt --key client.key --cacert ca.crt https://host:9100/metrics` succeeds (a Windows curl built with Schannel cannot use PEM client certificates and exits 58; use an OpenSSL-based curl, `openssl s_client` or Python's `ssl` there).
- [ ] `up{job="node"} == 1` for all targets.
