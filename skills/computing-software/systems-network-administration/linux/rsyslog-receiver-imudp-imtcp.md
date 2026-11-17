---
id: computing-software.systems-network-administration.linux.rsyslog-receiver-imudp-imtcp
name: rsyslog-receiver-imudp-imtcp
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rsyslog, rsyslog-receiver, imudp, imtcp, central-logging, log-collector, rulesets, allowed-sender, network-devices, syslog-server, sysadmin]
level: practitioner
status: docs-checked
description: "Turn rsyslog into a central log collector: imudp/imtcp listeners bound to rulesets, per-host files, keeping remote logs out of local files, firewall/SELinux and capacity settings."
sources:
  - https://www.rsyslog.com/doc/configuration/modules/imudp.html
  - https://www.rsyslog.com/doc/configuration/modules/imtcp.html
  - https://www.rsyslog.com/doc/concepts/multi_ruleset.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rsyslog as a receiver (imudp / imtcp)

**Goal:** accept syslog from servers and network gear, file it per host, and keep it
separate from the collector's own logs.

## 1. Listeners bound to a ruleset
```
# /etc/rsyslog.d/10-receiver.conf
module(load="imudp")
module(load="imtcp" MaxSessions="2000")

template(name="PerHost" type="string" string="/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log")

ruleset(name="remote") {
    action(type="omfile" dynaFile="PerHost" createDirs="on" dirCreateMode="0750" fileCreateMode="0640")
    stop
}

input(type="imudp" port="514" ruleset="remote")
input(type="imtcp" port="514" ruleset="remote")
```
Binding inputs to a ruleset is the clean way to keep remote messages out of `/var/log/messages`;
the default ruleset continues to handle local logs only.
TLS listener: `module(load="imtcp" StreamDriver.Name="gtls" StreamDriver.Mode="1" StreamDriver.AuthMode="x509/name" PermittedPeer=["sender1.corp.example"])` with `input(type="imtcp" port="6514" ...)` plus global CA/cert/key settings.

## 2. Restrict senders
From 8.2608.0 the modules have an `AllowedSender` array parameter (module or input level; do not mix it with legacy directives). On older versions use the legacy directives:
```
input(type="imudp" port="514" ruleset="remote" AllowedSender=["10.0.0.0/8"])
input(type="imtcp" port="514" ruleset="remote" AllowedSender=["10.0.0.0/8"])
# legacy: $AllowedSender UDP, 10.0.0.0/8  and  $AllowedSender TCP, 10.0.0.0/8
```
UDP source addresses can be spoofed, so also use the host firewall: open only the listener ports you configured (514/udp, 514/tcp, 6514/tcp for TLS), ideally limited to source networks.

## 3. Operations
- Rotation: a logrotate glob over the per-host files with a postrotate HUP (rsyslogd reopens files on HUP).
- If SELinux is enforcing, check that the listening ports and log directories carry labels rsyslogd may use.
- Capacity: UDP drops under bursts. The imudp `RcvBufSize` input parameter (default 0, i.e. system default) sets the socket receive buffer, which the kernel caps at its own maximum; or move senders to TCP.
- Use `impstats` (`module(load="impstats" interval="60")`) to see queue sizes and discarded messages.

## Gotchas
- Network devices often send a bare IP or a wrong hostname; use `%fromhost-ip%` in the path for them.
- Hostname spoofing is trivial with UDP; don't treat remote logs as authenticated without TLS + x509/name.
- `%PROGRAMNAME%` can contain `/` from badly-formed senders — sanitise with a property replacer or use a fixed filename.

## Verify
- [ ] `ss -lunp | grep 514` and `ss -ltnp | grep 514` show rsyslogd; a test message forwarded from a sender creates `/var/log/remote/<host>/...`.
- [ ] Remote messages do not appear in the collector's `/var/log/messages`; `impstats` shows no discarded messages.

## Checked
Checked 2026-10-25 against the rsyslog documentation source on GitHub (rsyslog/rsyslog doc/source, main, release 8.2610.0 of 2026-10-20) and the systemd man pages. Confirmed: imtcp `MaxSessions` (module default 200), `AllowedSender` (introduced 8.2608.0), `StreamDriver.Name`/`.Mode`/`.AuthMode`, `PermittedPeer` (array, not allowed in anonymous modes), imudp `RcvBufSize`, `ruleset=` binding of inputs, `dynaFile`, `createDirs`, `dirCreateMode`/`fileCreateMode`, impstats `interval`, property `%fromhost-ip%`. Removed unconfirmed claims: SELinux port labels, firewalld service names, the `nstat` counter and `net.core.rmem_max` tuning.

Method: documentation only; no commands were run.
