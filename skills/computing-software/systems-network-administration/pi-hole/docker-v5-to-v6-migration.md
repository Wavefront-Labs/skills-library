---
id: computing-software.systems-network-administration.pi-hole.docker-v5-to-v6-migration
name: docker-v5-to-v6-migration
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [docker-v6-migration, env-var-mapping, revservers-format]
level: advanced
status: docs-checked
description: "Translate Pi-hole v5 Docker environment variables to their FTLCONF_ v6 equivalents, including reverse servers and dnsmasq files."
sources: ["https://docs.pi-hole.net/docker/upgrading/v5-v6/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker v5 to v6 variable migration

The last image with v5 components was `2024.07.0`; later images use v6. Nearly all old variables are removed and replaced by `FTLCONF_` equivalents.

| Old | New |
| --- | --- |
| `CUSTOM_CACHE_SIZE` | `FTLCONF_dns_cache_size` |
| `DNSSEC` | `FTLCONF_dns_dnssec` |
| `DNSMASQ_LISTENING` | `FTLCONF_dns_listeningMode` |
| `INTERFACE` | `FTLCONF_dns_interface` |
| `PIHOLE_DNS_` | `FTLCONF_dns_upstreams` |
| `QUERY_LOGGING` | `FTLCONF_dns_queryLogging` |
| `WEBPASSWORD` | `FTLCONF_webserver_api_password` |
| `WEB_PORT` | `FTLCONF_webserver_port` |
| `DHCP_ACTIVE` | `FTLCONF_dhcp_active` |
| `DHCP_LEASETIME` | `FTLCONF_dhcp_leaseTime` |
| `PIHOLE_DOMAIN` | `FTLCONF_dns_domain` |

**Reverse servers.** The `REV_SERVER*` variables become one `FTLCONF_dns_revServers`, in the form `<enabled>,<ip-address>[/<prefix-len>],<server>[#<port>],<domain>`:

```text
FTLCONF_dns_revServers: 'true,192.168.0.0/24,192.168.0.1#53,lan'
```

**dnsmasq files.** v6 no longer reads `/etc/dnsmasq.d/` by default. Mount the folder into the container and set `FTLCONF_misc_etc_dnsmasq_d: 'true'`. For a few lines use `FTLCONF_misc_dnsmasq_lines`, separated by `;`.

**Removed without replacement** include `CONDITIONAL_FORWARDING`, `DNS1`, `DNS2`, `IPV6`, `ServerIP`, `VIRTUAL_HOST` and `WEBLOGS_STDOUT`.

**Checklist**

1. Map every old variable.
2. Delete the variables the page lists as removed.

## Checked

2026-11-03. Read the Docker Upgrading from v5.x page: the 2024.07.0 note, every row of the table above, the `FTLCONF_dns_revServers` format and example, the dnsmasq.d mount and `FTLCONF_misc_etc_dnsmasq_d`, `FTLCONF_misc_dnsmasq_lines`, and the removed variables list. Removed the advice to keep the dnsmasq.d mount (not in the page).

Method: documentation only; no commands were run.
