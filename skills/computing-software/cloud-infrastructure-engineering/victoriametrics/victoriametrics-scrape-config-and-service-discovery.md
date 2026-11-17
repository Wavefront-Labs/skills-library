---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-scrape-config-and-service-discovery
name: victoriametrics-scrape-config-and-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [scrape-config, service-discovery, kubernetes-sd, file-sd, promscrape, stream-parse]
level: practitioner
status: docs-checked
description: "Point vmagent or VictoriaMetrics at a Prometheus-style scrape config and choose service discovery sections and reload behaviour."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmagent/", "https://docs.victoriametrics.com/victoriametrics/sd_configs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics scrape config and service discovery

Both vmagent and single-node VictoriaMetrics accept `-promscrape.config` (a file path or HTTP URL). `-promscrape.config.strictParse=false` ignores unsupported sections. Reload with `SIGHUP`, `/-/reload` (protect with `-reloadAuthKey`), or automatically with `-promscrape.configCheckInterval`.

Per-job options beyond Prometheus: `headers`, `disable_compression`, `disable_keepalive`, `series_limit`, `stream_parse`, `scrape_align_interval`, `scrape_offset`. Global streaming: `-promscrape.streamParse` and `-promscrape.minResponseSizeForStreamParse`.

Supported discovery sections include `kubernetes_sd_configs`, `consul_sd_configs`, `consulagent_sd_configs` (local agent only, better for huge clusters), `dns_sd_configs` (SRV default, or A, AAAA, MX), `docker_sd_configs`, `dockerswarm_sd_configs`, `ec2_sd_configs`, `gce_sd_configs`, `azure_sd_configs`, `digitalocean_sd_configs`, `file_sd_configs` (JSON or YAML, wildcards, HTTP URLs), `http_sd_configs`, `hetzner_sd_configs`, `nomad_sd_configs`, `openstack_sd_configs`, `static_configs` and more.

Kubernetes roles: `node`, `service`, `pod`, `endpoints`, `endpointslice`, `ingress`, with namespace and label or field selectors.

`refresh_interval` is not supported; use the matching flag instead, for example `-promscrape.consulSDCheckInterval`.

Debug pages: `/targets` shows active targets and their last error, `/service-discovery` lists discovered targets with original labels, and both link to relabeling debug views.

Check the targets page after every change to confirm the new discovery results and scrape errors.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
