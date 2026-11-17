---
id: computing-software.cloud-infrastructure-engineering.ansible.avoiding-jinja-delimiters-in-when
name: avoiding-jinja-delimiters-in-when
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, conditionals, when-jinja-delimiters, when, jinja2]
level: intro
status: docs-checked
description: "Write when, changed_when, failed_when and until as raw Jinja expressions without {{ }}, and fix the conditional templating warning and dynamic-key cases."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/porting_guides/porting_guide_core_2.19.html", "https://github.com/ansible/ansible-lint/blob/main/docs/rules/no-jinja-when.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# No {{ }} in when

`when` is a raw Jinja2 expression without double curly braces, and so are `changed_when`,
`failed_when`, `until` and `assert: that`: variables can be used directly. Wrapping them in `{{ }}` creates a nested
expression, which ansible-lint's `no-jinja-when` rule calls an anti-pattern.

```yaml
# wrong
when: "{{ ansible_facts['os_family'] == 'RedHat' }}"
when: "{{ app_port }} == 8080"
# right
when: ansible_facts['os_family'] == 'RedHat'
when: app_port == 8080
```
Since ansible-core 2.19 the config option `ALLOW_EMBEDDED_TEMPLATES` (env
`ANSIBLE_ALLOW_EMBEDDED_TEMPLATES`, ini `allow_embedded_templates`, default true) permits, with a
deprecation warning, conditionals (`failed_when`, `until`, `assert.that` and similar) fully enclosed
in template delimiters, string constants such as `when: some_var == '{{ some_other_var }}'`, and
positional lookup arguments. When disabled, they are errors; the docs say a future release will
disable the feature by default.

## Dynamic names without delimiters
```yaml
when: hostvars[inventory_hostname]['enable_' ~ service_name] | default(false) | bool
when: vars['feature_' ~ item] is defined
when: item.name in existing_users.stdout_lines
```
Use `~` for string concatenation and `vars[...]` / `hostvars[...]` lookups instead of building a
variable name with `{{ }}`.

## Quoting
YAML needs quotes when the expression would otherwise be parsed as something else: for example an
unquoted string with a space after a colon is read as a mapping.
```yaml
when: "'web' in group_names"
when: "result.stdout is search('ready: true')"
```

## Verify
```bash
ansible-lint -t no-jinja-when playbooks/
```

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_conditionals.rst, 2.19 porting guide), the
ansible-core devel `config/base.yml` entry for `ALLOW_EMBEDDED_TEMPLATES` (`version_added` 2.19) and the
ansible-lint `no-jinja-when` rule page. Fixed: the `search('ready: true')` example needed quotes to be valid
YAML. Removed the quoted warning text (the wording is not in the current source) and an unconfirmed
injection claim.
Method: documentation only; no commands were run.
