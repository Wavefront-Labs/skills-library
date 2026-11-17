---
id: computing-software.cybersecurity-defensive.zeek.conn-log-analysis
name: conn-log-analysis
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, conn-log, conn-state, history-field, ip-proto]
level: practitioner
status: docs-checked
description: "Read Zeek conn.log with jq: who talked to whom, duration, orig and resp bytes versus IP bytes, conn_state SF, decoding the history string, UDP records and ip_proto."
sources: ["https://docs.zeek.org/en/current/reference/logs/conn.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# conn.log analysis

`conn.log` tracks TCP and UDP (and other) connections: who talked to whom, when, for how long, with what protocol. Full field meanings are in `Conn::Info`. View JSON logs with `jq . -c conn.log`.

Key fields: `ts`, `uid`, `id.orig_h/p`, `id.resp_h/p`, `proto`, `service`, `duration`, `orig_bytes`/`resp_bytes` (application payload), `orig_ip_bytes`/`resp_ip_bytes` (IP packet level), `orig_pkts`/`resp_pkts`, `conn_state`, `missed_bytes`, `history`.

`conn_state` of `SF` means normal establishment and termination. For TCP that is a graceful close. For UDP, which has no state, SF means Zeek judged it a normal exchange.

`history` letters: uppercase means the originator did it, lowercase the responder. For `ShADadFf`:

- S originator SYN
- h responder SYN ACK
- A originator ACK
- D originator sent payload data
- a responder ACK
- d responder sent payload data
- F originator FIN
- f responder FIN

A UDP record with `Dd` means each party sent data. You can verify byte counts against a packet decode with tshark.

`ip_proto` (marked as added in 7.1) is the numeric IP protocol and is always present, including for non-transport flows such as OSPF, where `proto` is `unknown_transport` and `conn_state` may be `OTH`. Load `policy/protocols/conn/ip-proto-name-logging.zeek` for names.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
