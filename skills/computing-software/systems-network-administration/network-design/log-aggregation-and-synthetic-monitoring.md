---
id: computing-software.systems-network-administration.network-design.log-aggregation-and-synthetic-monitoring
name: log-aggregation-and-synthetic-monitoring
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-monitoring, log-aggregation, siem, syslog-ng, rsyslog, graylog, elastic, synthetic-monitoring, blackbox-exporter, thousandeyes, smokeping, dns-probe, http-probe, sla-monitoring]
level: practitioner
status: docs-checked
description: "Centralise network logs (syslog collectors, parsing, retention, SIEM use cases) and add synthetic DNS/HTTP/latency probes that catch user-visible failures early."
sources:
  - https://www.rsyslog.com/doc/
  - https://github.com/prometheus/blackbox_exporter
  - https://oss.oetiker.ch/smokeping/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log aggregation and synthetic monitoring

## Log aggregation
Pipeline: devices -> syslog collector(s) -> parsing/enrichment -> store/search platform
-> SIEM rules.
- Collector: rsyslog (or another syslog daemon) on two hosts behind a VIP or with devices sending to both.
  Example rsyslog listeners (from the imudp and imtcp module docs); per-device files use omfile with a
  dynamic file name (dynaFile) built from a template:
  ```
  module(load="imudp") input(type="imudp" port="514")
  module(load="imtcp") input(type="imtcp" port="514")
  ```
- Parse vendor message formats into fields; enrich with site/role from your
  source of truth.
- Retention: set by policy and compliance requirements.
- Clocks: all devices on NTP, UTC preferred (see clock-timezone-and-log-timestamps).

Useful network SIEM use cases: config-change messages outside change windows, login
failures/brute force on devices, BPDU guard/port security/DAI violations, interface flaps on core
links, new device MAC on sensitive ports, VPN logins from unusual countries.

## Synthetic monitoring
Measures what users experience, independent of device health:
| Probe | Tool | Catches |
|---|---|---|
| ICMP latency/loss to key sites and WAN peers | SmokePing, blackbox_exporter icmp prober | degradation, loss trends |
| DNS resolution of critical names | blackbox_exporter dns module, `dig` checks | resolver failures, wrong answers |
| HTTP(S) transaction (status, TLS, timing) | blackbox_exporter http prober | app/proxy/firewall failures |
| Path visibility across ISPs/SaaS | commercial path-monitoring services | upstream provider problems |
Place probes **at user sites** (branch agents), not only in the data centre.

blackbox_exporter module example:
```yaml
modules:
  dns_corp:
    prober: dns
    dns: {query_name: "intranet.corp.example", query_type: "A", valid_rcodes: [NOERROR]}
```

## Verify
- [ ] Logs from every device class searchable within a minute of generation.
- [ ] At least one SIEM rule fires on a test config change outside the window.
- [ ] Synthetic probes from two sites alert on a simulated DNS failure.

## Checked

2026-10-28: Confirmed: rsyslog imudp and imtcp module examples (module(load=...) with input(type=... port=...)), omfile dynaFile, blackbox_exporter modules with prober dns, query_name, query_type and valid_rcodes (CONFIGURATION.md), icmp and http probers, SmokePing as a latency measurement tool. Removed: 90-day/1-year/PCI retention figures, the Cisco message mnemonic names, the per-device rsyslog template and source-IP filter lines, and product names (Graylog, Elastic, Loki, Splunk, syslog-ng, IP SLA, Uptime Kuma, ThousandEyes, Catchpoint) that no fetched page covered.
Method: documentation only; no commands were run.
