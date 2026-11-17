---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.panorama-templates-and-template-stacks
name: panorama-templates-and-template-stacks
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [template-stacks, panorama, templates, template-variables, network-settings, device-settings, template-stack-priority]
level: practitioner
status: draft
description: "Push network and device settings with Panorama templates and stacks, using variables for per-site values."
sources: ["https://docs.paloaltonetworks.com/panorama/11-1/panorama-admin/manage-firewalls/manage-templates-and-template-stacks"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: standard interfaces, zones, profiles, syslog and admin settings across sites with local differences handled by variables.

```
configure
set template T-BASE config shared log-settings syslog SYSLOG-SIEM server siem1 server 192.0.2.50 transport SSL port 6514
set template T-SITE variable $mgmt-ip type ip-netmask 192.0.2.10/24
set template-stack TS-BRANCH templates [ T-SITE T-BASE ]
set template-stack TS-BRANCH devices 001122334455
commit
commit-all template-stack TS-BRANCH
```
Stack order matters: settings in templates higher in the list override those lower. Put site-specific overrides above base.

Variables (`$name`) can be IP, subnet, interface, zone or other types; set a value per device in the template stack device overrides.

Gotchas
- Pushing a template with an interface config to a firewall that has the same interface configured locally overwrites it; check Panorama > Managed Devices for local overrides.
- Not all settings can live in a template (for example HA settings and some management settings may be device-local; confirm).
- Commit then push; "Force Template Values" overwrites local overrides.

## Verify
Panorama > Managed Devices shows template status `In Sync`. On the firewall:
```
show config pushed-template
```
