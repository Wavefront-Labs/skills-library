---
id: computing-software.systems-network-administration.virtualisation.proxmox-firewall-logging-and-log-levels
name: proxmox-firewall-logging-and-log-levels
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-firewall-log, firewall-logging, proxmox, firewall]
level: practitioner
status: docs-checked
description: "Configure Proxmox VE firewall logging: per-rule log levels, default policy logging for host and guests, rate limiting, and where to read the logs."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
  - https://pve.proxmox.com/pve-docs/pve-firewall.8.html
  - https://github.com/proxmox/pve-docs/blob/master/generated/pve-firewall-cluster-opts.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall logging and log levels

**Goal:** see what the firewall drops or accepts without flooding the logs.

## Levels
`nolog`, `emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info`, `debug`. The level does not change how much is logged: it sets a `LOGID` prefix on the log line (`nolog` is `--`, `emerg` 0 up to `debug` 7) for filtering. By default all logging of firewall-filtered traffic is disabled.

## Default policy logging
- Host: Node -> Firewall -> *Options*: `log_level_in`, `log_level_out` and `log_level_forward` (standard rules; only some dropped or rejected packets are logged). Also `tcp_flags_log_level` and `smurf_log_level` for those filters.
- Guest: VM/CT -> Firewall -> *Options*: `log_level_in`, `log_level_out`.
- In files: `/etc/pve/nodes/<node>/host.fw` or `/etc/pve/firewall/<vmid>.fw` under `[OPTIONS]`:
```
[OPTIONS]
log_level_in: info
log_level_out: nolog
```

## Per-rule logging
GUI rule *Log level* field, or in the rule line: `IN ACCEPT -p tcp -dport 22 -source +management -log info`. Per-rule levels are independent of the *Options* levels.

## Rate limiting
Datacenter firewall options (`/etc/pve/firewall/cluster.fw`):
```
[OPTIONS]
log_ratelimit: enable=1,rate=1/second,burst=5
```
The option takes `[enable=]<1|0>[,burst=<integer>][,rate=<rate>]`.

## Reading logs
- GUI: Node or guest -> Firewall -> **Log**.
- Entry format: `VMID LOGID CHAIN TIMESTAMP POLICY: PACKET_DETAILS`; `VMID` is 0 for the host firewall.
- The `pvefw-logger` daemon (an NFLOG reader, ulogd replacement) produces the log.

## Gotchas
- Logging every packet that hits a busy default-drop policy produces a lot of output; keep `log_ratelimit` enabled (it defaults to enabled, burst 5) and enable logging only while troubleshooting.
- Some traffic is dropped but never logged even with logging on (for example TCP packets with invalid connection state, and NetBIOS/SMB and UPnP probe ports such as 135, 137-139, 445, 1900).

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, last pushed 2026-10-17). Confirmed: log level names and LOGID mapping; that the level only changes the LOGID prefix; host options `log_level_in/out/forward`, `tcp_flags_log_level`, `smurf_log_level`; `log_ratelimit` grammar and burst default 5; log line format and VMID 0 for host; never-logged traffic list; per-rule `-log <level>`. Removed: the log file path and `tail -f` advice (path not in the documentation), the claim that `info` is a volume setting, and the nftables logging remark.

Method: documentation only; no commands were run.
