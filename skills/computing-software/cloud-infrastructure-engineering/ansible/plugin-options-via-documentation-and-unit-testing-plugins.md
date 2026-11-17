---
id: computing-software.cloud-infrastructure-engineering.ansible.plugin-options-via-documentation-and-unit-testing-plugins
name: plugin-options-via-documentation-and-unit-testing-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, plugin-development, plugin-options, plugin-configuration, plugin-tests, get-option, ansible-test-units]
level: advanced
status: docs-checked
description: "Declare plugin options in DOCUMENTATION with ini, env and vars sources, read them with get_option, and unit test plugins with pytest and ansible-test units."
sources: ["Developing plugins, configuration fields (https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html)", "Testing collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_testing.html)", "Unit testing Ansible modules (https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html)", "ansible-test sanity tests (https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/index.html)", "Configuration manager source, value precedence (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/manager.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin options via DOCUMENTATION, and unit testing plugins

## Options are defined by the docs
For lookup, inventory, callback, connection, become, cache, vars plugins, the `DOCUMENTATION`
YAML is parsed and becomes the config schema:
```python
DOCUMENTATION = r"""
name: cmdb
author: Platform Team
short_description: Look up hosts in the CMDB
description: Returns records from the CMDB API.
options:
  _terms:
    description: Query strings.
    required: true
  url:
    description: CMDB base URL.
    type: string
    required: true
    env: [{name: CMDB_URL}]
    ini: [{section: cmdb_lookup, key: url}]
    vars: [{name: cmdb_url}]
  timeout:
    type: integer
    default: 10
  validate_certs:
    type: boolean
    default: true
"""
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        url = self.get_option("url")
        timeout = self.get_option("timeout")
        return [self._query(url, t, timeout) for t in terms]
```
Precedence (low → high): default, ini (`ansible.cfg`), env, vars (`vars:` sources, where the plugin type supports them), direct (keyword arguments in the lookup call); playbook keywords and CLI options sit between vars and env when a plugin documents them. Within one source the last entry listed wins. Option `type` values are `boolean`, `float`, `integer`, `list`, `none`, `path`, `pathlist`, `pathspec`, `string`, `tmppath`. `ansible-doc -t lookup acme.cmdb.cmdb` shows every source.

Inventory plugins: `self._read_config_data(path)` then `self.get_option(...)`; use the
`Constructable` and `Cacheable` base classes with the `constructed` and `inventory_cache` doc fragments (`extends_documentation_fragment: [constructed, inventory_cache]`).

## Unit tests
Layout inside a collection: `tests/unit/plugins/lookup/test_cmdb.py`.
```python
import pytest
from ansible.plugins.loader import lookup_loader

def test_lookup_returns_records(mocker):
    lookup = lookup_loader.get("acme.cmdb.cmdb")
    mocker.patch.object(lookup, "_query", return_value={"name": "web1"})
    assert lookup.run(["web1"], variables={}, url="https://cmdb") == [{"name": "web1"}]

def test_missing_url_raises():
    lookup = lookup_loader.get("acme.cmdb.cmdb")
    with pytest.raises(Exception):
        lookup.run(["x"], variables={})
```
Filters are plain functions — test them directly: `from ansible_collections.acme.cmdb.plugins.filter.net import to_cidr`.

Run:
```bash
cd ansible_collections/acme/cmdb
ansible-test units --docker default -v                 # all supported Python versions
ansible-test units --docker default -v --python 3.13 tests/unit/plugins/lookup/test_cmdb.py
```
Put extra test dependencies (for example pytest-mock for the `mocker` fixture) in `tests/unit/requirements.txt`.

## Gotchas
- `lookup_loader.get` requires the collection to be importable: the repo must sit at `ansible_collections/<ns>/<name>/`.
- `set_options` must be called before `get_option`, otherwise options are unset.

## Verify
- [ ] `ansible-test sanity --docker default -v` (which includes the `ansible-doc` and `yamllint` tests) passes on the DOCUMENTATION blocks.
- [ ] `ansible-test units` green on all supported Python versions.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5 sources.
- Confirmed: plugin option fields (`env`, `ini`, `vars`, `type`, `required`, `secret`) and the documented `type` names; the precedence order in `get_config_value_and_origin` (direct, vars, keywords, CLI, env, ini, default); unit tests belong under `tests/unit/plugins/`; `ansible-test units --docker default -v [--python 3.13] [path]`; `tests/unit/requirements.txt`; the `ansible-doc` and `yamllint` sanity tests exist.
- Fixed: example option types used `str`/`int`/`bool`, while the documented names are `string`/`integer`/`boolean`; `--venv` was dropped because the docs only show `--docker`; the coercion remark was removed as unconfirmed.

Method: documentation only; no commands were run.
