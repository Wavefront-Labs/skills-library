---
id: computing-software.cloud-infrastructure-engineering.ansible.jinja-control-structures-raw-blocks-and-comments-in-templates
name: jinja-control-structures-raw-blocks-and-comments-in-templates
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, jinja2-templates, template-for-loop, template-if, raw-block, jinja-comments, whitespace-control]
level: practitioner
status: docs-checked
description: "Write for loops and if blocks in .j2 templates with clean whitespace, emit literal {{ }} with raw blocks, and use Jinja comments and ansible_managed headers."
sources: ["https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/modules/template.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/doc_fragments/template_common.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_templating.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/filter/comment.yml", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/porting_guides/porting_guide_core_2.19.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control structures, raw blocks and comments in templates

## for and if
```jinja
{{ ansible_managed | comment }}
{# This comment never reaches the target file #}
upstream {{ app_name }} {
{% for host in groups['app'] | sort %}
    server {{ hostvars[host].ansible_host }}:{{ app_port }}{% if hostvars[host].backup | default(false) %} backup{% endif %};
{% else %}
    server 127.0.0.1:{{ app_port }};   # rendered when the group is empty
{% endfor %}
}
{% if tls_enabled | bool %}
listen 443 ssl;
{% elif http2 | default(false) %}
listen 80 http2;
{% else %}
listen 80;
{% endif %}
```
Loop helpers: `loop.index`, `loop.index0`, `loop.first`, `loop.last`, `loop.length`:
```jinja
servers = [{% for h in nodes %}"{{ h }}"{% if not loop.last %}, {% endif %}{% endfor %}]
```
Better for lists: `{{ nodes | to_json }}` or `{{ nodes | join(', ') }}`.

## Whitespace
The template module defaults are `trim_blocks: true` (the first newline after a block tag is removed) and
`lstrip_blocks: false` (set it to true to strip leading spaces and tabs before a block tag). Either set the
option on the task, or put a header as the **first line** of the template:
```jinja
#jinja2: lstrip_blocks: True
```
Manual control: `{%-` and `-%}` strip whitespace on that side.

## Literal braces: raw
Templates for Go templates, Helm, Prometheus alert rules or other Jinja files:
```jinja
{% raw %}
summary: "Instance {{ $labels.instance }} down"
{% endraw %}
```
Alternatively change the delimiters per task (`variable_start_string: '[['` and `variable_end_string: ']]'` on the template task) or with the `#jinja2:` header, for example `#jinja2:variable_start_string:'[%', variable_end_string:'%]'`. The module documentation calls the header the best way to prevent evaluation of text that looks like Jinja2 but is not.

## Comments
`{# ... #}` is a Jinja comment and is stripped from the output. The template module also has `comment_start_string` and `comment_end_string` options (added in 2.12). Comments in the target language (`#`, `//`) are output as-is.
`{{ ansible_managed | comment }}` renders the managed banner in a comment style (`comment('c')`, `comment('xml')`; styles are `plain`, `decoration`, `erlang`, `c`, `cblock`, `xml`).

## Gotchas
- `{% for %}` over a dict iterates keys; use `{% for k, v in d.items() %}` or `d | dict2items`.
- A variable set inside a loop (`{% set x = ... %}`) does not survive the loop; use `namespace()`: `{% set ns = namespace(total=0) %}{% set ns.total = ns.total + 1 %}`.
- Output order must be stable: the documentation says inventory order is "reproducible ... not normally predictable", so `| sort` group and dict iteration to avoid a change on every run.
- Keep `ansible_managed` static (its default is the plain string `Ansible managed`): the template module notes that a date in the template marks it changed on every run.
- Since ansible-core 2.19 a template that evaluates to `None` can return `None` rather than an empty string; end an `{% if %}` with `{% else %}{{ "" }}{% endif %}` where a string is required.

## Verify
- [ ] Render a template to a scratch path with `--check --diff` and compare with what you expect.
- [ ] A second run reports no change.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed against the `template_common` doc fragment (`trim_blocks` default yes, `lstrip_blocks` default no, comment strings added 2.12, `#jinja2:` header note, date-in-template note), `comment` filter styles, `DEFAULT_MANAGED_STR` in `config/base.yml`, the inventory-order wording in the Controlling playbook execution page, and the 2.19 porting guide (None results).
Method: documentation only; no commands were run.
