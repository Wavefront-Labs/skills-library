---
id: computing-software.systems-network-administration.cisco-networking.catalyst-center-template-editor
name: catalyst-center-template-editor
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-center, dnac, template-editor, day-n-templates, velocity, jinja2, composite-template, provisioning]
level: practitioner
status: draft
description: "Write and deploy Catalyst Center Template Editor day-N templates in Velocity or Jinja2: variables, binding, composite templates, simulation and safe provisioning."
sources:
  - https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/catalyst-center/2-3-7/user_guide/b_cisco_catalyst_center_user_guide_237/b_cisco_dna_center_ug_2_3_7_chapter_01000.html
  - https://developer.cisco.com/docs/dna-center/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Template Editor day-N templates

## Projects and templates
Tools > Template Hub (Template Editor in older releases): templates live in projects; each has a
language (**Velocity** or **Jinja2**), device type/software filters and is versioned on **commit**.
Only committed versions can be provisioned. Onboarding (day-0, PnP) templates and day-N templates
are separate types.

## Example (Jinja2)
```jinja
{# NTP and access-port hardening #}
{% for srv in ntp_servers.split(',') %}
ntp server {{ srv.strip() }}
{% endfor %}
{% for intf in __interface %}
{% if intf.portMode == 'access' %}
interface {{ intf.portName }}
 spanning-tree bpduguard enable
{% endif %}
{% endfor %}
```
Velocity equivalent uses `#foreach($srv in $ntp_servers.split(","))`, `$var`, `#if`.
Variables become a form at provisioning; set type, default, required, and **bind** variables to
Catalyst Center data (system variables like `__device`, `__interface`, site settings) so they fill
automatically.

## Composite templates
Chain several templates in order (base, security, QoS) and deploy as one; each part stays reusable.

## Deploying
1. Associate templates to the network profile (Design > Network Profiles) for sites/device types,
   or use Template Hub > Provision directly.
2. **Simulate** with a real device to see the rendered CLI before pushing.
3. Provision; view results per device (Provision > Work Items / Activities).
Interactive commands: wrap in `#INTERACTIVE ... <IQ>prompt<R>answer #ENDS_INTERACTIVE`.
Enable-mode commands: `#MODE_ENABLE ... #MODE_END_ENABLE`.

## Gotchas
- Templates push additively; removing lines requires explicit `no` commands.
- Conflicts with Catalyst Center intent (settings it manages, like AAA/NTP from Design) produce
  overwrite fights; choose one source for each setting.
- Commit message per change; roll back by provisioning the previous version.

## Verify
- [ ] Simulation output equals intended CLI; device config after provisioning matches (`show run | section ...`).
