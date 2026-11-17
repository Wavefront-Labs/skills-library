---
id: computing-software.systems-network-administration.cisco-networking.jinja2-network-config-templates
name: jinja2-network-config-templates
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, jinja2, jinja2-templates, config-templating, python, ansible, network-automation, source-of-truth, netbox]
level: practitioner
status: draft
description: "Render device configs from Jinja2 templates and structured data: template layout, loops/conditionals/filters, whitespace control, and testing output before deployment."
sources:
  - https://jinja.palletsprojects.com/en/stable/templates/
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jinja2 configuration templates

## Data + template
```yaml
# host_vars/sw1.yml
hostname: sw1
vlans:
  - {id: 10, name: DATA}
  - {id: 100, name: VOICE}
access_ports:
  - {name: GigabitEthernet1/0/1, vlan: 10, voice: 100, desc: desk-101}
ntp_servers: [10.0.0.11, 10.0.0.12]
```
```jinja
{# templates/access-switch.j2 #}
hostname {{ hostname }}
{% for v in vlans %}
vlan {{ v.id }}
 name {{ v.name | upper }}
{% endfor %}
{% for p in access_ports %}
interface {{ p.name }}
 description {{ p.desc | default('user port') }}
 switchport mode access
 switchport access vlan {{ p.vlan }}
{% if p.voice is defined %}
 switchport voice vlan {{ p.voice }}
{% endif %}
 spanning-tree portfast
{% endfor %}
{% for s in ntp_servers %}
ntp server {{ s }}
{% endfor %}
```

## Render
```python
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml
env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True,
                  lstrip_blocks=True, undefined=StrictUndefined)
data = yaml.safe_load(open("host_vars/sw1.yml"))
print(env.get_template("access-switch.j2").render(**data))
```
Ansible: `ansible.builtin.template` or `cisco.ios.ios_config: src=access-switch.j2`.

## Practices
- `trim_blocks`/`lstrip_blocks` (or `{%- -%}`) to avoid blank lines that break diffs.
- `StrictUndefined` so a missing variable fails rendering instead of producing `vlan ` lines.
- Split templates by function (`{% include 'ntp.j2' %}`) and use macros for repeated blocks.
- Keep logic in data (source of truth: NetBox, YAML in Git), not in templates.
- Render to files and diff against running config (or `ios_config` check mode) before pushing.

## Testing
- Unit test: render with fixture data and compare to a golden file (pytest).
- Lint generated configs with Batfish for references (undefined ACLs, unused VLANs).

## Verify
- [ ] Rendering all devices in CI produces no errors; diffs reviewed in pull requests.
