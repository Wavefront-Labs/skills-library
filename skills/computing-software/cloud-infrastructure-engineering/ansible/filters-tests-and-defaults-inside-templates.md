---
id: computing-software.cloud-infrastructure-engineering.ansible.filters-tests-and-defaults-inside-templates
name: filters-tests-and-defaults-inside-templates
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, jinja2-templates, template-filters, template-defaults, filters, default-filter]
level: practitioner
status: docs-checked
description: "Use filters, tests and defaults inside .j2 templates: default and omit-like patterns, mandatory, join and to_nice_yaml blocks, is defined tests and safe nested lookups."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_filters.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_templating.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/filter/to_nice_yaml.yml", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/filter/mandatory.yml", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/porting_guides/porting_guide_core_2.19.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filters, tests and defaults inside templates

Templates get the standard Jinja2 filters and tests, the Ansible-specific ones, and the host's variables.

## Defaults
```jinja
listen {{ nginx_port | default(80) }};
worker_processes {{ nginx_workers | default(ansible_facts['processor_vcpus']) }};
server_name {{ server_names | default([inventory_hostname]) | join(' ') }};
{% if tls_cert is defined and tls_cert | length > 0 %}
ssl_certificate {{ tls_cert }};
{% endif %}
```
- `default(x)` replaces an undefined value; `default(x, true)` also replaces values that evaluate to false or an empty string.
- `mandatory` fails with a clear message: `{{ db_password | mandatory('db_password must be set') }}`.
- `default(omit)` is for task and module arguments (omit the option when undefined). In a template body, wrap an optional line in `{% if var is defined %}`.

## Safe nested access
Since ansible-core 2.8, reading an attribute of an undefined value returns another undefined value, so a default at the end of a chain covers a missing link anywhere in it:
```jinja
{{ app_config.database.host | default('localhost') }}
```

## Structured blocks
```jinja
# config.yml
{{ app_settings | to_nice_yaml(indent=2, sort_keys=true) }}

"servers": {{ groups['web'] | map('extract', hostvars, 'ansible_host') | list | to_json }}
```
`to_nice_yaml` options include `indent` and `sort_keys` (default true).

## Formatting
```jinja
{{ "%-20s %s" | format(key, value) }}
{{ memory_mb | int // 2 }}m
{{ user_list | sort(attribute='name') | map(attribute='name') | join(',') }}
{{ comment_text | comment }}             {# comments the text out; default style is plain #}
{{ 'enabled' if feature_x | bool else 'disabled' }}
```

## Tests
`is defined`, `is none`, `is mapping`, `is string`, `is match('^10\.')`, `is version('2.0', '>=')`. Tests run on the control node.

## Gotchas
- An undefined-variable error points at the template line; render a small copy with a debug task to iterate quickly.
- `map` and `select` return generators: end the chain with `| list` when you need a list.
- Since ansible-core 2.19 filters that expect strings convert other values to strings without complaint (for example `replace` on a list); apply them per element with `map('replace', ...)`.

## Verify
```bash
ansible host -m ansible.builtin.template -a 'src=app.conf.j2 dest=/tmp/app.conf' --check --diff
```

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the Using filters page (`default`, `default(omit)`, `default(x, true)`, `mandatory`, chained undefined since 2.8, `extract`) and in the `to_nice_yaml`, `comment`, `mandatory` and `extract` filter documentation; the string-conversion behaviour in the 2.19 porting guide. Removed the `.get()` access examples and the claim about non-dict parents, which the documentation does not cover.
Method: documentation only; no commands were run.
