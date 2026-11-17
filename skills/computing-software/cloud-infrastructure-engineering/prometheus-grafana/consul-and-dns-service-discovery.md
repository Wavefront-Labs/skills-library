---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.consul-and-dns-service-discovery
name: consul-and-dns-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, service-discovery, consul-sd-configs, dns-sd-configs, consul-sd, dns-sd, srv-records, a-records, consul-tags, consul-services-filter, consul-health, nomad-sd, headless-service-dns, refresh-interval, pca]
level: practitioner
status: docs-checked
description: "Discover targets from Consul (services, tags, health, ACL token, filters) and from DNS SRV/A/AAAA records (headless services, static infra), with the relabeling each needs."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#consul_sd_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#dns_sd_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consul and DNS service discovery

**Goal:** use a registry you already run (Consul, or just DNS) to feed targets to Prometheus.

## 1. Consul
```yaml
  - job_name: consul-services
    consul_sd_configs:
      - server: consul.example.internal:8500
        scheme: https
        token: <acl-token>
        datacenter: dc1
        services: [api, worker]
        health_filter: '<Health API filter expression>'
        refresh_interval: 30s
    relabel_configs:
      - source_labels: [__meta_consul_service]
        target_label: job
      - source_labels: [__meta_consul_address, __meta_consul_service_metadata_metrics_port]
        regex: (.+);(.+)
        replacement: $1:$2
        target_label: __address__
```
Config reference (consul_sd_config):
- `server` defaults to `localhost:8500`; `scheme` defaults to `http`; `path_prefix` is for Consul behind a reverse proxy; `token`, `datacenter`, `namespace` and `partition` (the last two Consul Enterprise only). `username`/`password` are deprecated in favour of `basic_auth`; the usual `http_config` (TLS, authorization) also applies.
- `services`: list of services to fetch; if omitted, all services are scraped.
- Two Consul APIs are used: the Catalog API lists services (when `services` is empty, or when `tags` or `filter` are set) and the Health API returns instances with health. `filter` applies to the Catalog API and `health_filter` to the Health API. The field names differ between them (tags are `ServiceTags` in the Catalog API but `Service.Tags` in the Health API); see the Consul filtering docs for syntax.
- `tags` (service must contain all listed tags) and `node_meta` are deprecated in favour of `filter` / `health_filter` (as of Consul 1.14).
- `tag_separator` (default `,`) is the string used to join tags into `__meta_consul_tags`.
- `allow_stale` defaults to true (reduces load on Consul); `refresh_interval` defaults to `30s` and the page suggests raising it on large setups because the catalog changes all the time.

Meta labels: `__meta_consul_address`, `__meta_consul_dc`, `__meta_consul_health`, `__meta_consul_partition`, `__meta_consul_metadata_<key>` (node metadata), `__meta_consul_node`, `__meta_consul_service_address`, `__meta_consul_service_id`, `__meta_consul_service_metadata_<key>`, `__meta_consul_service_port`, `__meta_consul_service`, `__meta_consul_tagged_address_<key>`, `__meta_consul_tags`.

## 2. DNS
```yaml
  - job_name: dns-srv
    dns_sd_configs:
      - names: ["_metrics._tcp.app.example.com"]
        type: SRV
        refresh_interval: 30s
  - job_name: dns-a
    dns_sd_configs:
      - names: ["node-exporter.example.internal"]
        type: A
        port: 9100
```
- `names`: DNS names to query. `type` is one of `SRV` (default), `A`, `AAAA`, `MX`, `NS`. `port` is used when the type is not SRV. `refresh_interval` defaults to `30s`.
- The DNS servers come from `/etc/resolv.conf`. Only basic A, AAAA, MX, NS and SRV queries are supported, not RFC 6763 DNS-SD.
- Meta labels: `__meta_dns_name` (the record name that produced the target), `__meta_dns_srv_record_target`, `__meta_dns_srv_record_port`, `__meta_dns_mx_record_target`, `__meta_dns_ns_record_target`.

## 3. Choosing between them
| Need | Use |
|---|---|
| tags, service and node metadata, health status labels | Consul |
| no registry, plain DNS records | DNS SRV (port comes from the record) or A/AAAA with `port` |
| Nomad jobs | `nomad_sd_configs` (listed in the scrape_config reference; its options were not read here) |

## Verify
- [ ] The Prometheus targets / service-discovery page lists the targets you expect after relabeling.
- [ ] After removing a service from Consul or DNS, its target disappears within about `refresh_interval`.

## Checked
Date: 2026-11-07. Read: the `<consul_sd_config>` and `<dns_sd_config>` sections of the Prometheus configuration page (the page is ~3600 lines; I read only those two sections plus the scrape_config section heads, not the rest). Trims: removed the `token_file` option, the example filter expression and field names (`ServiceMeta...`), "default `__address__` is ServiceAddress:ServicePort", the blocking-query / 500 long-polls explanation, the `,tag,` leading-separator claim and the canary relabel, the health values `passing/warning/critical`, the headless-service and `kubernetes_sd` RBAC advice, the claims that DNS TTL is ignored and that Terminating pods stay in A records, the "Consul SD retries forever on ACL errors" log message, the Nomad `__meta_nomad_*` labels and the `dig` verify. Removed the cited file_sd guide from sources (no claim now rests on it). Note the draft's `tags` filter is deprecated per the page.
Method: documentation only; no commands were run.
