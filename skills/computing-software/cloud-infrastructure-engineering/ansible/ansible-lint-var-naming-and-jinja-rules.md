---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-lint-var-naming-and-jinja-rules
name: ansible-lint-var-naming-and-jinja-rules
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-lint, var-naming, jinja-rule, lint-naming-rules]
level: practitioner
status: docs-checked
description: "Fix ansible-lint var-naming (pattern, no-role-prefix, reserved, no-jinja) and jinja (spacing, invalid) findings, with config options and when to noqa."
sources: ["ansible-lint var-naming rule (https://ansible.readthedocs.io/projects/lint/rules/var-naming/)", "ansible-lint jinja rule (https://ansible.readthedocs.io/projects/lint/rules/jinja/)", "ansible-lint profiles (https://ansible.readthedocs.io/projects/lint/profiles/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# var-naming and jinja rules

## var-naming
| Sub-rule | Meaning | Fix |
|---|---|---|
| `var-naming[pattern]` | name must match `^[a-z_][a-z0-9_]*$` | `appPort` → `app_port` |
| `var-naming[no-role-prefix]` | variables inside a role should start with `role_name_` (underscores before the prefix are accepted) | in role `nginx`: `port` → `nginx_port` (or `__nginx_port` for internal) |
| `var-naming[no-reserved]` | Ansible reserved names (for example `hosts`) | rename |
| `var-naming[no-keyword]` | Python keywords | rename |
| `var-naming[no-jinja]` | Jinja in a variable name | restructure |
| `var-naming[read-only]` | assigning a read-only special variable (for example `role_name`) | rename |
| `var-naming[non-string]`, `[non-ascii]` | names that are not strings / not ASCII | use plain ASCII string names |

Config:
```yaml
# .ansible-lint
var_naming_pattern: "^[a-z_][a-z0-9_]*$"
```
With `include_role`/`import_role`, variables passed in `vars` should carry the included role's prefix; in other task types, `vars` are task-scoped and need no prefix.

## jinja
| Sub-rule | Example finding | Fix |
|---|---|---|
| `jinja[spacing]` | `{{some|dict2items}}` | `{{ some | dict2items }}`; also `when: "{{ foo | bool }}"` → `when: foo | bool` (conditions are templated implicitly) |
| `jinja[invalid]` | invalid template such as `{{ & }}` or `{{ {{ '1' }} }}` | fix the syntax |

`ansible-lint --fix` can rewrite `jinja` findings automatically, along with yaml and fqcn rules. The formatter follows black style and skips blocks with newlines, `~` concatenation and dotted numeric access such as `foo.0.bar`:
```bash
ansible-lint --fix=jinja,fqcn,yaml
```

## When noqa is acceptable
- A role that is not yet compliant but is called with `include_role`/`import_role` `vars`: `# noqa: var-naming[no-role-prefix]`.
- Templates generating other templating languages (Helm, Go templates): prefer `{% raw %}` over noqa.

## Gotchas
- Renaming role variables is a breaking change for consumers; deprecate old names with a compatibility mapping in `defaults` for one release.
- `jinja` and `var-naming` are both in the `basic` profile.

## Verify
```bash
ansible-lint -t var-naming,jinja roles/
```

## Checked
Checked 2026-10-23 against the ansible-lint documentation source on GitHub (docs/rules/var-naming.md, jinja.md, profiles.md; latest release v26.10.1): the var-naming sub-rules and meanings, the default pattern and the `var_naming_pattern` setting, the include_role/import_role prefix note, the jinja sub-rules and examples, the formatter limitations, the `--fix` support and the profile membership of both rules. Removed the unconfirmed claim that register and set_fact names inside roles must carry the prefix and the profile-version aside.
Method: documentation only; no commands were run.
