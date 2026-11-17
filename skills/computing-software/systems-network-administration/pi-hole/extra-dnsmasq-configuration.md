---
id: computing-software.systems-network-administration.pi-hole.extra-dnsmasq-configuration
name: extra-dnsmasq-configuration
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [dnsmasq-lines, etc-dnsmasq-d, dnsmasq-conf-conflicts]
level: sme
status: docs-checked
description: "Inject extra dnsmasq options into Pi-hole v6 with misc.dnsmasq_lines or the dnsmasq.d directory, and avoid conflicts."
sources: ["https://docs.pi-hole.net/ftldns/configfile/", "https://docs.pi-hole.net/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Extra dnsmasq configuration

Pi-hole generates the dnsmasq configuration (`/etc/pihole/dnsmasq.conf`). You can add to it in two advanced ways.

**dnsmasq_lines.** `misc.dnsmasq_lines` injects extra lines into the generated config:

```toml
[misc]
  dnsmasq_lines = [ "address=/example.com/192.168.0.1", "address=/example.org/192.168.0.2" ]
```

Incorrectly formatted or duplicated lines, or lines that conflict with Pi-hole's automatic configuration, can break the embedded dnsmasq and stop DNS resolution. Directives like `dhcp-script` and `conf-script` name programs dnsmasq will execute, so this option cannot be set via the API. Use `pihole.toml`, an environment variable or `pihole-FTL --config`.

**etc_dnsmasq_d.** `misc.etc_dnsmasq_d` (default `false`) makes FTL load additional dnsmasq configuration from `/etc/dnsmasq.d/`. The same conflict warning applies: files specifying options that can be defined only once may clash with the automatic configuration.

**Docker.** Set `FTLCONF_misc_dnsmasq_lines` with lines separated by `;`, or mount a directory and set `FTLCONF_misc_etc_dnsmasq_d: 'true'`.

**Alternatives.** Prefer native options (`dns.hosts`, `dns.cnameRecords`, `dns.hostRecord`) where they exist.

**Checklist**

1. Check no native setting covers the need.
2. Add one line at a time.
3. Restart and check the logs for dnsmasq errors.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile); Docker (docker). Reworded the unconfirmed check step naming a log file.
Method: documentation only; no commands were run.
