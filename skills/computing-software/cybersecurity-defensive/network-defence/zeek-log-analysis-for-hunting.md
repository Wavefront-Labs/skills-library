---
id: computing-software.cybersecurity-defensive.network-defence.zeek-log-analysis-for-hunting
name: zeek-log-analysis-for-hunting
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-security-monitoring, zeek-log-analysis, zeek, conn-log, zeek-cut, uid-pivoting, dns-log, ssl-log, threat-hunting]
level: practitioner
status: docs-checked
description: "Hunt with Zeek logs: conn.log fields and conn_state, uid pivots across dns/http/ssl/files, zeek-cut one-liners, long connections, rare JA4/SNI, and self-signed certificates."
sources: ["https://docs.zeek.org/en/master/scripts/base/protocols/conn/main.zeek.html", "https://docs.zeek.org/en/master/scripts/base/protocols/dns/main.zeek.html", "https://docs.zeek.org/en/master/scripts/base/protocols/http/main.zeek.html", "https://docs.zeek.org/en/master/scripts/base/protocols/ssl/main.zeek.html", "https://docs.zeek.org/en/master/scripts/policy/protocols/ssl/validate-certs.zeek.html", "https://github.com/zeek/zeek/tree/master/tools/zeek-cut"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zeek log analysis for hunting

## Core logs
- `conn.log`: every connection; `uid`, `id.orig_h/p`, `id.resp_h/p`, `proto`, `service`, `duration`,
  `orig_bytes`, `resp_bytes`, `conn_state`, `history`, `missed_bytes`.
- `dns.log` (query, qtype_name, rcode_name, answers), `http.log` (host, uri, user_agent, status_code),
  `ssl.log` (server_name/SNI, version, cipher; `validation_status` comes from the
  `policy/protocols/ssl/validate-certs` script and JA3/JA4 columns from packages),
  `x509.log`, `files.log` (mime_type, source; hashes only when a hash analyzer runs, e.g. `frameworks/files/hash-all-files`),
  `notice.log`, `weird.log`.
- `uid` links one connection across logs; `fuid` links files.

## conn_state cheat sheet
`S0` attempt no reply (scans), `REJ` rejected, `SF` normal established and closed, `S1` established
not closed (long-lived), `RSTO/RSTR` reset by originator/responder, `OTH` midstream (sensor saw only part).

## One-liners (TSV logs)
```
# top talkers by bytes out
zeek-cut id.orig_h id.resp_h orig_bytes < conn.log | sort -k3 -nr | head
# long connections (> 1 hour)
zeek-cut id.orig_h id.resp_h id.resp_p duration < conn.log | awk '$4 > 3600' | sort -k4 -nr | head
# rare TLS server names
zeek-cut server_name < ssl.log | sort | uniq -c | sort -n | head -50
# self-signed or invalid certs on outbound
zeek-cut id.orig_h id.resp_h server_name validation_status < ssl.log | grep -v '^.*ok$'
# DNS: long or high-entropy query names (tunnelling candidates)
zeek-cut query < dns.log | awk 'length($1) > 60' | sort | uniq -c | sort -nr | head
# pivot by uid
grep CHhAvVGS1DHFjwGM9 *.log
```
JSON logs: `jq -r 'select(.duration > 3600) | [.["id.orig_h"], .["id.resp_h"], .duration] | @tsv' conn.log`.

## Hunt ideas
- Internal hosts talking directly to the internet on 53/123/25 bypassing your resolvers/relays.
- HTTP with unusual user agents, or POSTs to IPs without Host names.
- `files.log` executables (`mime_type=application/x-dosexec`) downloaded over HTTP.
- Beaconing: connection counts per (src, dst) with low variance in intervals.
- SMB/RDP between workstations (east-west lateral movement).

## Gotchas
- `missed_bytes > 0` is the number of bytes missed in content gaps and is representative of packet loss: absent evidence may be capture gaps.
- `orig_bytes`/`resp_bytes` are payload bytes; for TCP they are taken from sequence numbers and may be inaccurate.
- Zeek timestamps are epoch seconds in UTC.

## Verify
Generate known traffic from a test host (DNS query, HTTPS download) and find it in dns/ssl/conn with
matching uid and correct bytes.

## Checked

Checked 2026-10-25 against the Zeek base and policy scripts that define the logs (Zeek sources (zeek/zeek master, last pushed 2026-10-23: doc/frameworks, tools/zeek-cut, base and policy scripts, event definitions)). Confirmed: conn.log fields and the `conn_state` values (S0, S1, SF, REJ, RSTO, RSTR, OTH), `missed_bytes` meaning, `uid` as the cross-log key, epoch `ts`, dns/http/ssl field names, and that `validation_status` is added by the validate-certs policy script. Corrected: `status_code` (not `status`) in http.log, no `mime` column in http.log, `qtype_name`/`rcode_name` for readable DNS columns, hashes in files.log require a hash analyzer. Removed the RITA remark, the asymmetric routing claim and the prose blog source.

Method: documentation only; no commands were run.
