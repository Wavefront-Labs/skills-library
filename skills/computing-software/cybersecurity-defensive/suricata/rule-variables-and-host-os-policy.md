---
id: computing-software.cybersecurity-defensive.suricata.rule-variables-and-host-os-policy
name: rule-variables-and-host-os-policy
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [address-groups, port-groups, home-net, host-os-policy]
level: practitioner
status: docs-checked
description: "Define HOME_NET, EXTERNAL_NET and port groups under vars, and map host-os-policy so fragment and stream handling follows target OS behaviour."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html", "https://docs.suricata.io/en/latest/rules/intro.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rule variables and host-os-policy

Under `vars`:
- `address-groups`: for example `HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"` and `EXTERNAL_NET: any`.
- `port-groups`: for example `HTTP_PORTS: "80"` and `SSH_PORTS: 22`.

Warning from the rules docs: `HOME_NET: any` combined with `EXTERNAL_NET: !$HOME_NET` makes `$EXTERNAL_NET` evaluate to an invalid value.

## host-os-policy

Maps OS names (windows, linux, bsd, solaris, macos and others) to IP lists, which controls how fragments and stream overlaps are handled for those hosts, for example `linux: [10.0.0.0/8, 192.168.1.100]`.

## Checked

2026-11-04. Confirmed against the suricata.yaml configuration page (address-groups, port-groups, host-os-policy sections) and the Rules Introduction page (HOME_NET/EXTERNAL_NET warning).

Removed: an uppercase-naming convention and an `any`-when-unset claim that the pages do not state.

Method: documentation only; no commands were run.
