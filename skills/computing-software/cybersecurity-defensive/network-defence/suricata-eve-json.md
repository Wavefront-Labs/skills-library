---
id: computing-software.cybersecurity-defensive.network-defence.suricata-eve-json
name: suricata-eve-json
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [eve-json, suricata, eve-log, flow-records, alert-metadata, siem-ingestion, ids-ips]
level: practitioner
status: docs-checked
description: "Configure Suricata EVE JSON output: event types, community ID, metadata and payload options, file rotation, output transports and using flow/protocol logs for hunts."
sources: ["https://docs.suricata.io/en/latest/output/eve/eve-json-output.html", "https://docs.suricata.io/en/latest/output/eve/eve-json-format.html", "https://docs.suricata.io/en/latest/output/log-rotation.html", "https://docs.suricata.io/en/latest/unix-socket.html", "https://github.com/corelight/community-id-spec"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suricata EVE JSON output

EVE is Suricata's single JSON log stream: alerts plus protocol metadata (dns, http, tls, flow, fileinfo,
smb, ssh, anomaly) - effectively a Zeek-like NSM log alongside IDS alerts.

## Config (suricata.yaml)
```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: regular        # or unix_stream, redis, syslog
      filename: eve.json
      community-id: true       # cross-tool flow correlation with Zeek, Elastic
      types:
        - alert:
            metadata:          # app-layer/flow context on alerts (default yes); rule keys below
              rule:
                metadata: true # log the rule metadata keyword under alert.metadata
            tagged-packets: yes
            # payload: yes    # adds base64 payload (off in the shipped config) - privacy/size trade-off
        - anomaly: { enabled: yes }
        - http: { extended: yes }
        - dns: { version: 3 }      # 3 is the 8.0 format; 7.x style is version 2
        - tls: { extended: yes }   # custom: [..., ja3, ja3s, ja4] needs ja3/ja4-fingerprints enabled
        - files: { force-magic: no }
        - flow
        - stats: { totals: yes, threads: no }
```
Use `eve-log` multiple instances to split alerts and protocol logs into different files/indices.

## Fields to know
`event_type`, `flow_id` (joins alert to its flow/http/tls records), `community_id`, `src_ip/dest_ip`,
`app_proto`, `alert.signature_id`, `alert.action` (allowed/blocked), `alert.metadata`.

## Shipping
- The default `regular` file holds one JSON object per line, so any log shipper can tail it; other `filetype` values are `syslog`, `unix_dgram`, `unix_stream` and `redis`.
- Rotate with logrotate plus a SIGHUP to Suricata (it closes and reopens its log files), or run `suricatasc -c reopen-log-files` after external rotation. Eve also has its own date-based rotation; deleting old files is still up to you.

## Hunting with EVE
- Pivot from an alert's `flow_id` to its dns/http/tls records.
- Rare TLS SNI / JA4 values, DNS to newly seen domains, long flows with low bytes (beacons).

## Gotchas
- Flow + all protocol logs can be many times the alert volume; size the SIEM or filter (e.g. drop flow for internal backup traffic).
- Payload logging may capture personal data/credentials.

## Verify
- [ ] Alerts in the SIEM carry `flow_id`, `community_id` and metadata.
- [ ] Stats events show no growing drops.

## Checked

Checked 2026-10-25 against Suricata user guide source (OISF/suricata doc/userguide, main branch, last pushed 2026-10-23, 8.x documentation). Confirmed: the `filetype` values, `community-id` (boolean, with optional `community-id-seed`), `tagged-packets`, `payload` (commented out in the shipped config), `http`/`tls` `extended`, `files` `force-magic`, `stats` `totals`/`threads`, alert `action` values (allowed or blocked), SIGHUP log reopening and the `reopen-log-files` socket command. Corrected: rule metadata is logged through the nested `metadata: rule: metadata: true` option; the DNS log format is version 3 in Suricata 8.0 (version 2 is the 7.x style); JA3/JA4 fields depend on the fingerprint options. Removed unconfirmed Elastic/Splunk shipping details and the volume multiplier.

Method: documentation only; no commands were run.
