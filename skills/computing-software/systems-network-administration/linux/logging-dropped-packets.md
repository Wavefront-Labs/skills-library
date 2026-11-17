---
id: computing-software.systems-network-administration.linux.logging-dropped-packets
name: logging-dropped-packets
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, firewall-logging, nflog, log-prefix, logdenied, firewalld, nftables-log, iptables-log, ulogd, rate-limit, security, troubleshooting, sysadmin]
level: practitioner
status: docs-checked
description: "Log what the firewall drops on Linux: firewalld LogDenied, nftables/iptables log rules with prefixes and rate limits, NFLOG to ulogd, and reading the kernel log fields."
sources:
  - https://firewalld.org/documentation/man-pages/firewalld.conf.html
  - https://wiki.nftables.org/wiki-nftables/index.php/Logging_traffic
  - https://www.netfilter.org/projects/ulogd/
  - https://firewalld.org/documentation/man-pages/firewalld.richlanguage.html
  - https://ipset.netfilter.org/iptables-extensions.man.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Logging dropped packets

**Goal:** see exactly which packets the firewall rejects — to debug "port is open but it
doesn't work" or to watch scans — without flooding the journal.

## 1. firewalld
```bash
firewall-cmd --get-log-denied
firewall-cmd --set-log-denied=unicast     # all | unicast | broadcast | multicast | off
journalctl -k -g 'REJECT|DROP' -f
```
`LogDenied` adds logging rules right before the reject and drop rules in INPUT, FORWARD and OUTPUT and in the final
reject/drop rules of zones; default `off`. Turn it back `off` after debugging on busy hosts. Targeted logging: a
rich rule with `log prefix="..." level="info" limit value="5/m"`; the rich-rule `nflog` action takes `group`, `prefix`,
`queue-size` and `limit`.

## 2. nftables
```
chain input {
  type filter hook input priority 0; policy drop;
  ct state established,related accept
  iif lo accept
  tcp dport { 22, 443 } accept
  limit rate 10/minute burst 20 packets log prefix "nft-drop: " level info flags all
  counter drop
}
```
Place the log rule **immediately before** the drop/policy, after all accepts. `flags all` adds TCP
sequence and options, IP options, the socket UID and link-layer addresses (nftables wiki, available since nftables 0.7).
The `log` statement also takes `level`, `snaplen`, `queue-threshold` and `group` (NFLOG group). Rules are evaluated left to
right, so put `log` after the match (`log` before `tcp dport 22` logs every packet).

## 3. iptables (legacy)
```bash
iptables -N LOGDROP
iptables -A LOGDROP -m limit --limit 10/min --limit-burst 20 -j LOG --log-prefix "ipt-drop: " --log-level 4
iptables -A LOGDROP -j DROP
iptables -A INPUT -j LOGDROP              # last rule of INPUT
```

## 4. Separate log file
- rsyslog: filter on the prefix text and write matching messages to their own file (see the rsyslog filter docs).
- NFLOG to ulogd (userspace logging via the nflog infrastructure): nft `log group 1 prefix "drop"`
  / iptables `-j NFLOG --nflog-group 1`; ulogd then reads that group and writes to a file or database.

## 5. Reading a line
`nft-drop: IN=eth0 OUT= MAC=... SRC=198.51.100.9 DST=10.0.10.20 LEN=60 TTL=52 PROTO=TCP SPT=51234 DPT=3306 WINDOW=64240 SYN`
- `IN=` set, `OUT=` empty: traffic to this host (input); both set: forwarded.
- `SYN` only: a new connection attempt.

## Gotchas
- Unlimited logging during a scan can fill disks and slow the box; always `limit`.
- Missing log lines do not prove no drops: check rule counters.

## Checked
2026-11-01. Confirmed: firewalld.conf `LogDenied` values and default and placement, `firewall-cmd --get-log-denied` /
`--set-log-denied`, rich-rule `log`/`nflog` syntax and `limit` (firewalld pages); nft `log` flags, level, group, ordering
(nftables wiki); iptables `LOG` and `NFLOG` option names and `limit-burst` (iptables-extensions man). Removed: chain-name
prefix claim, ulogd and rsyslog config syntax, interpretive log-line claims.
Method: documentation only; no commands were run.

## Verify
- [ ] A test connection to a closed port produces exactly one log line with the expected prefix, SRC and DPT.
- [ ] Rule counters (`nft list ruleset` / `iptables -vnL`) increase together with the log; log volume stays within the rate limit.
