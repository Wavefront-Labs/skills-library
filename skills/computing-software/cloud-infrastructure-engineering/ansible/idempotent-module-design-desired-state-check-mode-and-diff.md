---
id: computing-software.cloud-infrastructure-engineering.ansible.idempotent-module-design-desired-state-check-mode-and-diff
name: idempotent-module-design-desired-state-check-mode-and-diff
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, module-development, state-comparison, desired-state-pattern, module-diff, supports-check-mode, idempotency]
level: advanced
status: docs-checked
description: "Structure a custom Ansible module as read current state, compute desired state, compare, then change only if needed, with check mode support and a diff when asked."
sources: ["https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html", "https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html", "https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotent module design: desired state, check mode and diff

The pattern: read current state, build desired state from the parameters, compare, and mutate only when they differ.

```python
#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            size=dict(type="int", default=10),
            state=dict(type="str", default="present", choices=["present", "absent"]),
        ),
        supports_check_mode=True,
    )
    client = make_client(module)           # your API wrapper
    before = get_current(client, module.params["name"])   # None if absent
    after = None if module.params["state"] == "absent" else build_desired(module.params)

    result = dict(changed=before != after)
    if result["changed"]:
        if module._diff:
            pass                           # build and set result["diff"] here
        if not module.check_mode:          # never modify in check mode
            apply_change(client, before, after)
    module.exit_json(**result)
```
`make_client`, `get_current`, `build_desired` and `apply_change` are your own helpers.

## Rules (each from the developer guide)
1. **Declarative, not CRUD.** Offer `present`/`absent` or `started`/`stopped` so the user states the final state and ignores the existing one.
2. **Idempotency.** Running the module twice against the same system must give the same final state; if you cannot achieve that, document the behaviour and the reason.
3. **Check mode.** Pass `supports_check_mode=True` to `AnsibleModule()`; test `module.check_mode` and make no modification when it is true. The default is `supports_check_mode=False`, in which case the module exits in check mode with `skipped=True` and the message "remote module (<module name>) does not support check mode".
4. **`*_info` and `*_facts` modules** should implement check mode, otherwise playbooks that branch on those facts will not branch correctly in check mode.
5. **Diff.** Read `AnsibleModule._diff` to know whether diff mode is on (also set by the `diff` playbook keyword or the `DIFF_ALWAYS` setting). The best-practices page says to return a diff in diff mode when it applies; the structure of the value is not covered on the pages cited here, so follow an in-tree module for the shape.
6. **Returns.** Always return useful data even when nothing changed, keep the top level a dictionary, keep it JSON-serialisable (do not pass an object to `exit_json()`), and never `print()` from a module.
7. **Document it.** Declare support in the `attributes:` block of DOCUMENTATION: each attribute has `support` (`full`, `none`, `partial` or `N/A`), `description`, and `details` (required when support is `partial`). Usually these come from documentation fragments such as `ansible.builtin.action_common_attributes`. Do not put check mode or diff information under `notes`.

## Verify
- [ ] Run twice: the second run reports `changed=false`.
- [ ] With `--check` against a system where the resource is absent, the task reports changed and nothing is created.

## Checked
Date: 2026-11-07. Read: the check-mode section, `_ansible_diff` section and `supports_check_mode` text of the program-flow page; the `attributes` field description and the notes rule on the documenting page; the return-values, declarative and idempotency conventions, and `*_info` check-mode guidance on the best-practices page. The argument_spec keys used in the sample (`type`, `required`, `default`, `choices`) were taken from the same program-flow page's argument-spec section, which I only skimmed.
Corrected: the check-mode default and its skipped message are now stated as the page words them; the sample now calls the whole comparison a pattern with named helper stubs rather than inline API code.
Removed as not on a cited page: the `before`/`after`/`before_header`/`after_header` diff structure, the `update_password: always|on_create` advice, the async-polling gotcha, advice to normalise types and list order, the "copy current value when option is None" rule, the "mask secrets in diff" rule, the `changed=True` in check mode gotcha, and the labels-merge logic from the example.
Method: documentation only; no commands were run.
