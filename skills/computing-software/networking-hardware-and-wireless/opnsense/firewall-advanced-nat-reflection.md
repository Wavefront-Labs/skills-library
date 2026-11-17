---
id: computing-software.networking-hardware-and-wireless.opnsense.firewall-advanced-nat-reflection
name: firewall-advanced-nat-reflection
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [nat-reflection, hairpin-nat, firewall-advanced-settings, rdr]
level: practitioner
status: docs-checked
description: "OPNsense advanced firewall NAT reflection options: port-forward, 1:1 and automatic outbound reflection, rule generation and the source-IP downside."
sources: ["https://docs.opnsense.org/manual/firewall_settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NAT reflection settings

Under Firewall > Settings > Advanced the Network Address Translation block holds legacy auto-reflection switches. The docs advise against using them: automatic rules carry assumptions that may not fit your case, and explicit manual NAT rules make intent clear. A separate NAT Reflection how-to covers the manual approach.

Vocabulary: rdr is redirection (Destination NAT, Firewall > NAT > Destination NAT (Port Forward)), which changes the destination IP; nat is Source NAT (Outbound), which changes the source IP. Reflection NAT is just rdr; Hairpin NAT combines rdr and nat.

Options, all disabled by default:
- Reflection for Destination NAT (Port Forwards): generates rdr rules reflecting port forwards onto internal interfaces (those without a gateway). A forward on wan produces rules for lan, opt1, lo0 and the like.
- Reflection for 1:1: the same for 1:1 NAT entries.
- Automatic Source NAT (Outbound) for Reflection: adds nat rules alongside rdr, turning all reflection into hairpin NAT.

Firewall rules are not generated for reflection, so create them manually or the default deny blocks the traffic. Inspect automatic rules with pfctl -s nat or in Firewall > Diagnostics > Statistics > rules.

Downside of hairpin: the receiving server sees the firewall's internal address rather than the client, so tools like fail2ban cannot work properly.

## Checked

2026-11-03. Confirmed against the OPNsense Firewall Settings (Advanced) manual page, section Network Address Translation: the warning, rdr and nat vocabulary, the three reflection options and defaults, pfctl -s nat, the hairpin downside. Nothing removed.

Method: documentation only; no commands were run.
