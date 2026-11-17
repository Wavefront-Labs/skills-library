---
id: computing-software.systems-network-administration.wireshark.zeek-and-suricata-over-pcaps
name: zeek-and-suricata-over-pcaps
category: computing-software
field: systems-network-administration
product: wireshark
tags: [network-forensics, suricata, zeek-pcap, zeek, ids, conn-log, eve-json, threat-hunting]
level: practitioner
status: docs-checked
description: "Run Zeek and Suricata offline against capture files to get connection logs, protocol metadata and IDS alerts, then pivot back into Wireshark on the interesting flows."
sources: ["https://docs.zeek.org/en/master/quickstart.html", "https://docs.suricata.io/en/latest/command-line-options.html", "https://github.com/zeek/zeek/tree/master/tools/zeek-cut"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zeek and Suricata over pcaps

Wireshark is a microscope; for a 5 GB incident capture you first want a map. Zeek gives
structured logs per connection and protocol; Suricata gives signature alerts.

## Zeek
```
mkdir zeek-out && cd zeek-out
zeek -C -r ../incident.pcap local          # -C ignore checksum errors (offloaded captures)
ls      # conn.log dns.log http.log ssl.log files.log x509.log ... (a log exists only if matching traffic was seen)
```
Query with zeek-cut:
```
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p proto service duration orig_bytes resp_bytes | sort -k7 -nr | head
cat dns.log | zeek-cut query qtype_name rcode_name | sort | uniq -c | sort -rn | head
cat ssl.log | zeek-cut id.orig_h server_name version cipher
cat http.log | zeek-cut host uri user_agent status_code
```
JSON output for SIEM ingestion: `zeek -C -r x.pcap LogAscii::use_json=T`.

## Suricata
```
suricata-update                               # fetch ET Open rules
suricata -r ../incident.pcap -k none -l suricata-out/
jq 'select(.event_type=="alert") | [.timestamp,.src_ip,.dest_ip,.alert.signature]' suricata-out/eve.json | head
```
`-k none` disables checksum checks (captures from offloading NICs contain bad checksums). eve.json also
contains flow, dns, tls, http and fileinfo events.

## Pivot into Wireshark
Zeek's `uid` (conn.log) and Suricata's `flow_id` identify a connection whose 5-tuple is in the same records. Take the
addresses, ports and time range from them and filter the capture in Wireshark on those values.

## Gotchas
- Time zones: Zeek `ts` is epoch seconds; `zeek-cut -u` prints UTC and `-d` local time, so match the time format of your Wireshark view.
- Rules generate false positives; validate in the packets before declaring compromise.

## Verify
- [ ] conn.log covers the expected time span and the alert flows are found in Wireshark by
  5-tuple.

## Checked

Checked 2026-10-25 against the Zeek sources (zeek/zeek master, last pushed 2026-10-23: quickstart, zeek-cut manual page, base scripts) and Suricata user guide source (OISF/suricata doc/userguide, main branch, last pushed 2026-10-23, 8.x documentation). Confirmed: `zeek -r file local`, `-C` for checksum errors, `LogAscii::use_json=T` for JSON logs, zeek-cut usage and the conn/dns/http field names, `suricata -r`, `-k none`, `-l`, EVE event types. Corrected: `ja3` and `validation_status` are not in the base ssl.log (JA3 needs a package, `validation_status` needs the validate-certs policy script), so the example uses `version cipher`. Removed the unconfirmed tcpdump and display-filter examples, the snaplen claim and the Wireshark time zone claim.

Method: documentation only; no commands were run.
