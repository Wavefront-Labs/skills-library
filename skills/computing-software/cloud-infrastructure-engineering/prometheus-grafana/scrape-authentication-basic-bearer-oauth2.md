---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.scrape-authentication-basic-bearer-oauth2
name: scrape-authentication-basic-bearer-oauth2
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, scrape-config, scrape-auth, scrape-oauth2, scrape-bearer-token, basic-auth, authorization, credentials-file, oauth2-client-credentials, tls-config, kubernetes-service-account-token, secrets-in-config, http-config, pca]
level: practitioner
status: verified
description: "Authenticate scrapes: basic_auth, bearer authorization with credentials_file, oauth2 client-credentials, TLS client certs, k8s SA token; keep secrets out of prometheus.yml."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#oauth2", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#tls_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scrape authentication

**Goal:** scrape targets that require credentials without putting the secret in the
config file that is committed, templated and shown on `/config`.

## 1. The four mechanisms (mutually exclusive per job)
```yaml
scrape_configs:
  - job_name: basic
    basic_auth:
      username: prom
      password_file: /etc/prometheus/secrets/basic.pw     # not `password:` in git

  - job_name: bearer
    authorization:
      type: Bearer                                        # default; "Basic" not allowed here
      credentials_file: /etc/prometheus/secrets/token

  - job_name: oauth2
    oauth2:
      client_id: prometheus
      client_secret_file: /etc/prometheus/secrets/oauth.secret
      token_url: https://idp.example.com/oauth2/token
      scopes: [metrics.read]
      endpoint_params: {audience: metrics-api}          # extra form fields some IdPs need

  - job_name: mtls
    scheme: https
    tls_config:
      ca_file: /etc/prometheus/secrets/ca.crt
      cert_file: /etc/prometheus/secrets/client.crt
      key_file: /etc/prometheus/secrets/client.key
      server_name: metrics.internal       # SNI / verification name when the target IP differs
      # insecure_skip_verify: true        # last resort, never in prod
```
`basic_auth`, `authorization` and `oauth2` cannot be combined in one job; `tls_config` can
go with any. The same `http_config` block exists for `remote_write`, `alertmanager_configs`
and every `*_sd_config`, with the same keys.

## 2. Kubernetes: the service-account token
```yaml
  - job_name: kubelet
    scheme: https
    authorization:
      credentials_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      insecure_skip_verify: true      # kubelet serving certs are often self-signed per node
    kubernetes_sd_configs: [{role: node}]
```
The projected token file rotates; Prometheus re-reads `*_file` secrets on every scrape, so
rotation is picked up without a reload. Inline `credentials:` would not.

## 3. Secrets hygiene
- `*_file` variants exist for every secret: `password_file`, `credentials_file`,
  `client_secret_file`. Use them; the UI `/config` page and `/api/v1/status/config` redact
  inline secrets as `<secret>` but file paths are harmless either way.
- Mount secrets read-only (`0400`, owner `prometheus`); a world-readable token on a shared
  node is the usual leak.
- With the Prometheus Operator, the ServiceMonitor endpoint fields `basicAuth`, `authorization` and `oauth2` take
  Secret key references; see the operator API reference for the exact fields.

## 4. Diagnosing auth failures
`/targets` shows `server returned HTTP status 401 Unauthorized` (bad credential) or `403`
(valid credential, no permission) — different fixes. Reproduce from the Prometheus host:
```bash
curl -sv -H "Authorization: Bearer $(cat /etc/prometheus/secrets/token)" https://target:8443/metrics -o /dev/null
```
For oauth2, Prometheus sent one client-credentials token request (client authenticated with HTTP Basic, form fields
`grant_type`, `scope` and the `endpoint_params` such as `audience`) and reused the token across scrapes (one request
in 20 s with `expires_in` 3600). There are no per-scrape auth metrics, so rely on the target error string and the
IdP's logs.

## Gotchas
- `authorization.type` `Bearer` also loads in lower case, but `Basic` is rejected at load (`use "basic_auth" instead`).
- Whitespace around the secret in a `credentials_file` is stripped: files with an LF ending, a CRLF ending or no
  newline all authenticated (tested on 3.15.1). A 401 with a correct-looking file is more likely a stray character
  inside the secret; inspect it with `cat -A`.
- `tls_config.server_name` is also what `insecure_skip_verify: false` validates against;
  scraping by IP without it fails with "certificate is valid for … not 10.0.0.5".
- `oauth2.token_url` must be reachable at **scrape time**: with an unreachable `token_url` the target went down
  with a `Post "<token_url>": dial tcp ...` error, not an auth error.

## Verify
- [ ] No `password:`, `credentials:` or `client_secret:` literal in the committed config.
- [ ] Rotating the token file alone restores a 401'ing target without a reload.
- [ ] `/api/v1/status/config` shows `<secret>` for any remaining inline value.
