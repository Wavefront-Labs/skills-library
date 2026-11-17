---
id: computing-software.systems-network-administration.bash.bash-dev-tcp-redirection
name: bash-dev-tcp-redirection
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, dev-tcp, dev-udp, port-check, bash-networking, no-netcat, redirection]
level: practitioner
status: docs-checked
description: "Use bash's /dev/tcp and /dev/udp pseudo-files to test ports, send HTTP requests or banners from minimal hosts without nc/curl, with timeouts and limits."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/Redirections.html
  - https://tldp.org/LDP/abs/html/devref1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bash /dev/tcp networking

Bash interprets `/dev/tcp/HOST/PORT` and `/dev/udp/HOST/PORT` in redirections: with a valid
hostname or Internet address and a port number or service name it opens the corresponding TCP
or UDP socket. Useful on minimal hosts without `nc`, `curl` or `telnet`.

## Port check
```bash
timeout 3 bash -c '</dev/tcp/db01/5432' && echo open || echo "closed/filtered"
for p in 22 80 443 5432; do timeout 2 bash -c "</dev/tcp/10.0.0.5/$p" 2>/dev/null && echo "$p open"; done
```
Wrap the attempt in `timeout` so a filtered port cannot hang the check.

## Simple HTTP request
```bash
exec 3<>/dev/tcp/example.com/80
printf 'GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n' >&3
cat <&3
exec 3>&-
```
This is plain TCP with no TLS.

## Banner grab / send data
```bash
timeout 3 bash -c 'exec 3<>/dev/tcp/mail01/25; head -1 <&3'      # SMTP banner
echo "<14>myhost test: hello" > /dev/udp/syslog01/514             # UDP datagram, no reply read
```

## Gotchas
- These are bash features; use `#!/bin/bash`, not a plain `sh` script.
- UDP gives no handshake, so a successful write says nothing about delivery.

## Verify
- [ ] The port-check result matches a known-open and a known-closed port.

## Checked
2026-11-01: confirmed against the Bash Reference Manual (Redirections) and the Advanced Bash-Scripting Guide (/dev/tcp pseudo-device, exec file-descriptor use). Removed: timeout durations, build-flag remark, IPv6 and resolver remarks, EDR remark, Graphite example, ss cross-check.
Method: documentation only; no commands were run.
