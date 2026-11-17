---
id: computing-software.cloud-infrastructure-engineering.ansible.custom-module-development
name: custom-module-development
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, module-development, custom-modules, module-utils, ansiblemodule, argument-spec, check-mode, diff-mode, exit-json, fail-json, library-dir, documentation-yaml, examples-yaml, return-yaml, action-plugins, powershell-modules, binary-modules, module-unit-tests, hacking-test-module, module-local-testing, python-modules, validate-modules, no-log-params, required-if]
level: advanced
status: docs-checked
description: "Write a custom Ansible module in Python: argument_spec, idempotent logic with check and diff mode, exit_json/fail_json, module_utils, DOCUMENTATION and testing."
sources: ["Developing modules (general) (https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)", "Ansible module architecture, binary and want-JSON modules (https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html)", "Module utilities (https://docs.ansible.com/ansible/latest/dev_guide/developing_module_utilities.html)", "Unit testing Ansible modules (https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html)", "Windows module development (https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general_windows.html)", "AnsibleModule source (https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/basic.py)", "Argument spec type validators (https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/common/parameters.py)"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Custom module development

**Goal:** when no module exists for an API or appliance, write one that behaves like
`ansible.builtin` — validated args, honest `changed`, check/diff support, documented.

## 1. Where it lives
`library/` next to the playbook (quick), `roles/x/library/` (role-local), or
`plugins/modules/` in a collection (the right long-term home). Shared code goes in
`module_utils/` and is imported as `ansible.module_utils.<name>` (library/) or
`ansible_collections.<ns>.<coll>.plugins.module_utils.<name>`; Ansible packs it into the AnsiballZ zip.

## 2. The skeleton
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
module: app_feature
short_description: Enable or disable a feature flag in App
version_added: "1.2.0"
description: [Idempotently sets a feature flag via the App admin API.]
options:
  name: {description: Flag name., type: str, required: true}
  state: {description: Desired state., type: str, choices: [enabled, disabled], default: enabled}
  url: {description: API base URL., type: str, required: true}
  token: {description: API token., type: str, required: true, no_log: true}
author: [Platform team (@acme)]
'''
EXAMPLES = r'''
- acme.platform.app_feature: {name: dark_mode, state: enabled, url: https://app.example, token: "{{ app_token }}"}
'''
RETURN = r'''
flag: {description: Resulting flag object., type: dict, returned: always}
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', choices=['enabled', 'disabled'], default='enabled'),
            url=dict(type='str', required=True),
            token=dict(type='str', required=True, no_log=True),
        ),
        supports_check_mode=True,
    )
    p = module.params
    headers = {'Authorization': 'Bearer %s' % p['token'], 'Content-Type': 'application/json'}
    resp, info = fetch_url(module, '%s/api/flags/%s' % (p['url'], p['name']), headers=headers)
    if info['status'] not in (200, 404):
        module.fail_json(msg='GET failed: %s' % info.get('msg'), status=info['status'])
    current = module.from_json(resp.read()) if info['status'] == 200 else {'enabled': False}
    want = p['state'] == 'enabled'
    changed = current.get('enabled') != want
    diff = {'before': {'enabled': current.get('enabled')}, 'after': {'enabled': want}}
    if changed and not module.check_mode:
        resp, info = fetch_url(module, '%s/api/flags/%s' % (p['url'], p['name']), method='PUT',
                               data=module.jsonify({'enabled': want}), headers=headers)
        if info['status'] >= 400:
            module.fail_json(msg='PUT failed: %s' % info.get('body'), status=info['status'])
        current = module.from_json(resp.read())
    module.exit_json(changed=changed, flag=current, diff=diff)

if __name__ == '__main__':
    main()
```
Argument spec extras: `type` (`str`, `int`, `bool`, `list` with `elements`, `dict`, `path`, `raw`,
`jsonarg`), `aliases`, `fallback=(env_fallback, ['APP_TOKEN'])`, `options=` for nested dicts,
`deprecated_aliases`. Module-level constraints: `required_if=[('state','present',['url'])]`,
`required_one_of`, `mutually_exclusive`, `required_together`, `required_by`.

Contract: read current state → compute desired → `changed` only if they differ → act unless
`check_mode` → `exit_json(changed=..., **facts)`; any error → `fail_json(msg=...)`. Never print;
stdout must be the single JSON document. `module.run_command([...], check_rc=True)` for CLIs,
`module.atomic_move`, `module.set_mode_if_different`, `module.add_cleanup_file`, `module.tmpdir`,
`module.warn()` / `module.deprecate()` for advice.

## 3. Test it quickly
```bash
ANSIBLE_LIBRARY=./library ansible -m app_feature -a 'name=x url=https://app.example token=t' localhost
# or directly, skipping Ansible, with an arguments file (/tmp/args.json):
#   {"ANSIBLE_MODULE_ARGS": {"name": "x", "url": "https://app.example", "token": "t"}}
python library/app_feature.py /tmp/args.json
# a module inside a collection:
ansible localhost -m acme.platform.app_feature -a 'name=x url=https://app.example token=t' --playbook-dir=$PWD
```
`ansible-test sanity --test validate-modules` (collection) checks docs match the argument_spec.
Unit tests go under `tests/unit/plugins/` in the collection and run with `ansible-test units`; the developer guide's unit-test page shows replacing `exit_json` / `fail_json` with exceptions and feeding arguments through a `set_module_args` helper.

## 4. Action plugins and Windows
If the work happens on the control node (templating, calling other modules, transferring files),
write an **action plugin** (`plugins/action/<name>.py`, `ActionBase.run`) paired with a module stub
that holds the docs. Windows modules are PowerShell (`<name>.ps1` using `Ansible.Basic` `[Ansible.Basic.AnsibleModule]::Create($args, $spec)`) plus a `<name>.py` docs-only file.

## Gotchas
- Secrets: `no_log=True` on the option *and* do not echo them in `msg`/return values; `module.no_log_values` masks known ones.
- Returning `ansible_facts={...}` sets facts on the host; everything else is available via `register` only.
- A module that always sets `changed=True` breaks handlers and reports; a module that compares server-normalised values to raw input flaps every run — normalise both sides.
- Python on the target: modules run with the target's `ansible_python_interpreter`; avoid third-party imports or guard them with `missing_required_lib`.
- An uncaught exception surfaces as "MODULE FAILURE"; wrap external calls and `fail_json` with a clear `msg`.
- Binary modules (Ansible 2.2+) take arguments and return data the same way as "want JSON" modules (a JSON arguments file in, JSON on stdout) and cannot use `module_utils`; they are not portable across systems.

## Verify
- [ ] `ansible localhost -m <mod> ... -C` reports `changed` without side effects; the real run then reports `changed=true` once and `false` on repeat.
- [ ] `--diff` prints the before/after dict.
- [ ] `ansible-doc -M library <mod>` renders; `ansible-test sanity --test validate-modules` passes.
- [ ] A bad option value fails at argument parsing with a readable message, before any API call.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5 sources.
- Confirmed in module_utils source: `AnsibleModule` methods `exit_json`, `fail_json`, `warn`, `deprecate`, `run_command(check_rc=...)`, `atomic_move`, `set_mode_if_different`, `add_cleanup_file`, `tmpdir`, `jsonify`, `from_json`, `no_log_values`, `missing_required_lib`; argument types `str`, `list`, `dict`, `bool`, `int`, `float`, `path`, `raw`, `jsonarg`/`json`, `bytes`, `bits`; `fetch_url` in `module_utils.urls`.
- Confirmed in the developer guide: `library/` layout, `ANSIBLE_LIBRARY` ad hoc test, the `/tmp/args.json` direct run, collection test with `--playbook-dir`, `required_if`/`required_one_of`/`required_by`/`mutually_exclusive`/`required_together`/`deprecated_aliases`/`env_fallback`, PowerShell `Ansible.Basic` `Create($args, $spec)` and the docs-only `.py` file, `ansible-doc -M`.
- Fixed: the stdin heredoc test and the `-M` option on `ansible` (not documented) were replaced by the documented forms; the `utils` import path for `set_module_args` is not a collection API and was removed.

Method: documentation only; no commands were run.
