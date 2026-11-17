---
id: computing-software.cloud-infrastructure-engineering.ansible.writing-custom-ansible-lint-rules
name: writing-custom-ansible-lint-rules
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-lint, custom-lint-rules, ansiblelintrule, rulesdir, matchtask, policy-enforcement, internal-standards]
level: advanced
status: docs-checked
description: "Encode team standards as custom ansible-lint rules: AnsibleLintRule subclasses with matchtask/matchyaml, loading via rulesdir, testing with fixtures, and shipping them as a package."
sources: ["ansible-lint custom rules (https://ansible.readthedocs.io/projects/lint/custom-rules/)", "ansible-lint example rule (https://github.com/ansible/ansible-lint/blob/main/examples/rules/task_has_tag.py)", "ansible-lint configuration (https://ansible.readthedocs.io/projects/lint/configuring/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing custom ansible-lint rules

Goal: internal rules ("no `shell` without `changed_when`", "every `uri` must set `timeout`",
"no hosts: all in site playbooks") fail CI the same way built-in rules do.

## A task rule
`lint_rules/uri_timeout.py`:
```python
from __future__ import annotations
from typing import TYPE_CHECKING
from ansiblelint.rules import AnsibleLintRule

if TYPE_CHECKING:
    from ansiblelint.file_utils import Lintable
    from ansiblelint.utils import Task

class UriTimeoutRule(AnsibleLintRule):
    id = "acme-uri-timeout"
    description = "uri/get_url tasks must set an explicit timeout to avoid hanging jobs."
    tags = ["acme", "reliability"]

    def matchtask(self, task: Task, file: Lintable | None = None) -> bool | str:
        if task["action"]["__ansible_module__"] in ("ansible.builtin.uri", "uri", "ansible.builtin.get_url", "get_url"):
            if "timeout" not in task["action"]:
                return "uri/get_url without timeout"
        return False
```
- `matchtask` receives a normalised task: `task["action"]` holds the module and its arguments, and keywords such as `when` are keys on the task. The built-in example rule (`examples/rules/task_has_tag.py` in the ansible-lint repository) uses the same signature.
- Return `True` or a message string to report a match, `False` or `None` for no match.

## Other hooks
- `match(self, line)` runs on each line and returns `True`, a message string, or `None`/`False`.
- Other hooks (`matchplay`, `matchyaml`) exist in the `AnsibleLintRule` base class; read the ansible-lint source for their signatures before relying on them.

## Load them
```yaml
# .ansible-lint
rulesdir: [./lint_rules]
use_default_rules: true      # keep the built-in rules alongside your own
```
CLI equivalent: `ansible-lint -r ./lint_rules -R` (`-R` keeps the default rules when `-r` is used). Suppress like any rule: `# noqa: acme-uri-timeout`.

## Test them
Keep a sample playbook that violates the rule and run ansible-lint with `-r ./lint_rules` against it in CI; the run must report the custom rule id. (The Python `Runner` API used by ansible-lint's own tests is internal and not documented, so this skill does not rely on it.)

## Share across repos
Vendor a `lint_rules/` directory (for example a git submodule) and point `rulesdir` at it. The ansible-lint docs also describe packaging rules as a Python package installed under the `ansiblelint/rules/custom/<name>/` directory so they load automatically. Pin ansible-lint, because the rule API is internal.

## Gotchas
- Each rule needs a unique `id`, a `description` and `tags`; prefix ids with your organisation to avoid collisions with built-ins.
- `matchtask` sees tasks after ansible-lint normalises them, so check arguments rather than raw text.
- Guard optional keys with `.get()` so an exception in a rule does not hide real findings.

## Verify
- [ ] `ansible-lint -r ./lint_rules -R -L` lists the custom rule ids.
- [ ] A sample violating playbook fails CI with the custom rule id.

## Checked
Checked 2026-10-23 against the ansible-lint documentation source and repository (latest release v26.10.1): the required rule attributes (id, description, tags), `match` and `matchtask` signatures from the documented example and examples/rules/task_has_tag.py, the `rulesdir` and `use_default_rules` options in the sample .ansible-lint, and the `-r`/`-R`/`-L` flags in cli.py. Removed the unconfirmed `severity`, `version_added`, `create_matcherror`, `matchlines`, the Runner-based unit test, the `internal-error` claim and the claim that custom rules must be added to `enable_list`.
Method: documentation only; no commands were run.
