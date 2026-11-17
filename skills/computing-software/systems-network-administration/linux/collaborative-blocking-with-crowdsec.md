---
id: computing-software.systems-network-administration.linux.collaborative-blocking-with-crowdsec
name: collaborative-blocking-with-crowdsec
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, crowdsec, cscli, bouncer, fail2ban-alternative, community-blocklist, intrusion-prevention]
level: practitioner
status: docs-checked
description: "Install CrowdSec on Linux: parsers and scenarios via collections, firewall bouncer, community blocklist, inspecting alerts and decisions, whitelists and multi-server LAPI."
sources:
  - https://github.com/crowdsecurity/crowdsec-docs/blob/main/crowdsec-docs/unversioned/getting_started/installation/linux.mdx
  - https://github.com/crowdsecurity/crowdsec-docs/tree/main/crowdsec-docs/docs/cscli
  - https://github.com/crowdsecurity/crowdsec-docs/blob/main/crowdsec-docs/unversioned/bouncers/firewall.mdx
  - https://github.com/crowdsecurity/crowdsec-docs/tree/main/crowdsec-docs/docs/log_processor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collaborative blocking with CrowdSec

CrowdSec splits detection (agent reading logs, scenarios) from enforcement (bouncers). Detected attackers are shared with, and blocklists received from, the community network.

## Install
```bash
curl -s https://install.crowdsec.net | sudo sh       # adds the CrowdSec package repository (manual repo steps are in the install docs)
apt install crowdsec crowdsec-firewall-bouncer-nftables   # -iptables variant for iptables hosts; RPM systems use yum/dnf with the same package names
cscli version; systemctl status crowdsec
```
The Security Engine only detects; it blocks nothing until a remediation component (bouncer) is installed.

## Collections (parsers + scenarios)
```bash
cscli collections list
cscli collections install crowdsecurity/nginx crowdsecurity/http-cve crowdsecurity/sshd
cscli hub update && cscli hub upgrade      # keep scenarios current
```
Logs to watch are declared in `/etc/crowdsec/acquis.yaml` or `acquis.d/*.yaml`:
```yaml
source: file
filenames: [/var/log/nginx/access.log, /var/log/nginx/error.log]
labels: { type: nginx }
---
source: journalctl
journalctl_filter: ["_SYSTEMD_UNIT=ssh.service"]
labels: { type: syslog }
```

## See what it does
```bash
cscli metrics                     # lines read/parsed per source; unparsed lines = wrong type label
cscli alerts list
cscli decisions list              # active bans
cscli decisions add --ip 198.51.100.7 --duration 24h --reason manual   # default duration 4h, default type ban
cscli decisions delete --ip 198.51.100.7
cscli explain --file /var/log/nginx/access.log --type nginx   # debug parsing (also --log "<line>" and --dsn)
```

## Bouncers
```bash
cscli bouncers list               # registered remediation components
nft list set ip crowdsec crowdsec-blacklists | head     # IPv4 set; IPv6 uses table ip6 crowdsec6, set crowdsec6-blacklists
```
The firewall bouncer supports iptables, nftables, ipset and pf. A decision is enforced only where a bouncer runs.

## Whitelists
```yaml
# /etc/crowdsec/parsers/s02-enrich/mywhitelist.yaml
name: me/whitelist
description: office and monitoring
whitelist:
  reason: trusted
  ip: [203.0.113.10]
  cidr: [10.0.0.0/8]
```
`systemctl reload crowdsec` after edits. The docs recommend centralized AllowLists (`cscli allowlists`, managed at the LAPI) for plain IP/CIDR rules; parser whitelists suit expression-based rules. Whitelisting only prevents new decisions: delete existing ones with `cscli decisions delete`. Whitelist monitoring and load balancer IPs first, or health checks get banned.

## Multi-server
Run one LAPI (local API) and register agents on other hosts: `cscli lapi register --url <lapi-url>` on the agent, `cscli machines validate <name>` on the LAPI. Bouncers on each host then share decisions.

## Verify
- [ ] `cscli metrics` shows parsed lines for every acquisition.
- [ ] A controlled test brute force against a test host produces an alert and a decision; the IP is dropped by nftables.

## Checked

Checked 2026-10-26 against crowdsecurity/crowdsec-docs main (last commit 2026-10-23): install page, cscli reference pages (decisions add/delete, explain, lapi register, machines validate, hub update/upgrade, collections install), data source pages (file, journald, introduction), whitelist pages, firewall bouncer page, and collection names in crowdsecurity/hub. Confirmed: installer URL, bouncer package names, cscli flags and defaults (decisions add duration 4h and type ban), acquisition syntax with --- separators and acquis.d, parser whitelist directory and reload, nftables set names. Corrected: the file acquisition needed source: file; the docs now recommend centralized AllowLists for IP/CIDR rules. Removed: the claims that the installer auto-detects services and that the firewall bouncer registers automatically, the list of other bouncers, and the default LAPI port.

Method: documentation only; no commands were run.
