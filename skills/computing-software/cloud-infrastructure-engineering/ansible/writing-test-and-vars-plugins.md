---
id: computing-software.cloud-infrastructure-engineering.ansible.writing-test-and-vars-plugins
name: writing-test-and-vars-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, plugin-development, test-plugin, custom-vars-plugin, custom-plugins]
level: advanced
status: docs-checked
description: "Write Jinja test plugins with TestModule and vars plugins with BaseVarsPlugin, place them in collections, document them, and control vars plugin stage and enablement."
sources: ["Developing plugins, test and vars plugins (https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html)", "Vars plugins (https://docs.ansible.com/ansible/latest/plugins/vars.html)", "Documenting modules and plugins (https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html)", "vars_plugin_staging doc fragment (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/doc_fragments/vars_plugin_staging.py)", "host_group_vars vars plugin source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/vars/host_group_vars.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Test plugins and vars plugins

## Test plugin
```python
# plugins/test/semver.py  (in collection acme.platform)
import re

SEMVER = re.compile(r'^v?\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$')

def is_semver(value):
    return isinstance(value, str) and bool(SEMVER.match(value))

class TestModule(object):
    def tests(self):
        return {'semver': is_semver}
```
Usage: `when: release is acme.platform.semver`. Document it inline with `DOCUMENTATION` or with an adjacent YAML documentation file (supported for filter and test plugins since ansible-core 2.14), then check with `ansible-doc -t test acme.platform.semver`. Test plugins do not use the configuration system and should propagate `jinja2.exceptions.UndefinedError` / `AnsibleUndefinedVariable` so undefined variables are only fatal when needed.

## Vars plugin
Vars plugins inject variable data that did not come from an inventory source, playbook or the command line; `group_vars` and `host_vars` themselves work through the `host_group_vars` vars plugin.
```python
# plugins/vars/cmdb_vars.py
DOCUMENTATION = '''
    name: cmdb_vars
    short_description: Load host vars from a CMDB export
    options:
      stage:
        ini: [{key: stage, section: vars_cmdb_vars}]
        env: [{name: ANSIBLE_VARS_PLUGIN_STAGE}]
    extends_documentation_fragment: [vars_plugin_staging]
'''
import json, os
from ansible.plugins.vars import BaseVarsPlugin
from ansible.inventory.host import Host

class VarsModule(BaseVarsPlugin):
    REQUIRES_ENABLED = True
    def get_vars(self, loader, path, entities):
        super().get_vars(loader, path, entities)
        data = json.load(open(os.path.join(path, 'cmdb.json')))
        result = {}
        for e in entities:
            if isinstance(e, Host):
                result.update(data.get(e.name, {}))
        return result
```
Enable: `[defaults] vars_plugins_enabled = host_group_vars,acme.platform.cmdb_vars`. The `vars_plugin_staging` fragment adds a `stage` option (`all`, `task` or `inventory`) that decides when the plugin runs; if it is unset the global `run_vars_plugins` setting applies (default `demand`). The ini section for the option is whatever the plugin documents; the developer guide uses `vars_<plugin name>`. Wrap values that may contain template-like text with `ansible.utils.unsafe_proxy.wrap_var`.

## Gotchas
- `get_vars` is called at least once per inventory source path and the playbook directory, so cache expensive I/O.
- Vars plugins that live in a collection must be enabled by the user with `vars_plugins_enabled`; legacy vars plugins always run unless they set `REQUIRES_ENABLED = True`.
- `ansible-inventory` ignores the `stage` and `run_vars_plugins` settings and always loads vars plugins.

## Verify
```bash
ansible-doc -t test acme.platform.semver
ansible-inventory --host web01
```

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5 sources.
- Confirmed: `vars_plugins_enabled` and collection vars plugins needing explicit enabling; `REQUIRES_ENABLED`; the `get_vars(self, loader, path, entities)` signature; the `vars_plugin_staging` fragment and its `stage` choices (`all`, `task`, `inventory`); `RUN_VARS_PLUGINS` (`run_vars_plugins`, default `demand`); the documented ini section pattern `vars_<plugin>`; `ansible-inventory` always loads vars plugins; `wrap_var` for unsafe values; test plugins are documentation-only since 2.14.
- Fixed: the example's ini section was a collection name (the docs use `vars_<name>`), the example's extra optional `cache` parameter was dropped to match the documented `get_vars(self, loader, path, entities)` signature (the built-in host_group_vars plugin does accept it), and an unused import was removed.
- Removed as unconfirmed: the test-name collision remark and the `jq` pipeline.

Method: documentation only; no commands were run.
