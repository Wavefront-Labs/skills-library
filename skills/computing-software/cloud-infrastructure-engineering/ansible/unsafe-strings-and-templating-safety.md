---
id: computing-software.cloud-infrastructure-engineering.ansible.unsafe-strings-and-templating-safety
name: unsafe-strings-and-templating-safety
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, variables-precedence, unsafe-strings, jinja2, security]
level: advanced
status: docs-checked
description: "Mark data as !unsafe so Ansible never templates it, protect against Jinja injection from external sources, and handle literal braces in passwords and configs."
sources: ["Ansible advanced playbook syntax, unsafe or raw strings (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_advanced_syntax.html#unsafe-or-raw-strings)", "Ansible Core 2.19 porting guide, template trust model inversion (https://docs.ansible.com/ansible/latest/porting_guides/porting_guide_core_2.19.html)", "Templating (Jinja2) (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# !unsafe strings

Ansible templates variable values: a value that contains Jinja can be evaluated. That breaks passwords containing `{%` and is a code-injection path when values come from untrusted sources. The `unsafe` data type blocks templating.

## Mark literals unsafe
```yaml
vars:
  mypassword: !unsafe 234%234{435lkj{{lkjsdf
  my_unsafe_variable: !unsafe 'unsafe % value'
```
For hashes and lists, mark the individual elements:
```yaml
my_unsafe_array:
  - !unsafe 'unsafe element'
  - 'safe element'
my_unsafe_hash:
  unsafe_key: !unsafe 'unsafe value'
```
Values supplied through `vars_prompt` can also be marked unsafe (see the prompts documentation).

## Data from outside
Values returned by lookup plugins are unsafe by default (before ansible-core 2.19), which blocks templating of their content and prevents Jinja injection.

ansible-core 2.19 inverts this model: only strings marked as loaded from a trusted source are eligible to be rendered as templates. Templates in playbooks, roles, variable files and most built-in inventory plugins are trusted; untrusted values can still be referenced by templates, but a template appearing inside an untrusted string is returned unmodified, and by default this fails silently. Custom plugins that source template strings must apply trust through the plugin API. Newly created strings from template operations are never trusted automatically. The environment variable `_ANSIBLE_TEMPLAR_UNTRUSTED_TEMPLATE_BEHAVIOR` (`warning` or `error`) makes untrusted templates visible while troubleshooting.

## Alternatives
| Need | Use |
|---|---|
| Literal braces inside a template file | `{% raw %} ... {% endraw %}` |
| Literal braces in a task argument | `!unsafe`, or Jinja that emits the braces |

## Verify
```yaml
- ansible.builtin.debug: {var: mypassword}     # prints the literal braces
```

## Checked
Checked 2026-10-23 against the Ansible documentation source on GitHub (playbooks_advanced_syntax.rst, porting_guide_core_2.19.rst; latest ansible-core release v2.21.5): the `!unsafe` syntax for scalars, lists and hashes, lookup results being unsafe, the 2.19 trust model inversion and its details, and the untrusted-template troubleshooting variable. Removed the unconfirmed claims that facts and registered results are unsafe, that `-e` and `include_vars` values are templated, that `!vault` values are decrypted and then templated, that `!unsafe` cannot be used in JSON extra vars, the `lookup('file')` workaround and the claim about concatenating unsafe values in older cores.
Method: documentation only; no commands were run.
