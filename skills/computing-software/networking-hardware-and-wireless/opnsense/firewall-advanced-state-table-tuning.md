---
id: computing-software.networking-hardware-and-wireless.opnsense.firewall-advanced-state-table-tuning
name: firewall-advanced-state-table-tuning
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [state-table, firewall-optimization, adaptive-timeouts, syncookies, max-states]
level: advanced
status: docs-checked
description: "Tune the OPNsense pf state table: optimization modes, adaptive timeouts, max states, fragments, table entries, bogon refresh and syncookies."
sources: ["https://docs.opnsense.org/manual/firewall_settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# State table and limits

Miscellaneous settings under Firewall > Settings > Advanced:

- Firewall Optimization: normal (default); high-latency for slow links such as satellite, expiring idle connections later; aggressive, which expires idle connections sooner, saving CPU and memory but possibly dropping legitimate idle ones; conservative, which avoids dropping idle connections at the cost of memory and CPU.
- Bind states to interface: states float by default and match regardless of interface, best for most setups.
- Firewall Adaptive Timeouts: start is the state count where timeouts begin scaling linearly by (end - states) / (end - start); end is where all timeouts reach zero and states are purged, so set a lower state limit and do not reach it.
- Firewall Maximum States: size of the state table; raise it for many connections (default shown in the help text).
- Firewall Maximum Fragments: entries in the fragment reassembly pool.
- Firewall Maximum Table Entries: combined cap for aliases, sshlockout, bogons and similar tables. Large aliases such as GeoIP may require raising it.
- Disable Firewall: turns off all firewall and NAT features.
- Aliases Resolve Interval: seconds between hostname re-resolution for aliases; Check certificate of aliases URLs refuses invalid or revoked HTTPS sources.
- Bogon Networks Update Frequency: how often reserved or unassigned IANA ranges refresh.
- Logging: tunes logging of default block/pass, automatic source NAT, bogon and private blocks; if disabled only your manual rules' log directives appear in the firewall log.

Anti DDoS: Enable syncookies prevents memory allocation before a proper handshake, protecting pf from state exhaustion. Modes: never (default), always, or adaptive with lower and upper percentages of state table usage.

## Checked

2026-11-03. Confirmed against the OPNsense Firewall Settings (Advanced) manual page, sections Miscellaneous, Logging, Bogon Networks and Anti DDOS: optimization modes, adaptive timeout formula, maximum states, fragments and table entries, alias options, syncookie modes. Nothing removed.

Method: documentation only; no commands were run.
