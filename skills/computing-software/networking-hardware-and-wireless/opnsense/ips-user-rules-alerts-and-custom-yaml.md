---
id: computing-software.networking-hardware-and-wireless.opnsense.ips-user-rules-alerts-and-custom-yaml
name: ips-user-rules-alerts-and-custom-yaml
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [suricata-yaml, user-defined-rules, ids-alerts, bypass]
level: advanced
status: docs-checked
description: "Extend OPNsense IDS/IPS: user-defined rules, SSL fingerprint blocking, bypass toggle, alert tab and custom.yaml template overrides."
sources: ["https://docs.opnsense.org/manual/ips.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IDS/IPS user rules, alerts and custom configuration

Most rules come from third-party vendors such as Proofpoint, but the User defined tab lets you write limited rules of your own. Two uses are called out. Fingerprinting: you can block protected sites based on their SSL fingerprint by adding rules manually in the User defined tab (see the SSL fingerprint how-to). Bypass: the Bypass toggle skips inspection for matching traffic, for example to exclude local traffic and improve routing performance (the IPS bypass how-to has an example).

The Alerts tab shows triggered alerts; the info button gathers details about the detected event or threat. Remember that alerts captured behind NAT may show the firewall instead of the real client.

Advanced Suricata configuration uses suricata.yaml syntax. Create a template file named custom.yaml in /usr/local/opnsense/service/templates/OPNsense/IDS/. That file is processed by OPNsense's template system, so Jinja2 template tags can be used.

For log shipping, enable eve syslog output and create a logging target in System > Settings > Logging / Targets filtered on application suricata and level info; this does not change the product's own alert logging.

## Checked

2026-11-03. Confirmed against the OPNsense Intrusion Prevention System manual page: User defined tab, fingerprinting, bypass, Alerts tab, custom.yaml path and Jinja2, EVE syslog tip. Removed: the claim that custom.yaml is the supported place for non-GUI options.

Method: documentation only; no commands were run.
