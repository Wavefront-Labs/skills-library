---
id: computing-software.cloud-infrastructure-engineering.ansible.jinja2-templates-and-the-template-module
name: jinja2-templates-and-the-template-module
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, jinja2, templates, template-module, templating, j2, ansible-managed, validate, backup, trim-blocks, lstrip-blocks, whitespace-control, macros, include, template-lookup, block-start-string, native-jinja, to-nice-yaml, to-json, config-files, deploy-config]
level: practitioner
status: docs-checked
description: "Render config files with Ansible's template module and Jinja2: loops/conditionals in .j2, whitespace control, validate before install, backup, ansible_managed, macros, native Jinja type gotchas."
sources: ["https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/modules/template.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/doc_fragments/template_common.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_templating.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/porting_guides/porting_guide_core_2.19.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jinja2 templates and the template module

**Goal:** generated config files that are correct for every host, validated before
they are installed, and diffable in a review.

## 1. The task
```yaml
- name: Update sshd configuration safely
  ansible.builtin.template:
    src: sshd_config.j2                # templates/ in a role, relative to the playbook otherwise
    dest: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: "0600"
    validate: /usr/sbin/sshd -t -f %s  # %s = temp file; installed only if the command succeeds
    backup: true                       # keeps dest.<pid>.<timestamp>~ when the file changes
  notify: restart sshd
```
`validate` runs the command against the rendered temp file **before** it replaces `dest`;
`%s` must be present. The command is passed securely, so shell features such as expansion
and pipes do not work. The module's own examples validate sudoers with
`/usr/sbin/visudo -cf %s` and sshd with `/usr/sbin/sshd -t -f %s`.

`--diff` shows before/after for each changed template; `--check --diff` previews.

## 2. The template
```jinja
{{ ansible_managed | comment }}
server {
    listen {{ site.port | default(80) }};
    server_name {{ site.name }}{% for a in site.aliases | default([]) %} {{ a }}{% endfor %};
{% if site.tls | default(false) %}
    ssl_certificate /etc/pki/tls/certs/{{ site.name }}.crt;
{% endif %}
{% for loc in site.locations %}
    location {{ loc.path }} {
        proxy_pass http://{{ loc.upstream }};
    }
{% endfor %}
}
```
- `ansible_managed` defaults to the string `Ansible managed`. Set it as an ordinary variable (the `ansible_managed` key in `ansible.cfg` is deprecated, removal planned for 2.23). Never put a date or other per-run value in it: the module notes that a date in the template marks it changed on every run.
- `comment` renders text in a comment style: `plain` (default), `decoration`, `erlang`, `c`, `cblock`, `xml`, for example `comment('xml')`.
- Dicts, sorted for stable output: `{% for k, v in settings | dictsort %}`.
- Multi-line data: `{{ cert_pem | indent(4) }}`, `{{ data | to_nice_yaml(indent=2) }}`, `{{ data | to_nice_json }}`.
- Optional line: `{% if x is defined %}...{% endif %}`.
- Jinja macros (`{% macro %}`), `{% import %}` and `{% include %}` work as in Jinja2.
- Extra variables inside a template: `template_host`, `template_uid`, `template_path`, `template_fullpath`, `template_destpath`, `template_run_date`.

## 3. Whitespace
The template module defaults to `trim_blocks: true` (first newline after a block tag removed) and
`lstrip_blocks: false` (set it to `true` to strip leading spaces and tabs before a block tag; useful
for indented `{% if %}` in YAML or ini output). Override per task, or with a first-line header in the
template such as `#jinja2: lstrip_blocks: True`. `{%-` and `-%}` strip manually.

## 4. Where templating happens
- Templating runs on the **control node** before the task is sent; the `template` module renders there and copies the result, so the managed node never sees Jinja and only the control node needs `jinja2`. Template files must be UTF-8 (`output_encoding` controls the output).
- `lookup('template', 'x.j2')` renders into a variable; `ansible.builtin.copy: content:` can then write it.
- Delimiters that clash with other tools (Helm, Go templates): set `block_start_string`, `variable_start_string` (and the matching end strings) on the task, use the `#jinja2:` header, or wrap the foreign braces in `{% raw %}...{% endraw %}`.

## 5. Types
Since ansible-core 2.19 Jinja native mode is always used for expressions in playbooks and the `jinja2_native` setting is deprecated and has no effect. The `template` **module** is different: it generates text files and never uses native types. Filters that expect strings convert other values to strings silently, for example `['a', 'b'] | replace('a', 'x')` gives a string, so use `map('replace', ...)` to keep a list. A template that evaluates to `None` can now yield `None` instead of an empty string; end an `{% if %}` with `{% else %}{{ "" }}{% endif %}` when you need a string.

## Gotchas
- A template that uses `hostvars[other]` needs facts from `other` (gathered or cached).
- Quote `mode`: a bare number is treated as decimal, and a leading zero (`0644`) "works sometimes, but can fail in loops". Use `"0644"` or a symbolic mode. Setting `mode` also avoids creating files with the system umask default.
- `backup: true` leaves files in the destination directory; do not use it where the daemon loads everything in a glob-included directory.
- Undefined variables fail the task by default; use `| default(...)` deliberately. The `error_on_undefined_vars` setting is deprecated and no longer used.
- Windows targets: `ansible.windows.win_template` (defaults to `\r\n`); on POSIX targets `newline_sequence` accepts `\n`, `\r` or `\r\n`.

## Verify
- [ ] `ansible-playbook site.yml --check --diff --limit one-host` shows exactly the intended config diff.
- [ ] Break the template deliberately and confirm `validate` refuses the install.
- [ ] A second run reports `changed=0` for every template task.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed against the `template` module and `template_common`, `validate`, `backup` and `files` doc fragments, `lib/ansible/config/base.yml` (`DEFAULT_JINJA2_NATIVE`, `DEFAULT_MANAGED_STR`, `DEFAULT_UNDEFINED_VAR_BEHAVIOR` all deprecated), the `comment` filter documentation, the backup naming in `module_utils/basic.py`, and the 2.19 porting guide (native mode, None results). Removed unconfirmed validators for other tools and macro path-resolution claims.
Method: documentation only; no commands were run.
