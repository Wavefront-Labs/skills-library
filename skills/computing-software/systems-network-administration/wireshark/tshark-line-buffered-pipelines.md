---
id: computing-software.systems-network-administration.wireshark.tshark-line-buffered-pipelines
name: tshark-line-buffered-pipelines
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, line-buffered, live-pipelines, alerting]
level: practitioner
status: verified
description: "Stream tshark output live into grep, awk or alerting scripts with -l and --line-buffered so lines are not stuck in stdio buffers."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Line-buffered live tshark pipelines

When stdout is a pipe, tshark buffers output in blocks: a quiet link prints nothing for minutes.

## Fix
```
tshark -i <interface> -l -Y dns.flags.rcode==3 -T fields -e frame.time -e ip.src -e dns.qry.name | \
  grep --line-buffered -v '\.local$' | while read t src q; do logger "NXDOMAIN $src $q"; done
```
- `-l` flushes stdout after each packet (man page). The pipeline above ran against a file (`-r`) and printed `10.0.0.5 xxxxxxxxxxxx` / `8.8.8.8 www.example.`.
- Every stage needs line buffering: `grep --line-buffered`, `awk ... fflush()`, `sed -u`,
  `stdbuf -oL cmd` for others.
- Python 3 consumers: `for line in sys.stdin` delivered the first line immediately in a test (`(echo a; sleep 2; echo b) | python ...` printed `a` at 0.0 s),
  so the buffering problem was the upstream stage: plain `sed -n p` held `a` for 2.0 s, `sed -u` does not buffer.

## Useful patterns
```
tshark -i <interface> -l -f "tcp[tcpflags] & tcp-rst != 0" -T fields -e ip.src -e tcp.srcport | uniq -c   # filter compiles (checked with dumpcap -d)
tshark -i <interface> -l -q -z io,stat,10          # statistics print only at the end; use a ring buffer + periodic stats instead
```

## Long-running considerations
- Live display filters (`-Y`) keep state for reassembly; memory can grow on long runs. Restart
  periodically, use `-f` capture filters instead of `-Y`, or use `-M <n>`: "automatically reset internal session when reached to specified
  number of packets" (it printed `resetting session.` on a 13-packet file with `-M 5`; not compatible with `-2`).
- `-a duration:3600` stops after an hour; wrap in a loop or a service unit.

## Verify
- [ ] Generate one matching packet and see the line appear at the end of the pipeline within a second.
