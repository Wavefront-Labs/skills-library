---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.scraping-through-proxies
name: scraping-through-proxies
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, scrape-config, scrape-proxy, proxy-url, no-proxy, proxy-from-environment, proxy-connect-header, http-proxy, https-proxy, egress-proxy, connect-tunnel, air-gapped, remote-write-proxy, pca]
level: practitioner
status: docs-checked
description: "Scrape through an HTTP(S) proxy: proxy_url, no_proxy, proxy_from_environment and proxy_connect_header, and how to keep local scrapes direct."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scraping through proxies

**Goal:** reach targets or remote-write endpoints that are only accessible via an egress
proxy, without proxying the local targets that must stay direct.

## 1. Per-job proxy settings
```yaml
scrape_configs:
  - job_name: saas-exporter
    scheme: https
    proxy_url: http://egress-proxy.internal:3128
    no_proxy: "localhost,127.0.0.1,.cluster.local,10.0.0.0/8"
    proxy_connect_header:                      # sent on the CONNECT to the proxy itself
      Proxy-Authorization: ["Basic cHJvbTpzZWNyZXQ="]
    static_configs:
      - targets: ["metrics.vendor.example.com:443"]
```
- `proxy_url` applies to that job only (and to its SD HTTP calls if the SD block has its own
  `proxy_url`; SD and scrape are configured separately).
- `no_proxy` is a comma-separated string of IPs, CIDR ranges and domain names to exclude from proxying; IPs and domain
  names can contain port numbers.
- `proxy_connect_header` maps a header name to a list of secret values, sent to the proxy during CONNECT requests.
- `proxy_from_environment` (default `false`) makes the job use the proxy indicated by `HTTP_PROXY`, `HTTPS_PROXY` and
  `NO_PROXY` (and their lowercase versions). Prefer an explicit `proxy_url` so the behaviour is visible in the config.

These keys belong to `http_config`, which the scrape config embeds and so do most `*_sd_config` blocks (including
`oauth2`, which has its own proxy keys for token requests). Check the `remote_write` and `alertmanager_config` reference
sections for the options available there.

## 2. HTTPS through a proxy
For HTTPS targets the proxy receives a CONNECT request (`proxy_connect_header` is sent on it). If a TLS-intercepting
proxy re-signs traffic, certificate verification fails until its CA is configured in the job's `tls_config`
(`ca_file`).

## 3. Telling proxy errors apart
Read the error on the target's row in the Prometheus targets page and test from the Prometheus host with a client that
uses the same proxy. Typical split: the proxy host unreachable (connection error to the proxy), proxy authentication
rejected (check `proxy_connect_header`), a certificate error after CONNECT (interception or wrong CA), or a timeout
(raise `scrape_timeout` for that job only).

## 4. Keep local scrapes direct
With `proxy_from_environment: false` (the default) the proxy environment variables are ignored for that job. Where it is
set to `true`, every such job follows `HTTP_PROXY`/`HTTPS_PROXY` unless `NO_PROXY` excludes the target, so list local
targets (pod and service CIDRs, cluster domain names, the API server address) in `no_proxy`, or prefer per-job `proxy_url`.

## Gotchas
- Do not put credentials in `proxy_url` in a file that is committed; `proxy_connect_header` values are typed as secrets.
- `no_proxy` only matters when a proxy is configured for that job.

## Verify
- [ ] Proxy access log shows CONNECTs only for the intended hosts.
- [ ] Local targets (`kubelet`, `node`) remain `up` with proxy settings applied.
- [ ] Stopping the proxy flips only the proxied job to errors.

## Checked
Date: 2026-10-28. Confirmed against the Prometheus configuration reference (`http_config` and `oauth2` sections: `proxy_url`, `no_proxy` format, `proxy_from_environment` default false and the environment variables it reads, `proxy_connect_header` as a list of secrets sent during CONNECT; `http_config` embedded by the SD blocks; `tls_config`). Removed unconfirmed claims: exact Go `NO_PROXY` semantics, `proxy_from_environment` exclusivity with `proxy_url`, `remote_write`/`alertmanager` proxy keys, error message strings, the curl test, SOCKS5 and https-proxy behaviour, and the Prometheus Operator version gate. Corrected the environment-proxy advice: with the default `proxy_from_environment: false` the variables are ignored.
Method: documentation only; no commands were run.
