---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-lint-config-file-noqa-and-autofix
name: ansible-lint-config-file-noqa-and-autofix
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-lint, ansible-lint-config, skip-list, warn-list, noqa, lint-fix, autofix, ignore-file]
level: practitioner
status: docs-checked
description: "Configure ansible-lint with .ansible-lint (profile, exclude_paths, skip_list, warn_list, enable_list), suppress with noqa or an ignore file, and apply --fix autofixes."
sources: ["ansible-lint configuration (https://ansible.readthedocs.io/projects/lint/configuring/)", "ansible-lint usage (https://ansible.readthedocs.io/projects/lint/usage/)", "ansible-lint autofix (https://ansible.readthedocs.io/projects/lint/autofix/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-lint: config file, noqa and autofix

## .ansible-lint (project root; also .ansible-lint.yml/.yaml, .config/ansible-lint.yml/.yaml)
```yaml
---
profile: production            # min | basic | moderate | safety | shared | production
exclude_paths:
  - .cache/
  - collections/ansible_collections/   # vendored content
  - tests/fixtures/
skip_list:                     # never reported
  - yaml[line-length]
warn_list:                     # reported, but do not fail
  - experimental
  - role-name[path]
enable_list:                   # opt-in rules
  - name[prefix]
  - no-same-owner
offline: true                  # disable installation of requirements.yml and schema refreshing
kinds:                         # tell lint what unusual files are
  - playbook: "**/playbooks/*.yml"
mock_modules: [acme.internal.special]   # modules not installed in CI
mock_roles: [vendor.secret_role]
var_naming_pattern: "^[a-z_][a-z0-9_]*$"
use_default_rules: true
rulesdir: [./lint_rules]       # custom rule directories
```
`skip_list`/`warn_list` take rule ids or `rule[subrule]` tags. Prefer narrow subrule tags over
skipping whole rules. On the command line, list values such as `skip_list`, `warn_list` and `exclude_paths` are
appended to the file's values, while scalar options override them. Run lint from the project root.

## Suppressing a single finding
```yaml
- name: Legacy migration script     # noqa: no-changed-when command-instead-of-shell
  ansible.builtin.shell: ./migrate.sh | tee /var/log/m.log
```
Add `# noqa: <rule>` at the end of a line in the task; list several rule ids separated by spaces. Always name the
rule. Line-based rules need the comment at the end of the offending line. The `schema` rule is mandatory and cannot
be silenced with `noqa`.

Bulk legacy findings: an ignore file `.ansible-lint-ignore` (or `.config/ansible-lint-ignore.txt`) next to the config file; `#` starts a comment:
```
roles/legacy/tasks/main.yml no-changed-when
playbooks/old.yml fqcn[action-core]
```
Generate with `ansible-lint --generate-ignore` (it overwrites the existing file). Ignored rules still print a non-fatal warning; add `skip` to a line (`playbooks/old.yml role-name skip`) to silence it. Shrink the file over time.

## Autofix
```bash
ansible-lint --fix                      # all fixable rules
ansible-lint --fix=fqcn,yaml,no-free-form
```
`--fix` takes `all`, `none` or a comma-separated list of rule ids or tags (the `write_list` option does the same in the config). Rules with transforms include `command-instead-of-shell`, `deprecated-local-action`, `fqcn`, `jinja`, `key-order`, `name`, `no-free-form`, `no-jinja-when`, `no-log-password`, `partial-become` and `yaml`.
YAML reformatting runs whenever `--fix` is used, even with `write_list: ["none"]` or with `yaml[...]` in `skip_list`. It rewrites files: run on a clean git tree and review the diff.

## Gotchas
- Unless `offline: true`, lint installs `requirements.yml` content; CI should pre-install or mock.
- Pin ansible-lint in CI and pre-commit (`rev:`) so new releases do not change the findings.
- Modules from collections that are not installed fail the syntax check; install them or use `mock_modules` (stubs are written under `{cache_dir}/ansible-lint-mocks/` and never overwrite installed modules).

## Verify
- [ ] The ansible-lint version and config are pinned; `ansible-lint` exits 0 on main.
- [ ] `ansible-lint -L` lists rules; `ansible-lint -T` lists tags for skip/warn entries.

## Checked
Checked 2026-10-23 against the ansible-lint documentation source on GitHub (latest release v26.10.1) and its cli.py: config file names, CLI-versus-file merge rules, the sample .ansible-lint keys (profile, exclude_paths, skip_list, warn_list, enable_list, offline, kinds, mock_modules, mock_roles, var_naming_pattern, rulesdir, write_list), noqa placement, the ignore file (names, `--generate-ignore`, `skip` suffix), `--fix` semantics and the list of rules with transforms, `-L`/`-T`. Removed the unconfirmed claims that a bare noqa is flagged, that `--fix` preserves comments via a ruamel formatter, and that rule ids change between major versions.
Method: documentation only; no commands were run.
