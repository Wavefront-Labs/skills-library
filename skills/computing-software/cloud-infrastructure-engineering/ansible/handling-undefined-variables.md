---
id: computing-software.cloud-infrastructure-engineering.ansible.handling-undefined-variables
name: handling-undefined-variables
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, variables-precedence, error-on-undefined, strict-undefined, default-filter, omit, mandatory, argument-specs]
level: practitioner
status: docs-checked
description: "Handle undefined variables deliberately: default and default(omit), mandatory, is defined tests, error_on_undefined_vars, and role argument_specs validation."
sources: ["Ansible filters guide, handling undefined variables (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html#handling-undefined-variables)", "Ansible filters, mandatory (https://docs.ansible.com/ansible/latest/collections/ansible/builtin/mandatory_filter.html)", "Ansible configuration reference, DEFAULT_UNDEFINED_VAR_BEHAVIOR (https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-undefined-var-behavior)", "Ansible role argument validation (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-argument-validation)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Handling undefined variables

By default Ansible fails a task whose templated expression references an undefined variable. Keep it that way and make every optional variable explicit. (In the ansible-core configuration reference, `DEFAULT_UNDEFINED_VAR_BEHAVIOR` / `error_on_undefined_vars` is marked deprecated, "no longer used in the Ansible Core code base", with removal scheduled for 2.23, so do not rely on turning the failure off.)

## Tools
```yaml
port: "{{ app_port | default(8080) }}"
port: "{{ app_port | default(8080, true) }}"    # also use the default for false or empty values
mode: "{{ file_mode | default(omit) }}"         # no value sent to the module if unset
token: "{{ api_token | mandatory(msg='api_token must be set') }}"
galaxy_api_key: "{{ undef(hint='You must specify your Galaxy API key') }}"
```
`omit` makes a module parameter optional: Ansible sends no value and the module uses its own default. When chaining filters after `default(omit)`, the filters guide suggests `"{{ foo | default(None) | some_filter or omit }}"`. `undef(hint=...)` gives a variable an undefined value with a hint, a convenient way to require an override.

Since ansible-core 2.8, accessing an attribute of an undefined value returns another undefined value, so `{{ foo.bar.baz | default('DEFAULT') }}` works when intermediate keys may be missing.

## Tests
```yaml
when: proxy_url is defined
when: proxy_url is defined and proxy_url | length > 0
when: app.tls is undefined
```

## Fail early, with a message
```yaml
- ansible.builtin.assert:
    that:
      - db_host is defined
      - db_port | int > 0
    fail_msg: "db_host/db_port must be set in group_vars"
    quiet: true
```

## Roles: argument_specs
`roles/app/meta/argument_specs.yml` (or `.yaml`) validates inputs: when it exists, a task is inserted at the start of role execution that validates the supplied parameters, and the role fails if validation fails. The task is tagged `always`.
```yaml
argument_specs:
  main:
    short_description: Deploy app
    options:
      app_version: {type: str, required: true}
      app_port: {type: int, default: 8080}
      app_env: {type: str, choices: [dev, stage, prod]}
```
The entry point name is `main` unless the role has other entry points. `short_description` is displayed by `ansible-doc -t role -l`.

## Gotchas
- `default()` does not replace an empty string, `0` or `false` unless the second argument is `true`.
- Use `omit` as a whole argument value, not inside a longer string.

## Verify
- [ ] Run once with minimal inventory: every missing required input fails at assert or argument_specs with a clear message, not deep inside a template.

## Checked
Checked 2026-10-23 against the Ansible documentation source and ansible-core source on GitHub (playbooks_filters.rst, playbooks_reuse_roles.rst, config/base.yml, plugins/filter/mandatory.yml, modules/assert.py; latest ansible-core release v2.21.5): `default` with and without the second argument, `omit` and its chaining note, `mandatory` with the `msg` option, `undef(hint=...)`, the 2.8 nested-undefined behaviour, `assert` options, the argument_specs file names, inserted validation task and `always` tag, and the deprecation of `DEFAULT_UNDEFINED_VAR_BEHAVIOR`. Wrong or stale claims fixed: `error_on_undefined_vars` is deprecated and no longer used (the skill treated it as a live switch); `mandatory` takes `msg=`. Removed the unconfirmed argument_specs error text, the `ansible-inventory --vars` and `-vvv` origin tips, the skipped-task claim and the `omit`-inside-string claim.
Method: documentation only; no commands were run.
