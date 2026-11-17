---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-tls-auth-and-web-config
name: prometheus-tls-auth-and-web-config
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, prometheus-security, prometheus-tls, web-config, web-config-file, basic-auth, bcrypt, mtls, client-cert, tls-config, authorization-header, bearer-token, oauth2-scrape, admin-api, lifecycle-api, network-policy, exporter-toolkit, secrets-files, pca]
level: practitioner
status: gated
description: "Lock down Prometheus and exporters: web.yml TLS and basic auth, mTLS between scraper and targets, scrape-side tls_config/authorization, and which flags must stay off in production."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/https/", "https://prometheus.io/docs/operating/security/", "https://github.com/prometheus/exporter-toolkit/blob/master/docs/web-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS, authentication and web configuration

**Goal:** no plaintext metrics on shared networks, no unauthenticated admin endpoints,
and credentials that never appear in `prometheus.yml` or `ps` output.

## 1. Threat model Prometheus assumes
Prometheus trusts anyone who can reach its HTTP port: they can run arbitrary PromQL (DoS),
read all metrics (which include hostnames, versions, sometimes label values that are
secrets), and with the lifecycle/admin API reload config, delete data or shut it down.
Exporters are the same: `/metrics` on 0.0.0.0 leaks system detail. So: encrypt, authenticate,
and keep the admin flags off unless a trusted automation needs them.

## 2. Server-side: `web.yml` (exporter-toolkit)
Prometheus, Alertmanager, node_exporter, blackbox_exporter and most official exporters
accept `--web.config.file=web.yml`:
```yaml
tls_server_config:
  cert_file: /etc/prometheus/tls/server.crt
  key_file:  /etc/prometheus/tls/server.key
  client_auth_type: RequireAndVerifyClientCert   # mTLS; NoClientCert for TLS only
  client_ca_file: /etc/prometheus/tls/ca.crt
  min_version: TLS12
basic_auth_users:
  scraper: $2y$10$...bcrypt...     # htpasswd -nBC 10 scraper   (or: python -c "import bcrypt;print(bcrypt.hashpw(b'pw',bcrypt.gensalt()).decode())")
http_server_config:
  http2: true
```
- The file is re-read live (run: a `min_version` change applied to the next connection with no reload). A bad file is rejected at start: `Unable to validate web configuration file ... failed to read cert_file` and the process exits (run). `promtool check web-config` also reports it (run).
- If `http2` is true (the default), a `cipher_suites` list needs an AES-128-GCM suite or the server will not start; see the web-tls skill.
- bcrypt cost 10 is the docs' example (measured `checkpw`: 0.047 s at 10, 0.19 s at 12, 0.77 s at 14); the exporter-toolkit docs say the hash is computed on the first authenticated request and then cached.
- Test: `curl --cacert ca.crt -u scraper:pw https://host:9090/-/ready` (run with `--ssl-no-revoke` on the Windows Schannel curl build: 200 with credentials, 401 without; with `RequireAndVerifyClientCert` a client without a certificate was reset and one with a certificate got 200).

## 3. Scrape-side: talking to protected targets
```yaml
scrape_configs:
  - job_name: node
    scheme: https
    tls_config:
      ca_file: /etc/prometheus/tls/ca.crt
      cert_file: /etc/prometheus/tls/scraper.crt    # mTLS client identity
      key_file:  /etc/prometheus/tls/scraper.key
      server_name: node-exporter.internal            # SNI/verification override when scraping by IP
    basic_auth: { username: scraper, password_file: /etc/prometheus/secrets/node-pw }
  - job_name: app
    authorization: { type: Bearer, credentials_file: /var/run/secrets/token }
  - job_name: cloud
    oauth2: { client_id: ..., client_secret_file: ..., token_url: https://idp/token, scopes: [metrics.read] }
```
All three jobs above passed `promtool check config` with real files in place (run). `insecure_skip_verify: true` is for lab clusters only; it defeats the point and hides
expiring certs. Kubernetes SD jobs usually point at the service account token and cluster CA (gated: unconfirmed, source is paywalled or blocked; no cluster here). `bearer_token_file` is no longer in the 3.15 configuration reference but `promtool check config` still accepted it; prefer `authorization: {credentials_file: ...}`.

## 4. Flags and endpoints to control
| Flag / path | Default | Production |
|---|---|---|
| `--web.enable-lifecycle` (`/-/reload`, `/-/quit`) | off | on only if reloads come from a sidecar on localhost; else SIGHUP |
| `--web.enable-admin-api` (`snapshot`, `delete_series`) | off | on briefly for backups, behind auth |
| `--web.enable-remote-write-receiver` | off | on only on receivers, behind auth |
| `--web.listen-address` | `0.0.0.0:9090` (confirmed in `--help`) | bind to pod IP/localhost where a proxy terminates |
| `--web.external-url` / `--web.route-prefix` | — | set when behind a reverse proxy so links work |
| `/debug/pprof` | always on (200 without auth; 401 once basic auth is set, run) | restrict via proxy/NetworkPolicy |

## 5. Layered alternatives
- A reverse proxy (nginx, oauth2-proxy, Envoy) in front for SSO/OIDC; Prometheus has no
  user model of its own.
- Kubernetes: `NetworkPolicy` allowing ingress to 9090 only from Grafana/Alertmanager
  namespaces; exporters only from the Prometheus pods (gated: unconfirmed, source is paywalled or blocked; no cluster here).
- Secrets as files from a mounted Secret/Vault agent, never as env-interpolated YAML.
  Prometheus does not expand env vars in general: `job_name: ${FOO}` with `FOO=expanded` showed `${FOO}` in `/api/v1/status/config` (run); the one exception in 3.x is `global.external_labels` values, which are expanded (run: `envvar: expanded`; the old `expand-external-labels` flag is now default), so pre-processing tools like `envsubst` would leave the secret in the rendered file.

## Gotchas
- Certificate rotation: exporter-toolkit re-reads cert files per connection, so rotating
  in place works; scrape-side `tls_config` files are also re-read, but a wrong `server_name`
  after rotation shows up as `x509: certificate is valid for ..., not ...`.
- `basic_auth` in `web.yml` protects `/metrics` too, so Grafana's Prometheus data source
  needs the same credentials.
- Alertmanager clustering (gossip, default `--cluster.listen-address=0.0.0.0:9094`) is not covered by `--web.config.file`; Alertmanager 0.34.1 has a separate `--cluster.tls-config` flag (marked EXPERIMENTAL in `--help`) for mutual TLS on the gossip channel, and network policy is the other layer.
- Federation and remote_read endpoints inherit server auth; configure the puller accordingly.

## Verify
- [ ] `curl http://host:9090/metrics` (plain, unauthenticated) fails from a non-Prometheus host.
- [ ] `openssl s_client -connect host:9090 </dev/null 2>/dev/null | openssl x509 -noout -dates` shows a valid, non-expiring-soon cert, and an alert exists on cert expiry (blackbox `probe_ssl_earliest_cert_expiry`).
- [ ] `grep -nE 'password:|credentials:|client_secret:' prometheus.yml` returns nothing (only `*_file` keys).

## Checked
Prometheus 3.15.1, promtool and Alertmanager 0.34.1 (windows-amd64), OpenSSL 3.2.3, Python ssl and bcrypt, run locally: web.yml with TLS, basic auth and mTLS (`RequireAndVerifyClientCert`: no client cert reset, with cert 200), live re-read, startup failure and `promtool check web-config` on a missing cert, TLS10-TLS13 names accepted, `promtool check config` on the node/app/cloud scrape jobs (tls_config, basic_auth password_file, authorization credentials_file, oauth2) and on `bearer_token_file`, env var non-expansion in `/api/v1/status/config`, `/debug/pprof` with and without auth, Alertmanager `--help` for the gossip flags. Docs read: exporter-toolkit docs/web-configuration.md. Not run: Kubernetes NetworkPolicy and service-account jobs, OAuth2 token fetch, cert-expiry alerting.
