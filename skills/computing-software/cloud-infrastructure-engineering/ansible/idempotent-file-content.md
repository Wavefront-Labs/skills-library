---
id: computing-software.cloud-infrastructure-engineering.ansible.idempotent-file-content
name: idempotent-file-content
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, idempotency, idempotent-content, templates, jinja2]
level: practitioner
status: docs-checked
description: "Keep generated files byte-stable across runs: no timestamps, sorted dict and list output, stable to_nice_json/yaml, ansible_managed without dates, and no random values."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/filter/to_nice_json.yml", "https://github.com/pallets/jinja/blob/main/docs/templates.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Idempotent file content

A template that renders differently on each run makes the task changed and fires handlers every time.

## Sources of churn and fixes
| Cause | Fix |
|---|---|
| `{{ ansible_date_time.iso8601 }}` or `now()` in a header | remove; git history is the timestamp |
| `ansible_managed` text containing timestamps | keep the setting without date placeholders (the default value is `Ansible managed`; the `ansible_managed` ini key is deprecated, to be removed in 2.23, in favour of setting the `ansible_managed` variable) |
| iterating a dict whose order varies | `{% for k, v in mydict | dictsort %}` |
| set/unique producing unstable order | `| sort` after `unique`/`union` |
| `to_json`/`to_yaml` key order | `to_nice_json` and `to_nice_yaml` default to `sort_keys=True`; the docs show `to_json(indent=4, sort_keys=True)` |
| `random` for cron minutes or passwords | `random(seed=inventory_hostname)` (the filter docs show this for cron times) |
| password hashes with random salt | pass a fixed salt to `password_hash` (the filter docs derive one with `random(seed=inventory_hostname)`), or `update_password: on_create` on the user module |
| hostvars of hosts not in play/limit | gather or cache facts, or default to stable values |
| trailing whitespace from Jinja blocks | `trim_blocks`/`lstrip_blocks` consistently |

## Examples
```jinja
{# hosts list sorted for stable output #}
{% for h in groups['web'] | sort %}
server {{ h }} {{ hostvars[h].ansible_host }}:8080
{% endfor %}
```
```yaml
- ansible.builtin.cron:
    name: logrotate-app
    minute: "{{ 59 | random(seed=inventory_hostname) }}"
    job: /usr/sbin/logrotate /etc/logrotate.d/app
```

## Detect
```bash
ansible-playbook site.yml --check --diff -l web01       # after convergence: no diff expected
```

## Verify
- [ ] `--check --diff` on a converged host shows no file diffs.

## Checked
Checked 2026-10-26 against ansible-documentation playbooks_filters.rst, ansible-core devel `config/base.yml`
(DEFAULT_MANAGED_STR) and filter docs `to_nice_json.yml`/`to_nice_yaml.yml`, and Jinja `templates.rst` and `filters.py`
(`dictsort`, `trim_blocks`/`lstrip_blocks`). Confirmed `random(seed=inventory_hostname)` for cron, password_hash salt examples,
`sort_keys` default true, `ansible_managed` default and deprecation. Corrected the `ansible_managed` and `sort_keys` rows.
Method: documentation only; no commands were run.
