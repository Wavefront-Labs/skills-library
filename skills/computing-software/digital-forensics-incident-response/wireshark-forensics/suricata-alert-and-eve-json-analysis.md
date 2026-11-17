---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.suricata-alert-and-eve-json-analysis
name: suricata-alert-and-eve-json-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [suricata, eve-json, ids-alerts, jq, pcap-replay, network-security-monitoring, dfir]
level: practitioner
status: docs-checked
description: "Run Suricata over pcaps and triage EVE JSON alerts, flow, DNS, HTTP, TLS and fileinfo records with jq, separating true positives from noise."
sources: ["https://docs.suricata.io/en/latest/output/eve/eve-json-format.html", "https://docs.suricata.io/en/latest/output/eve/eve-json-output.html", "https://docs.suricata.io/en/latest/command-line-options.html", "https://docs.suricata.io/en/latest/configuration/suricata-yaml.html", "https://rules.emergingthreats.net/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Suricata alert and EVE JSON analysis

**Goal:** use Suricata both live (sensor alerts) and offline (replaying incident pcaps with
current rules) and analyse its EVE JSON output efficiently.

## Offline run on a pcap
```bash
suricata-update                                   # fetch ET Open (and enabled sources)
suricata -r capture.pcapng -l out/ -k none        # -k none: ignore checksum errors from offload
suricata -r capture.pcapng -l out/ -S local.rules # only your rules
```
Output in `out/`: `eve.json` (one JSON event per line) and `fast.log` by default. Enable the `file-store`
output (`version: 2`, `enabled: yes`) in `suricata.yaml` to write extracted files to disk.

## EVE event types
`alert`, `flow`, `dns`, `http`, `tls`, `fileinfo`, `smb`, `ssh`, `quic`, `anomaly`,
`stats`. Events share `flow_id` (link alerts to the related DNS/HTTP/TLS records); `community_id` is added when
`community-id: true` is set on the eve-log output (pivot to Zeek and other tools).

## jq recipes
```bash
jq -c 'select(.event_type=="alert") | [.timestamp,.src_ip,.dest_ip,.dest_port,.alert.signature_id,.alert.signature]' eve.json
jq -r 'select(.event_type=="alert") | .alert.signature' eve.json | sort | uniq -c | sort -rn   # signature histogram
jq -c 'select(.flow_id==1234567890)' eve.json          # everything for one flow
jq -r 'select(.event_type=="tls") | [.dest_ip,.tls.sni,.tls.ja3.hash // "",.tls.subject] | @tsv' eve.json
jq -r 'select(.event_type=="fileinfo") | [.fileinfo.filename,.fileinfo.sha256,.http.hostname] | @tsv' eve.json
jq -r 'select(.event_type=="dns" and .dns.type=="request") | .dns.queries[].rrname' eve.json | sort | uniq -c | sort -rn | head   # DNS log version 3 (Suricata 8)
jq -r 'select(.event_type=="dns" and .dns.type=="query") | .dns.rrname' eve.json | sort | uniq -c | sort -rn | head   # version 2 (7.x)
```

## Triage approach
1. Histogram signatures; ignore policy and informational rules unless relevant and focus on malware,
   trojan, exploit and command-and-control hits (use the rule `msg` prefix and `classtype` of your ruleset).
2. For each high-severity alert, pull the flow (`flow_id`) and adjacent protocol records,
   then open the packets in Wireshark (filter by 5-tuple and time).
3. Read the rule (`grep -r 'sid:<sid>;' /var/lib/suricata/rules/`) to know what it actually
   matched; many hits are content matches on benign traffic.
4. Retro-hunt: replay older captures with today's rules to find earlier activity of a newly
   discovered threat.

## Gotchas
- Captures taken on checksum-offloading NICs contain "bad" checksums; `-k none` disables checksum checks so those packets are still processed.
- Alerts are leads; confirm with payload and host evidence before declaring compromise.
- Large eve.json: index it in a SIEM rather than reading it with jq.

## Self-check
For each confirmed alert you have flow ID, rule logic understood, packet evidence and a host
correlation.

## Checked

Checked 2026-10-25 against Suricata user guide source (OISF/suricata doc/userguide, main branch, last pushed 2026-10-23, 8.x documentation). Confirmed: `-r`, `-l`, `-S`, `-k [all|none]` options, default alert output to `eve.json` and `fast.log`, the `file-store` output (`version: 2`), the event types listed, field names used in the jq recipes (`flow_id`, `alert.signature_id`, `alert.signature`, `tls.sni`, `tls.subject`, `tls.ja3.hash`, `fileinfo.filename`, `fileinfo.sha256`, `http.hostname`), `community-id` as an option. Corrected: DNS events use `type` request/response with a `queries` array in the version 3 format introduced in Suricata 8.0 (`query`/`rrname` is the version 2 shape). Removed the unconfirmed ET category prefixes, the silent-miss claim and the DuckDB suggestion.

Run 2026-11-01: all seven jq recipes executed with jq 1.8.2 against a hand-made eve.json fixture shaped like the documented records (alert, tls with and without `ja3`, fileinfo, DNS version 3 `request`/`queries[]` and version 2 `query`/`rrname`); each returned the expected rows and the `// ""` fallback printed an empty field. This checks the jq syntax only, not Suricata's real output. Suricata itself was not installed, so the `suricata` and `suricata-update` commands are unrun and the status stays docs-checked.

Method: documentation, plus the jq recipes run on a fixture; the Suricata commands were not run.
