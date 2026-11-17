---
id: computing-software.cybersecurity-defensive.system-hardening.network-device-logging
name: network-device-logging
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [network-device-logging, syslog, aaa-accounting, cisco-ios, junos, network-device-hardening]
level: practitioner
status: docs-checked
description: "Configure security logging on routers, switches and firewalls: syslog targets and levels, timestamps, AAA command accounting, config change logs, and SIEM use cases."
sources: ["https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html", "https://www.juniper.net/documentation/us/en/software/junos/network-mgmt/topics/topic-map/system-logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network device logging

Network devices are high-value targets and rarely have EDR. Their logs are often the only evidence of
unauthorised access or configuration change.

## What to capture
- Authentication: successful and failed logins (console, SSH, web), with source.
- Commands entered (AAA command accounting to TACACS+, plus local archive logging).
- Configuration changes and who made them.
- Interface/protocol state changes (routing adjacency flaps can indicate attacks or misconfiguration).
- ACL denies on management and control plane filters (rate limited).
- System events: reboots, image changes, crashes, high CPU.

## Cisco IOS / IOS XE
```
service timestamps log datetime msec localtime show-timezone
logging buffered <size> 6
logging trap 6
logging source-interface Loopback 0
logging host <SYSLOG_IP>
archive
 log config
  logging enable
  logging size 200
  hidekeys
  notify syslog
aaa accounting commands 15 default start-stop group tacacs
aaa accounting exec default start-stop group tacacs
```
- Cisco advises sending logs to a remote syslog server for correlation. Syslog over UDP is unreliable and
  cleartext, so extend management-traffic protections (encryption or out-of-band access) to syslog.
- Configuration Change Notification and Logging (`archive` / `log config`) logs the user, the command entered and the
  time; `hidekeys` keeps password data out of the log and `notify syslog` emits a syslog message per change.
- AAA command accounting sends each command, its date and the username to the TACACS+ server (not supported with
  RADIUS).

## Junos
```
set system syslog host <SYSLOG_IP> authorization notice
set system syslog host <SYSLOG_IP> interactive-commands any
set system syslog host <SYSLOG_IP> change-log any
```
Junos facilities include `authorization` (authentication and authorization attempts), `change-log` (configuration
changes) and `interactive-commands` (commands issued at the CLI); severity `any` means all levels and `notice` is a
non-error condition that may warrant handling. The default timestamp is month, date, hour, minute, second; the
`time-format` statement under `[edit system syslog]` adds the year or milliseconds (see "Including the Year or
Millisecond in Timestamps" on the Junos page for the options).

## Firewalls
Log admin events and policy hits (at least denies and allow-logs on sensitive rules); forward to the SIEM; include
config audit logs. Take exact settings from the vendor's documentation.

## Time and transport
Cisco notes accurate, reliable time is required for syslog correlation and forensics, and recommends NTP with
authentication from a trusted source. Prefer a reliable transport for critical sources where the platform
supports one, and use two collectors for resilience.

## SIEM use cases
- Login from a source outside the management network.
- Config change outside change windows or by non-network staff.
- Many failed logins (brute force) or successful login after failures.
- New local user created, AAA server unreachable (fallback to local), logging disabled.
- Device stopped sending logs (heartbeat/silence detection).

## Verify
SIEM shows logs from every device in inventory in the last 24 hours; a test config change appears with username
and command; device clocks are in agreement with the NTP source.

## Checked
2026-10-31. Confirmed in Cisco's hardening guide (remote syslog advice, UDP/cleartext note, `logging buffered`,
`logging trap`, `logging source-interface`, `service timestamps`, Configuration Change Notification and Logging
commands, command accounting, NTP importance) and the Junos system logging page (facilities `authorization`,
`change-log`, `interactive-commands`, `any` severity, `time-format`, default timestamp). Removed as unconfirmed:
`logging host ... transport tcp port 6514`, `login on-failure/on-success log`, `%PARSER-5-CFGLOG_LOGGEDCMD`,
Junos `UI_COMMIT`/`UI_CMDLINE_READ_LINE`, `source-address`, the `time-format year millisecond` argument syntax, the "under one second" skew target, and CIS Controls /
CISA guide references (not read).
Method: documentation only; no commands were run.
