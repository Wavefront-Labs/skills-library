---
id: computing-software.cybersecurity-defensive.splunk.sc4s-syslog-ingestion
name: sc4s-syslog-ingestion
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, syslog-ingestion, sc4s, splunk-connect-for-syslog, syslog-ng, hec, network-device-logs, udp-514]
level: practitioner
status: draft
description: "Ingest network and appliance syslog into Splunk with Splunk Connect for Syslog (SC4S): container deploy, vendor parsing, HEC output and loss-free sizing."
sources: ["https://splunk.github.io/splunk-connect-for-syslog/main/", "https://splunk.github.io/splunk-connect-for-syslog/main/gettingstarted/", "https://docs.splunk.com/Documentation/SVA/current/Architectures/Syslog"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Syslog ingestion with SC4S

**Goal:** get firewall, switch, load balancer and appliance syslog into Splunk with the
right sourcetype and timestamps, without sending UDP straight at indexers.

## Why not UDP into a forwarder
UDP 514 into a universal forwarder loses data on every restart and cannot be load-balanced
well. Splunk's validated architecture is a dedicated syslog tier: SC4S (syslog-ng in a
container) parses vendor formats and ships to Splunk over HEC.

## 1. Deploy (podman/docker + systemd)
`/opt/sc4s/env_file`:
```
SC4S_DEST_SPLUNK_HEC_DEFAULT_URL=https://hec.example.internal:8088
SC4S_DEST_SPLUNK_HEC_DEFAULT_TOKEN=<token>
SC4S_DEST_SPLUNK_HEC_DEFAULT_TLS_VERIFY=yes
```
Create indexes SC4S expects by default (`netfw`, `netops`, `netauth`, `netproxy`, `netids`,
`osnix`, `em_metrics` for its own metrics), or remap them in `splunk_metadata.csv`:
```
cisco_asa,index,fw_cisco
```
Run the published systemd unit that pulls `ghcr.io/splunk/splunk-connect-for-syslog/container3`.
Pin the image tag in production and upgrade deliberately.

## 2. Sources and ports
- Default listeners: UDP/TCP 514, TLS 6514. Vendors that cannot be identified from the
  message need a dedicated port: `SC4S_LISTEN_<VENDOR_PRODUCT>_UDP_PORT=5000`.
- Prefer TCP or TLS from senders that support it; keep UDP for devices that only do UDP.
- Put a pair of SC4S hosts behind a VIP or anycast; load-balancing UDP through a generic L7
  balancer rewrites the source IP and breaks host attribution.

## 3. Verify parsing
```
index=* sourcetype=sc4s:fallback | stats count by host
```
`sc4s:fallback` means no parser matched: add a dedicated port or a `app-parser` filter in
`/opt/sc4s/local/config/app_parsers/`. Each event carries `sc4s_vendor_product` in
indexed fields; check it is what you expect.

## Sizing and loss
- One modest SC4S node handles tens of thousands of EPS; UDP drops happen in the kernel
  first. Raise `net.core.rmem_max`/`rmem_default` and check
  `netstat -su | grep "receive buffer errors"`.
- Enable the disk buffer (on by default) so HEC outages queue rather than drop; size it for
  your longest expected Splunk outage.

## Gotchas
- Devices sending without year or timezone: set the device to RFC 5424 or ISO timestamps,
  or set the timezone per host in `vendor_context.csv`.
- Do not send SC4S output through a heavy forwarder that re-parses; you lose the vendor
  sourcetypes.

## Verify
`index=em_metrics` (or `_internal` with SC4S metrics enabled) shows per-source message
counts; compare against device-side counters for a day.
