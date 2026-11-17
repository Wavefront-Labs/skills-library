---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-test-sanity-units-and-integration
name: ansible-test-sanity-units-and-integration
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-test, sanity-tests, unit-tests, integration-tests-collections, validate-modules, pep8, pylint, docker-default, test-targets, integration-config, tests-sanity-ignore, coverage, pytest, collection-ci, github-actions-ansible, ansible-test-matrix, changelog-lint]
level: advanced
status: docs-checked
description: "Test an Ansible collection with ansible-test: sanity (validate-modules, pep8) in the default docker image, pytest unit tests, integration targets with aliases, CI matrix."
sources: ["Ansible developer guide, testing collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_testing.html)", "Ansible developer guide, sanity test ignores (https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/ignores.html)", "Ansible developer guide, integration test aliases (https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/integration-aliases.html)", "ansible-community/ansible-test-gh-action (https://github.com/ansible-community/ansible-test-gh-action)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ansible-test: sanity, units and integration

**Goal:** a collection that passes the checks the community runs, so a bad module never reaches a consumer.

## 1. Layout the tool expects
Run `ansible-test` from the collection root; the path must end in `ansible_collections/<ns>/<name>`. Inside:
```
tests/sanity/ignore-X.Y.txt       # one file per ansible-core release X.Y (last resort)
tests/unit/plugins/modules/test_app_feature.py
tests/unit/requirements.txt
tests/integration/targets/app_feature/tasks/main.yml
tests/integration/targets/app_feature/aliases
```

## 2. Sanity
```bash
ansible-test sanity --docker default -v                 # all tests in the default container
ansible-test sanity --docker default --test validate-modules --test pep8 plugins/modules/app_feature.py
ansible-test sanity --venv --python 3.12                # no container
```
Among the sanity tests: `validate-modules`, `pep8`, `pylint`, `yamllint`, `shebang`, `boilerplate`, `compile`, `import`, `ansible-doc`, `changelog`, `runtime-metadata`. See the sanity test reference for what each checks and how to fix it.

Ignore files hold one entry per line: file path, a space, the test name (with `:code` for tests that use error codes, and a Python version suffix such as `-3.8` where the test is version-specific), and an optional `# comment`:
```
plugins/modules/my_module.py validate-modules:missing-gplv3-license # reason
plugins/module_utils/my_util.py validate-modules!skip # waiting for bug fix
```
Fix the code instead of ignoring where possible: new content should not use ignores. An ignore for an error that no longer occurs is itself reported as an error. Collections need a separate `ignore-X.Y.txt` for each ansible-core release they are tested against.

## 3. Unit tests
Unit tests live under `tests/unit/plugins/` and are driven by pytest. Run them with:
```bash
ansible-test units --docker default -v
ansible-test units --docker default -v --python 3.13
ansible-test units --docker default -v --python 3.13 tests/unit/plugins/module_utils/foo/test_bar.py
```
ansible-core ships `ansible.module_utils.testing.patch_module_args`, a context manager that exposes arguments to `AnsibleModule`; `AnsibleModule.exit_json` and `fail_json` end with `sys.exit`:
```python
import pytest
from ansible.module_utils.testing import patch_module_args
from ansible_collections.acme.platform.plugins.modules import app_feature

def test_missing_required_option_exits():
    with patch_module_args({"name": "x"}):
        with pytest.raises(SystemExit):
            app_feature.main()
```
Check that your minimum supported ansible-core release includes `ansible.module_utils.testing`. Unit tests run with network isolation in containers; add Python requirements to `tests/unit/requirements.txt`.

## 4. Integration tests
```yaml
# tests/integration/targets/app_feature/aliases
unsupported   # cannot run in CI; or a group such as shippable/posix/group1
# tests/integration/targets/app_feature/tasks/main.yml
- block:
    - acme.platform.app_feature: {name: it_flag, state: enabled}
      register: r1
    - ansible.builtin.assert: {that: [r1 is changed]}
    - acme.platform.app_feature: {name: it_flag, state: enabled}
      register: r2
    - ansible.builtin.assert: {that: [r2 is not changed]}
  always:
    - acme.platform.app_feature: {name: it_flag, state: disabled}
```
Every target needs an `aliases` file. Run: `ansible-test integration app_feature --docker default -v`, add `--retry-on-error` to re-run failures with higher verbosity, and use `--list-targets` to list targets. Target names are directory names under `tests/integration/targets/`. Running integration tests in containers is recommended because tests can install packages and start services. A good target proves create, idempotent re-run, check mode and delete.

## 5. CI
```yaml
# .github/workflows/ci.yml (ansible-community/ansible-test-gh-action)
- uses: ansible-community/ansible-test-gh-action@release/v1
  with: {ansible-core-version: stable-2.21, testing-type: sanity}
- uses: ansible-community/ansible-test-gh-action@release/v1
  with: {ansible-core-version: stable-2.21, testing-type: units, target-python-version: "3.12"}
```
Matrix over the ansible-core versions your collection supports plus `devel`; the action's `ansible-core-version` input takes values such as `stable-2.21` or `devel`. Add `ansible-lint --profile production` as a separate job.

## Gotchas
- `ansible-test` is provided by both the `ansible` and `ansible-core` packages; always run it from the collection root.
- Dependencies of your collection must be in the same collection root; ansible-test ignores your configured collection paths.
- Files ignored by git are ignored by ansible-test.
- Every integration target needs `aliases`; aliases are one per line and a target belongs in exactly one group.

## Verify
- [ ] `ansible-test sanity --docker default` and `ansible-test units --docker default` exit 0 with only ignore entries you can justify.
- [ ] `ansible-test integration <target>` passes the create, re-run, check-mode and delete sequence.

## Checked
Checked 2026-10-23 against the Ansible developer guide source (developing_collections_testing.rst, testing_units.rst, sanity/ignores.rst, sanity/boilerplate.rst, sanity/integration-aliases.rst), the ansible-core source (lib/ansible/module_utils/testing.py and basic.py; latest release v2.21.5) and the ansible-test-gh-action README (latest release v1.18.0): command lines, the collection root requirement, ignore file naming and format (including `!skip`), the `boilerplate` sanity test replacing the older future-import and metaclass tests, `patch_module_args`, `--retry-on-error`, `--list-targets`, the aliases requirement and the action's inputs. Removed the unconfirmed `ModuleTestCase`/`set_module_args` helper imports (not present in community.general's current unit test utilities), `integration_config.yml` template and `tests/requirements.yml` claims, `cloud/acme` and `context/target` aliases, `pipx` install advice, validate-modules error-text claims and the stable-2.15 to 2.17 matrix.
Method: documentation only; no commands were run.
