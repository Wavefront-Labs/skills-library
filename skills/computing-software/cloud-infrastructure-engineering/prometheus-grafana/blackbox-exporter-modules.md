---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.blackbox-exporter-modules
name: blackbox-exporter-modules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [blackbox-exporter, blackbox-modules, http-probe-config, icmp-probe, dns-probe, tcp-probe, grpc-probe, multi-target-exporter]
level: practitioner
status: docs-checked
description: "Write blackbox_exporter modules for HTTP (status, body regex, TLS), TCP/TLS with query-response, ICMP, DNS and gRPC probes, and the multi-target scrape relabeling."
sources: ["https://github.com/prometheus/blackbox_exporter/blob/master/CONFIGURATION.md", "https://prometheus.io/docs/guides/multi-target-exporter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# blackbox_exporter modules

```yaml
modules:
  http_2xx_json:
    prober: http
    timeout: 5s
    http:
      method: GET
      valid_status_codes: [200]            # default 2xx
      fail_if_body_not_matches_regexp: ['"status":\s*"ok"']
      fail_if_not_ssl: true
      preferred_ip_protocol: ip4           # default ip6; ip_protocol_fallback (default true) allows the other family
      headers: {Accept: application/json}
      tls_config: {insecure_skip_verify: false}
  http_post_login:
    prober: http
    http: {method: POST, body: '{"user":"probe"}', valid_status_codes: [200, 401]}
  tcp_smtp_starttls:
    prober: tcp
    tcp:
      query_response:
        - expect: "^220"
        - send: "EHLO probe\r"
        - expect: "^250-STARTTLS"
        - send: "STARTTLS\r"
        - expect: "^220"
        - starttls: true
  icmp:
    prober: icmp
    icmp: {preferred_ip_protocol: ip4}
  dns_a_record:
    prober: dns
    dns:
      query_name: shop.example.com
      query_type: A
      valid_rcodes: [NOERROR]
      validate_answer_rrs: {fail_if_not_matches_regexp: ['shop\.example\.com\.\t.*\tIN\tA\t.*']}
  grpc_health:
    prober: grpc
    grpc: {tls: true, service: ""}         # service: the service name to query for health status
```

## Scrape (multi-target pattern)
```yaml
- job_name: blackbox-http
  metrics_path: /probe
  params: {module: [http_2xx_json]}
  static_configs: [{targets: [https://shop.example.com/healthz]}]
  relabel_configs:
    - {source_labels: [__address__], target_label: __param_target}
    - {source_labels: [__param_target], target_label: instance}
    - {target_label: __address__, replacement: blackbox-exporter:9115}
```
For DNS probes the target is the **resolver** (`8.8.8.8:53`), not the name.

## Gotchas
- ICMP needs elevated privileges: on Linux a user in a group within `net.ipv4.ping_group_range`, the `CAP_NET_RAW`
  capability (in Kubernetes via `securityContext.capabilities.add: [NET_RAW]`) or root.
- The probe timeout is derived from Prometheus' `scrape_timeout`, slightly reduced for network delays; a module's
  `timeout` is how long the probe waits before giving up. Keep `scrape_timeout` above the module timeout.
- Debug: `curl 'blackbox:9115/probe?target=https://shop.example.com&module=http_2xx_json&debug=true'`.

## Checked
2026-10-28. Confirmed in blackbox_exporter CONFIGURATION.md and README: module fields (`prober`, `timeout`, `http`
`valid_status_codes` default 2xx, `method`, `headers`, `fail_if_not_ssl`, `fail_if_body_not_matches_regexp`, `tls_config`,
`preferred_ip_protocol` default ip6 and `ip_protocol_fallback` default true), tcp `query_response` (`expect`, `send`,
`starttls`), dns (`query_name`, `query_type`, `valid_rcodes`, `validate_answer_rrs`; the target is the DNS server), icmp, grpc
(`tls`, `service`), ICMP privilege options, timeout derivation, `debug=true`, `probe_success`, `probe_duration_seconds` and
`probe_timeout_seconds`. Removed: the 0.5 s timeout formula, the grpc.health.v1 label, two probe metric names not found in the docs.
The SMTP dialogue and DNS answer regexp are illustrative examples.
Method: documentation only; no commands were run.

## Verify
- [ ] `probe_success == 1` per target; debug output shows each check passing.
- [ ] `probe_duration_seconds / probe_timeout_seconds` shows how much of the timeout each probe uses.
