---
id: computing-software.cybersecurity-defensive.zeek.systemd-zeek-conf-deployment
name: systemd-zeek-conf-deployment
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, systemd, zeek-conf, systemd-generator, zeek-target]
level: advanced
status: docs-checked
description: "Deploy Zeek with systemd: zeek.conf, linking zeek-systemd-generator, daemon-reload, zeek.target, config validation, multi-interface sections."
sources: ["https://docs.zeek.org/en/current/advanced/deployment/systemd.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# systemd zeek.conf deployment

The page marks this as added in 8.1. A generator reads `<PREFIX>/etc/zeek/zeek.conf` and creates unit files for manager, logger, proxy and worker processes. It targets appliance or container use and is an alternative to ZeekControl.

Install by linking the generator:

```
mkdir -p /etc/systemd/system-generators/
ln -s <PREFIX>/bin/zeek-systemd-generator /etc/systemd/system-generators/
```

Minimal section-less config:

```
interface = af_packet::eth1
workers = 2
manager = 1
loggers = 1
proxies = 1
```

Run `systemctl daemon-reload` to execute the generator; units appear in `/run/systemd/generator`. Reload gives no immediate failure feedback, so check `journalctl -f`, or validate beforehand:

```
<PREFIX>/bin/zeek-systemd-generator --config <PREFIX>/etc/zeek/zeek.conf /tmp/out
```

Start with `systemctl start zeek.target`; inspect with `systemctl status zeek.slice` or `systemd-cgtop zeek.slice`; logs via `journalctl --follow -u 'zeek*'`. Processes run as user and group zeek, configurable with the `user` and `group` keys. With AppArmor or SELinux, allow the generator executables.

Several interfaces need INI style, which the page marks as added in 9.0: non-interface options go in `[zeek]`, then one `[interface eth1]` section per interface, whose name feeds unit names, working directories and node names.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
