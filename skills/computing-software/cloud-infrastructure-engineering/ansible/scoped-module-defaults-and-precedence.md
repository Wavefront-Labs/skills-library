---
id: computing-software.cloud-infrastructure-engineering.ansible.scoped-module-defaults-and-precedence
name: scoped-module-defaults-and-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, module-defaults, block-module-defaults, role-module-defaults, module-defaults-precedence, action-groups]
level: practitioner
status: docs-checked
description: "Set module_defaults at play, block, role or task scope, predict how nested scopes merge and that explicit task arguments always win, and avoid role default leakage."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_module_defaults.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/executor/module_common.py", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html#inject-invocation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scoped module_defaults and precedence

## Scopes
`module_defaults` can be set at the play, block and task level; defaults set at play level (or block or task level on `include_role`/`import_role`) also apply to any roles used.
```yaml
- hosts: localhost
  module_defaults:
    group/aws:                        # action group: every module of amazon.aws/community.aws
      region: eu-west-1
  tasks:
    - name: Prod resources
      module_defaults:
        group/aws:
          profile: prod
      block:
        - amazon.aws.s3_bucket: {name: logs-prod}               # profile prod; region NOT set (inner group/aws replaces the outer one)
        - amazon.aws.s3_bucket: {name: logs-dr, region: eu-central-1}   # explicit arg wins
```

## Precedence rules
1. An argument written on the task always wins over any default.
2. Nested scopes are combined by top-level key (a module name or a `group/<name>`): an inner scope's entry for the same key **replaces** the outer entry as a whole, it does not merge option by option, while entries for different keys all apply. To keep an outer option, repeat it in the inner entry.
3. Module-specific defaults (`amazon.aws.s3_bucket:`) are applied after, and so override, action-group defaults (`group/aws:`).
4. An empty dict (`ansible.builtin.file: {}`) removes earlier defaults for that module. List the FQCN you use, as the documentation examples do.

## Roles
```yaml
tasks:
  - ansible.builtin.include_role:
      name: app
    module_defaults:
      ansible.builtin.uri: {timeout: 5}
```
Defaults set at play level, or at block or task level on `include_role`/`import_role`, apply to the tasks of the role, which can cause unexpected behaviour inside it. Defining `module_defaults` on a block inside the role's own tasks is the self-contained way, and role authors should not rely on play-level defaults being present.

## Templated values
```yaml
module_defaults:
  ansible.builtin.uri:
    headers: {Authorization: "Bearer {{ api_token }}"}
    validate_certs: "{{ validate_tls | default(true) }}"
```
Values are templated when the task runs (the module_defaults helper resolves them per task), so host variables can be used.

## Gotchas
- A group default is added to every module in the group, so set only options that all member modules accept (the docs advise checking the group's modules in its `meta/runtime.yml` or the collection documentation).
- Defaults are invisible at the call site; document them near the top of the play.

## Verify
- [ ] The tasks behave as if the defaulted options were set (the `invocation` result key is only added when `inject_invocation` is enabled, a setting introduced in ansible-core 2.21 with default false).

## Checked
Checked 2026-10-25 against ansible-core devel `executor/module_common.py` (`get_action_arg_defaults`: the list of scope dicts is merged with `dict.update` by top-level key, group defaults applied first and module-specific defaults after, values resolved by the templar at task time), `playbook/base.py` (`module_defaults` list attribute, extend and prepend), `config/base.yml` (INJECT_INVOCATION) and ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_module_defaults.rst. Confirmed: scopes, explicit task arguments winning, empty-dict reset, group versus module order, role propagation. Corrected the claim that nested scopes merge option by option (an inner entry for the same key replaces the outer one) and fixed the example comment. Removed unconfirmed claims about `Unsupported parameters`, `command`/`shell` behaviour and role-entry scope.
Method: documentation only; no commands were run.
