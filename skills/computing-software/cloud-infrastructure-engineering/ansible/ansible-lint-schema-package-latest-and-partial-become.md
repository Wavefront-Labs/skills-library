---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-lint-schema-package-latest-and-partial-become
name: ansible-lint-schema-package-latest-and-partial-become
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-lint, schema-rule, package-latest, partial-become, no-free-form]
level: practitioner
status: docs-checked
description: "Fix ansible-lint schema[] validation findings for playbooks, meta, galaxy and tasks, plus package-latest, partial-become and no-free-form rules."
sources: ["ansible-lint schema rule (https://ansible.readthedocs.io/projects/lint/rules/schema/)", "ansible-lint package-latest rule (https://ansible.readthedocs.io/projects/lint/rules/package-latest/)", "ansible-lint partial-become rule (https://ansible.readthedocs.io/projects/lint/rules/partial-become/)", "ansible-lint no-free-form rule (https://ansible.readthedocs.io/projects/lint/rules/no-free-form/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# schema, package-latest, partial-become, no-free-form

## schema[...]
ansible-lint validates files against JSON schemas by file kind:
| Finding | File | Typical cause |
|---|---|---|
| `schema[playbook]` | playbooks | misspelt play keyword, task at play level |
| `schema[tasks]` | task files | `whne:`, wrong indentation, unknown keyword |
| `schema[meta]` | `meta/main.yml` | role metadata errors; `galaxy_info.standalone` is required, and an empty or comment-only file fails |
| `schema[galaxy]` | `galaxy.yml` | collection metadata errors |
| `schema[requirements]` | `requirements.yml` | wrong keys |
| `schema[vars]` | `vars/*.yml` and `defaults/*.yml` | schema violations |
| `schema[ansible-lint-config]` | `.ansible-lint` | unknown option |
| `schema[moves]` | any | "foo was moved to bar in 2.10"-style module moves |

File kinds are guessed from paths (for example `tasks/**/*.yml` for task files); add patterns with `kinds:` in `.ansible-lint` for non-standard layouts:
```yaml
kinds:
  - playbook: "deploy/**/*.yml"
  - tasks: "common/tasks/*.yml"
```
The `schema` rule is mandatory: inline `noqa` comments cannot silence it, and it is validated before the other rules.

## package-latest
`state: latest` installs software and also updates it and installs additional packages. Fix: `state: present` with a pinned version, or keep `latest` and set `update_only: true` (dnf) or `only_upgrade: true` (apt) so no extra packages are installed; `# noqa: package-latest` is the last resort.

## partial-become
`become_user` without `become: true` in the same place (play or task) is reported as `partial-become[play]` or `partial-become[task]`. The rule ignores inherited `become`, so set both together. Fix:
```yaml
- name: Run as postgres
  ansible.builtin.command: psql -c 'select 1'
  become: true
  become_user: postgres
```

## no-free-form
`ansible.builtin.command: chdir=/srv echo hi` (a string containing `=` counts as free-form) → pass a dictionary:
```yaml
ansible.builtin.command:
  cmd: echo hi
  chdir: /srv
```
For `raw`, only `executable=` inside the string is flagged (`no-free-form[raw]`); use `args: {executable: ...}`. `ansible-lint --fix=no-free-form` can convert cases automatically.

## Verify
```bash
ansible-lint -t schema,package-latest,partial-become,no-free-form
```

## Checked
Checked 2026-10-23 against the ansible-lint documentation source on GitHub (docs/rules/schema.md, package-latest.md, partial-become.md, no-free-form.md; latest release v26.10.1): the schema sub-rules and the files they match, the mandatory (non-noqa) status, the `galaxy_info.standalone` requirement, `update_only`/`only_upgrade`, `partial-become[play|task]` and its ignoring of inherited become, free-form detection and the `raw` special case. Removed the unconfirmed "bad platforms name / missing license keys" causes.
Method: documentation only; no commands were run.
