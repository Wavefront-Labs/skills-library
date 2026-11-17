---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.querying-zeek-logs-with-zeek-cut
name: querying-zeek-logs-with-zeek-cut
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [zeek-cut, zeek, conn-log, network-forensics, command-line, dfir]
level: practitioner
status: docs-checked
description: "Query Zeek TSV logs from the command line with zeek-cut: field selection, human-readable timestamps, joining by uid across conn, dns, http and ssl logs, and JSON-log equivalents with jq."
sources: ["https://github.com/zeek/zeek/blob/master/tools/zeek-cut/zeek-cut.1", "https://github.com/zeek/zeek/tree/master/tools/zeek-cut", "https://docs.zeek.org/en/master/scripts/base/protocols/conn/main.zeek.html", "https://docs.zeek.org/en/master/quickstart.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Querying Zeek logs with zeek-cut

Zeek's default logs are tab-separated with a header describing fields. `zeek-cut` selects columns by name so pipelines survive field-order changes.

## Basics
```bash
cat conn.log | zeek-cut ts uid id.orig_h id.resp_h id.resp_p proto service duration orig_bytes resp_bytes conn_state
zeek-cut -d ts id.orig_h query < dns.log          # -d: ISO 8601 timestamps (local); -u for UTC
zcat conn.*.log.gz | zeek-cut -u ts id.orig_h id.resp_h resp_bytes
zeek-cut -c ts uid < conn.log                      # -c: include the first header block (-C: all header blocks)
zeek-cut -n ts uid < conn.log                      # -n: print all fields except those named
```
`-D <fmt>` / `-U <fmt>` give custom strftime formats (local time / UTC); the `ZEEK_CUT_TIMEFMT` environment variable sets the format used by `-d` and `-u`.

## Recipes
```bash
# top talkers by bytes sent out
zeek-cut id.orig_h orig_bytes < conn.log | awk '{b[$1]+=$2} END{for(h in b) print b[h],h}' | sort -rn | head
# long connections (possible C2 or tunnels), over 1 hour
zeek-cut -u ts uid id.orig_h id.resp_h id.resp_p duration < conn.log | awk '$6 > 3600'
# rare destination ports
zeek-cut id.resp_p < conn.log | sort | uniq -c | sort -n | head
# DNS names queried by one host
zeek-cut id.orig_h query < dns.log | awk '$1=="10.1.2.3"{print $2}' | sort | uniq -c | sort -rn
# TLS SNI and JA3 per host
zeek-cut id.orig_h server_name < ssl.log | sort | uniq -c | sort -rn   # JA3/JA4 columns exist only with the matching package
```

## Joining by uid
Every log tied to a connection carries `uid`. zeek-cut needs the intact header block, so filter after cutting, not before:
```bash
zeek-cut -u ts uid host uri user_agent status_code < http.log | awk '$2 == "CwX3pG2cjl0oFQ1aqb"'
```
In `files.log` the connection link is `uid` (with `id`): since Zeek 5.1 there is one entry per connection that carried the file, all sharing the same `fuid`; older versions used `conn_uids`.

## JSON logs
If Zeek writes JSON (`LogAscii::use_json=T`, common with SIEM shipping), `zeek-cut` does not apply; use `jq`:
```bash
jq -r 'select(.duration>3600) | [.ts, .uid, ."id.orig_h", ."id.resp_h", .duration] | @tsv' conn.log
```

## Gotchas
- `orig_bytes`/`resp_bytes` are payload bytes taken from TCP sequence numbers and may be inaccurate; `orig_ip_bytes` (IP-level bytes) is only set when `use_conn_size_analyzer` is T.
- Unset fields print as `-`; filter them out before numeric comparisons.
- Rotated logs are archived by time; include all relevant hours.

## Verify
Counts from zeek-cut pipelines for a sample host match the same query in the SIEM or a second method (e.g. jq on JSON copies).

## Checked

Checked 2026-10-25 against the zeek-cut manual page and source (zeek/zeek master, `tools/zeek-cut`, last pushed 2026-10-23) and the conn and files log definitions in the Zeek scripts. Confirmed: `-d`/`-u` (default format `%Y-%m-%dT%H:%M:%S%z`), `-D`/`-U`, `-c`/`-C`, `-n`, `ZEEK_CUT_TIMEFMT`, `zcat conn.log.gz | zeek-cut`, field-order independence, the conn and http field names, `use_json` for JSON logs, per-connection files.log entries since Zeek 5.1. Corrected: the `grep | zeek-cut` pipeline cannot work because zeek-cut requires the header block (use awk after cutting); `ja3` is not a base ssl.log column; `-c` includes only the first header block; `orig_ip_bytes` needs the conn-size analyzer. Removed the awk and compression remarks that no documentation covers.

Method: documentation only; no commands were run.
