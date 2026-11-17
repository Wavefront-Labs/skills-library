---
id: computing-software.cloud-infrastructure-engineering.saltstack.jinja-sls-templating
name: jinja-sls-templating
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, jinja, templating, sls, macros, import-yaml, filter-by]
level: practitioner
status: docs-checked
description: "Template Salt SLS files with Jinja: loops and conditionals, grains.filter_by, import and macros, salt[] calls, import_yaml, and render-before-YAML ordering."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/jinja/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jinja in SLS files

Jinja is the default templating language and renders before YAML parsing, so it runs before any state executes.

Loop to generate states:

```jinja
{% for motdfile in motd %}
{{ motdfile }}:
  file.managed:
    - source: salt://motd
{% endfor %}
```

- Wrap state elements in `{% if %}` blocks for conditionals.
- `grains.filter_by` picks per-OS values (for example the audit package on RedHat vs Debian).
- Import a macro or variable: `{% from 'lib.sls' import test %}`; add `with context` if the file needs grains. Includes must use full paths.
- Macros: `{% macro %}`; use whitespace control (`{%-`, `-%}`) so they return clean strings.
- Call execution modules as `salt['cmd.run']('whoami')`, preferred over `salt.cmd.run('whoami')`.
- Load data: `{%- import_yaml 'data.sls' as imported %}` then `imported['data']`.

Shared macros and variables should not start with an underscore and should be defined with `macro`, `set`, `load_yaml`, `load_json`, `import_yaml` or `import_json`.

## Checked

2026-11-09. Read the relevant sections of the Salt Understanding Jinja page (doc/topics/jinja/index.rst, master branch): Jinja in States, Include and Import, Macros, Calling Salt Functions, import_yaml profiling example. Removed the claim about template text in YAML comments (the page does not state it).

Method: documentation only; no commands were run.
