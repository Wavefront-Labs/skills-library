---
id: computing-software.cloud-infrastructure-engineering.saltstack.jinja-filters-escaping-debugging
name: jinja-filters-escaping-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, jinja, filters, escaping, raw, debugging, profile, yaml-encode]
level: advanced
status: docs-checked
description: "Use Salt Jinja filters (yaml_encode, yaml_dquote, ipv4), escape literal braces with raw blocks, and debug with show_full_context, log.error and profile."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/jinja/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jinja filters, escaping and debugging

Custom filters:
- `yaml_encode`: serialize a single scalar (ints, floats, timestamps, booleans, strings, unicode) with special characters escaped. It does not work for sequences or maps.
- `yaml_dquote`: serialize a string as a properly escaped double-quoted YAML string; if the value may not be a string, use `yaml_encode`.
- `ipv4` (2017.7.0): from a list, keep only valid IPv4 entries; `['192.168.0.1', 'foo', 'bar', 'fe80::'] | ipv4` returns `["192.168.0.1"]`.

Escaping:
- One string: `{{ '{{' }}`.
- A block (for example consul-template syntax): `{% raw %}...{% endraw %}`.

Debugging:
- `show_full_context()` outputs all variables in the current Jinja context, for example `{{ show_full_context()|yaml(False) }}`.
- `{%- do salt['log.error']('message') -%}` writes to the minion log (2017.7.0).
- `{% profile as '<name>' %}...{% endprofile %}` (3002) logs the render time of a block at the `profile` log level; view it with `salt-call --local -l profile state.apply <sls>`. `import_yaml`, `import_json` and `import_text` blocks log the same way.

## Checked

2026-11-09. Read the relevant sections of the Salt Understanding Jinja page (doc/topics/jinja/index.rst, master branch): Custom Filters (yaml_encode, yaml_dquote, ipv4), Escaping Jinja, Debugging, Logs, Profiling. Added version gates and the profile log level.

Method: documentation only; no commands were run.
