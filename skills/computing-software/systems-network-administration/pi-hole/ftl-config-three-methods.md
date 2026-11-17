---
id: computing-software.systems-network-administration.pi-hole.ftl-config-three-methods
name: ftl-config-three-methods
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-toml, pihole-ftl-config, read-only-config]
level: practitioner
status: docs-checked
description: "Change Pi-hole v6 settings through pihole.toml, the pihole-FTL --config command or FTLCONF_ variables, and know which wins."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pi-hole v6 configuration methods

Pi-hole FTL keeps its settings in the TOML file `/etc/pihole/pihole.toml`. You can edit it directly or use:

- the web interface or the API
- the command line: `sudo pihole-FTL --config dns.dnssec true`
- environment variables named `FTLCONF_<section>_<key>`, such as `FTLCONF_dns_upstreams`

The web interface, API and CLI are preferred over hand editing because they do error checking, which tries to prevent incompatible options that stop FTL from starting on a badly broken configuration.

**Precedence and read-only.** Every setting can be overridden by an environment variable. A setting defined this way becomes read-only: the TOML file, CLI and web interface cannot change it until the variable is removed.

**Whole-config lock.** `misc.readOnly` (default `false`) puts the entire configuration into read-only mode, blocking changes through the API or CLI. It suits infrastructure-as-code tools that must force the configuration.

**Settings the API cannot change.** Options that decide which files the server delivers or which programs run, such as `webserver.advancedOpts`, `webserver.paths.webroot`, `webserver.paths.webhome`, `webserver.paths.prefix` and `misc.dnsmasq_lines`, cannot be set through the API. Use `pihole.toml`, an environment variable or `pihole-FTL --config`, all of which need host access.

**Checklist**

1. Prefer the CLI or web interface over editing TOML.
2. Use `FTLCONF_` only when you want the value pinned.
3. Remember the section name is part of the variable.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile). Nothing needed removing.
Method: documentation only; no commands were run.
