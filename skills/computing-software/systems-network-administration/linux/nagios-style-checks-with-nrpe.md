---
id: computing-software.systems-network-administration.linux.nagios-style-checks-with-nrpe
name: nagios-style-checks-with-nrpe
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nrpe, nagios-plugins, icinga, check-disk, monitoring-plugins, check-by-ssh]
level: practitioner
status: draft
description: "Run Nagios-compatible checks on Linux hosts with NRPE and monitoring-plugins: nrpe.cfg commands, allowed_hosts, TLS, plugin exit codes and perfdata, and writing custom checks."
sources:
  - https://github.com/NagiosEnterprises/nrpe/blob/master/README.md
  - https://www.monitoring-plugins.org/doc/guidelines.html
  - https://icinga.com/docs/icinga-2/latest/doc/07-agent-based-monitoring/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Nagios-style checks with NRPE

NRPE runs plugins locally on the monitored host when the Nagios/Icinga/Naemon server asks (`check_nrpe -H host -c check_disk`). Icinga 2 and Checkmk have their own agents but still run the same plugins.

## Install
```bash
dnf install nrpe nagios-plugins-{disk,load,procs,swap,users}   # EPEL
apt install nagios-nrpe-server monitoring-plugins
systemctl enable --now nrpe            # nagios-nrpe-server on Debian; TCP 5666
```

## nrpe.cfg
```
allowed_hosts=127.0.0.1,10.0.0.5        # monitoring server(s) only
dont_blame_nrpe=0                       # never allow arguments from the network unless needed
command_timeout=60
include_dir=/etc/nrpe.d/
```
```
# /etc/nrpe.d/checks.cfg
command[check_root]=/usr/lib64/nagios/plugins/check_disk -w 20% -c 10% -p /
command[check_var]=/usr/lib64/nagios/plugins/check_disk -w 15% -c 5% -p /var
command[check_load]=/usr/lib64/nagios/plugins/check_load -r -w 2,1.5,1.2 -c 4,3,2
command[check_sshd]=/usr/lib64/nagios/plugins/check_procs -c 1: -C sshd
command[check_swap]=/usr/lib64/nagios/plugins/check_swap -w 30% -c 10%
command[check_updates]=sudo /usr/lib64/nagios/plugins/check_updates   # sudoers entry for nrpe user, NOPASSWD, exact path
```
Plugin path is `/usr/lib/nagios/plugins` on Debian. Restart nrpe after changes.

Test from the server:
```bash
/usr/lib64/nagios/plugins/check_nrpe -H web1 -c check_root
# DISK OK - free space: / 12000 MB (61% inode=89%);| /=7600MB;15800;17800;0;19800
```
`CHECK_NRPE: Error - Could not complete SSL handshake` = the server isn't in `allowed_hosts`, or TLS/ADH mismatch between versions; NRPE 4 supports proper certificates (`ssl_cert_file`, `ssl_client_certs=2`).

## Plugin contract (for custom checks)
- Exit code: 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN.
- First line of stdout: `SERVICE STATUS - text | perfdata`, perfdata as `'label'=value[UOM];warn;crit;min;max`.
```bash
#!/bin/bash
# check_cert_days: warn/crit days before certificate expiry
days=$(( ( $(date -d "$(openssl x509 -enddate -noout -in "$1" | cut -d= -f2)" +%s) - $(date +%s) ) / 86400 ))
if   (( days < ${3:-7} ));  then echo "CRITICAL - $days days left | days=$days"; exit 2
elif (( days < ${2:-21} )); then echo "WARNING - $days days left | days=$days"; exit 1
else echo "OK - $days days left | days=$days"; exit 0; fi
```
Timeouts or missing permissions must yield UNKNOWN (3), not OK.

## Security
- NRPE with `dont_blame_nrpe=1` and argument passing was the source of past RCEs; keep it off.
- Alternatives: `check_by_ssh` (key-restricted command), or migrate to Prometheus exporters; keep plugins for legacy dashboards.

## Verify
- [ ] Every command in nrpe.d runs as the nrpe user locally (`sudo -u nrpe <cmd>`) and returns a sane exit code.
- [ ] Port 5666 is reachable only from monitoring servers.
