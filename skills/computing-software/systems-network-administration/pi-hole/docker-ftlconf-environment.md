---
id: computing-software.systems-network-administration.pi-hole.docker-ftlconf-environment
name: docker-ftlconf-environment
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [ftlconf-variables, docker-env-config, single-source-of-truth]
level: practitioner
status: docs-checked
description: "Configure FTL in Docker with FTLCONF_ environment variables, including arrays, upstreams and the read-only side effect."
sources: ["https://docs.pi-hole.net/docker/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure FTL with FTLCONF_ variables

The recommended way to configure the container is environment variables named `FTLCONF_[section_][setting]`. This `pihole.toml` fragment

```toml
[dns]
  dnssec = true
```

becomes `FTLCONF_dns_dnssec: 'true'`.

**Arrays** are delimited with `;`, or written as a YAML block:

```yaml
environment:
  FTLCONF_dns_upstreams: '8.8.8.8;8.8.4.4;1.1.1.1'
  FTLCONF_misc_dnsmasq_lines: |-
    address=/example.com/192.168.1.1
    address=/example.org/192.168.1.2
  FTLCONF_webserver_port: '8082,443s'
```

`dns.upstreams` accepts non-standard ports (`127.0.0.1#5053`) and Docker service names such as `upstream0`.

**Read-only effect.** A setting defined through the environment becomes read-only: you cannot change it in the web interface or CLI. This keeps one source of truth. If you remove the variable, FTL reverts to the default for that setting.

**Other variables**

| Variable | Purpose |
| --- | --- |
| `TZ` | Timezone, so logs rotate at local midnight |
| `TAIL_FTL_LOG` | Default `1`; `0` stops FTL log output |
| `PIHOLE_UID`, `PIHOLE_GID` | Default `1000`; must not already be in use in the container |
| `FTL_CMD` | Default `no-daemon`; extra dnsmasq options |

**Checklist**

1. Translate each key from `pihole.toml` using the naming rule.
2. Use `;` or a YAML block for arrays.
3. Remember changed settings can no longer be edited elsewhere.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Docker Configuration (docker/configuration). Nothing needed removing.
Method: documentation only; no commands were run.
