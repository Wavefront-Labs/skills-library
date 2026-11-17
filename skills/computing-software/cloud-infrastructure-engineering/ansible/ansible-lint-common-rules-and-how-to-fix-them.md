---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-lint-common-rules-and-how-to-fix-them
name: ansible-lint-common-rules-and-how-to-fix-them
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-lint, fqcn-rule, name-rule, yaml-rule, no-changed-when, command-instead-of-module, risky-file-permissions, risky-shell-pipe]
level: practitioner
status: docs-checked
description: "Fix the ansible-lint findings that fire most: fqcn, name, yaml, no-changed-when, command-instead-of-module, risky-file-permissions, risky-shell-pipe, var-naming, no-handler."
sources: ["ansible-lint rules (https://github.com/ansible/ansible-lint/tree/main/docs/rules)", "ansible-lint rule index (https://ansible.readthedocs.io/projects/lint/rules/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-lint: the common rules and how to fix them

## Naming and style rules
| Rule | Trigger | Fix |
|---|---|---|
| `fqcn[action-core]`, `fqcn[action]` | `copy:` instead of `ansible.builtin.copy:` | use FQCN (`--fix` does it) |
| `fqcn[canonical]` | alias of a moved module | use the canonical name lint suggests |
| `name[missing]`, `name[casing]`, `name[template]`, `name[play]` | unnamed task, lowercase start, Jinja not at the end of the name | name everything, capitalise, template only at the end |
| `yaml[truthy]` | `yes/no/True` | `true/false` |
| `yaml[line-length]` | line too long (yamllint) | folded scalars `>-`, or skip the subrule |
| `yaml[indentation]`, `yaml[comments]` | formatting | `--fix` reformats YAML |
| `key-order` | `name` not first; `block`/`rescue`/`always` not last | reorder |
| `var-naming[pattern]`, `[no-role-prefix]` | dashes/uppercase; role vars without role prefix | rename `nginx_port` |
| `jinja[spacing]` | `{{foo}}` | `{{ foo }}` |

## Risk rules (these find real bugs)
**no-changed-when** — command/shell without `changed_when`:
```yaml
- ansible.builtin.command: uptime
  register: s
  changed_when: false
```
**command-instead-of-module** — a `command`/`shell` task that runs something a module covers (for example `apt-get update`
becomes `ansible.builtin.apt` with `update_cache: true`); the rule's source lists the commands it knows.

**command-instead-of-shell** — `shell` without shell features; switch to `command`.

**risky-file-permissions** — `copy`/`template`/`file`/`get_url` and similar modules creating files without `mode`
(permissions then depend on current system settings), or `create: true` without permissions:
```yaml
- ansible.builtin.template: {src: a.j2, dest: /etc/a.conf, mode: "0644", owner: root, group: root}
```
**risky-octal** — `mode: 644` (an integer) → `"0644"` (quoted with leading zero; `"0o644"` or symbolic modes also work).

**risky-shell-pipe** — pipes without `set -o pipefail`:
```yaml
- ansible.builtin.shell:
    cmd: |
      set -o pipefail
      false | cat
    executable: /bin/bash
```
**no-handler** — `when: result.changed` on a following task → convert to a handler.
**ignore-errors** — blanket `ignore_errors: true` → `failed_when` with conditions, `register` the result, or `ignore_errors: "{{ ansible_check_mode }}"`.
**package-latest** — `state: latest` installs and updates; use `state: present` with a pinned version, or add `update_only: true` (dnf) / `only_upgrade: true` (apt).
**latest[git]** / **latest[hg]** — `version: HEAD`; pin a tag/commit.
**no-relative-paths** — relative `src` (for example `../my_templates/foo.j2`) in `copy`/`template`; use the `files/` or `templates/` folder or an absolute path.
**partial-become** — `become_user` without `become: true` in the same place (play or task); the rule does not look at inherited values.

## Approach for a legacy repo
1. `ansible-lint --fix=fqcn,yaml,name` and commit separately (mechanical).
2. Generate `.ansible-lint-ignore` for the rest; fail CI only on new findings.
3. Burn down risk rules first (`no-changed-when`, `risky-*`, `command-instead-of-module`) — they change behaviour, so test with Molecule/`--check`.

## Verify
- [ ] `ansible-lint --profile production` passes, or only ignore-file entries remain with owners.

## Checked
Checked 2026-10-23 against the ansible-lint documentation source on GitHub (latest release v26.10.1): sub-rule names for fqcn, name, var-naming, partial-become; key-order wording; risky-file-permissions, risky-octal, risky-shell-pipe (cmd plus executable form), package-latest (update_only/only_upgrade), ignore-errors alternatives, no-relative-paths, latest[git]/[hg], no-handler and the `--fix` / `--generate-ignore` options. Removed the unconfirmed 160-character line-length figure.
Method: documentation only; no commands were run.
