---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.securing-the-federate-endpoint
name: securing-the-federate-endpoint
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [federation-security, federate-endpoint-auth, federation, prometheus-tls, basic-auth-users, web-config]
level: practitioner
status: docs-checked
description: "Protect /federate across networks with TLS and basic auth via web config or a proxy, and configure the federating server's scrape credentials."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/https/", "https://prometheus.io/docs/prometheus/latest/federation/", "https://prometheus.io/docs/operating/security/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Securing the /federate endpoint

The `/federate` endpoint returns the current value of every series selected by `match[]`. Prometheus presumes untrusted users can reach its HTTP endpoint and read all time series, and says its endpoints should not be exposed to public networks, so across networks `/federate` needs TLS and authentication.

## On the leaf (web config)
```yaml
# web.yml, passed with --web.config.file=web.yml
tls_server_config:
  cert_file: /etc/prometheus/tls/server.crt
  key_file: /etc/prometheus/tls/server.key
basic_auth_users:
  federator: $2y$10$...   # bcrypt hash of the password
```
Passwords in `basic_auth_users` are hashed with bcrypt. The file is read on every HTTP request, so changes to it and the certificates are picked up immediately. Basic auth without TLS exposes usernames and passwords in cleartext, hence both blocks above.
This protects the whole web server, not just `/federate`. To protect only `/federate`, put a reverse proxy in front and restrict the path.

## On the global server
```yaml
- job_name: federate
  scheme: https
  metrics_path: /federate
  honor_labels: true
  basic_auth: {username: federator, password_file: /etc/prometheus/secrets/federate}
  tls_config: {ca_file: /etc/prometheus/tls/ca.crt, server_name: prom-eu1.example.com}
  params: {'match[]': ['{__name__=~"job:.*"}']}
  static_configs: [{targets: [prom-eu1.example.com:9090]}]
```
mTLS alternative: `client_ca_file` + `client_auth_type: RequireAndVerifyClientCert` under `tls_server_config` on the leaf (the page notes other `client_auth_type` values are insecure) and `cert_file`/`key_file` in the global scrape's `tls_config`.

## Network
- Do not expose the leaf to public networks; restrict who can reach it to the global server.
- `--web.enable-admin-api` (paths under `/api/*/admin/`) and `--web.enable-lifecycle` (`/-/reload`, `/-/quit`) are disabled by default; leave them off on a listener other networks can reach.

## Gotchas
- More bcrypt rounds make brute force harder but cost CPU and time on every authenticated request, including the global server's scrapes; the security page leaves the round count to you.
- `server_name` in `tls_config` sets the server name the scrape uses to verify the leaf's certificate.

## Checked
Date: 2026-11-07.
Read in full: HTTPS and authentication (web config schema, `--web.config.file`, `tls_server_config`, `client_auth_type` default and the `RequireAndVerifyClientCert` note, `basic_auth_users` bcrypt, read on every request), Security model (untrusted access presumed, admin API and lifecycle flags off by default, basic auth cleartext without TLS, bcrypt rounds), and Federation (`/federate`, `match[]`, `honor_labels`). Scrape keys (`scheme`, `metrics_path`, `honor_labels`, `basic_auth.password_file`, `tls_config` `ca_file`, `cert_file`, `key_file`, `server_name`) were confirmed by searching the Configuration page for those keys and reading the `http_config` and `tls_config` sections, not by reading the whole page.
Removed because no page confirms them: the `htpasswd` command, the "cost above 12" threshold, the SAN-mismatch claim, the claim about sensitive labels, security-group/NetworkPolicy advice, and the invented Verify checklist (401 response).
Method: documentation only; no commands were run.
