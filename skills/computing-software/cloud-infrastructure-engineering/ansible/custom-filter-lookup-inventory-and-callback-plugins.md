---
id: computing-software.cloud-infrastructure-engineering.ansible.custom-filter-lookup-inventory-and-callback-plugins
name: custom-filter-lookup-inventory-and-callback-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, plugin-development, custom-plugins, custom-filters, custom-lookup, filter-plugins, lookup-plugins, inventory-plugins, callback-plugins, test-plugins, vars-plugins, action-plugins, filtermodule, lookupbase, baseinventoryplugin, callbackbase, constructable, cacheable, plugin-paths, ansible-doc-fragments]
level: advanced
status: docs-checked
description: "Write Ansible plugins in Python: filter/test, lookup, inventory (Constructable, Cacheable), callback, plus plugin paths and documentation."
sources: ["Developing plugins (https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html)", "Developing dynamic inventory (https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html)", "Enabling inventory plugins (https://docs.ansible.com/ansible/latest/plugins/inventory.html)", "Callback plugins (https://docs.ansible.com/ansible/latest/plugins/callback.html)", "CallbackBase and CallbackTaskResult source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/callback/__init__.py and https://github.com/ansible/ansible/blob/devel/lib/ansible/executor/task_result.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom filter, lookup, inventory and callback plugins

**Goal:** replace unreadable Jinja chains, bespoke inventory scripts and log scraping
with small, tested Python plugins that run on the control node.

## 1. Where plugins are found
Local: `filter_plugins/`, `lookup_plugins/`, `inventory_plugins/`, `callback_plugins/`,
`test_plugins/`, `action_plugins/`, `vars_plugins/` next to the playbook or inside a role.
Collection: `plugins/filter/`, `plugins/lookup/`, `plugins/inventory/`, `plugins/callback/`,
`plugins/test/`, `plugins/action/`, `plugins/vars/`. Global paths: `[defaults] filter_plugins =`
etc. Give plugins a `DOCUMENTATION` string so `ansible-doc -t <type> name` works. Lookup, inventory, callback and similar plugins use it as their option schema; filter and test plugins do not use the configuration system and (since ansible-core 2.14) treat it as plain documentation.

## 2. Filter and test plugins
```python
# filter_plugins/net.py
from ansible.errors import AnsibleFilterError
def cidr_hosts(cidr, skip=1):
    import ipaddress
    try:
        return [str(h) for h in list(ipaddress.ip_network(cidr).hosts())[skip:]]
    except ValueError as e:
        raise AnsibleFilterError('cidr_hosts: %s' % e)
class FilterModule(object):
    def filters(self):
        return {'cidr_hosts': cidr_hosts}
```
Use: `{{ '10.0.0.0/29' | cidr_hosts(skip=2) }}`. Tests are the same shape with
`class TestModule: def tests(self): return {'private_ip': is_private}` and return bools.
Raise `AnsibleFilterError` for bad input, but let `jinja2.exceptions.UndefinedError` / `AnsibleUndefinedVariable` propagate (re-raise `AnsibleUndefinedVariable`) so undefined variables are only fatal when the value is actually needed.

## 3. Lookup plugins
```python
# lookup_plugins/kv.py
from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
DOCUMENTATION = """
name: kv
short_description: read keys from an internal KV service
options:
  _terms: {description: keys, required: true}
  url: {description: base url, type: str, env: [{name: KV_URL}], ini: [{section: kv, key: url}], required: true}
"""
class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        url = self.get_option('url')
        out = []
        for t in terms:
            out.append(self._fetch(url, t))   # your HTTP call; raise AnsibleError on failure
        return out                            # always a list
```
Use: `{{ lookup('kv', 'db/password', url='https://kv.example') }}` or `query('kv', ...)`.
Options declared in DOCUMENTATION are resolved from env, ini, vars and keyword arguments by `set_options`.

## 4. Inventory plugins
```python
# inventory_plugins/cmdb.py
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
DOCUMENTATION = """
name: cmdb
plugin_type: inventory
short_description: hosts from the CMDB API
extends_documentation_fragment: [constructed, inventory_cache]
options:
  plugin: {description: token, required: true, choices: [cmdb, acme.platform.cmdb]}
  url: {type: str, required: true}
"""
class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = 'cmdb'
    def verify_file(self, path):
        return super().verify_file(path) and path.endswith(('cmdb.yml', 'cmdb.yaml'))
    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path, cache)
        self._read_config_data(path)
        key = self.get_cache_key(path)
        data = self._cache.get(key) if cache and self.get_option('cache') else None
        if data is None:
            data = self._query(self.get_option('url'))     # list of dicts
            self._cache[key] = data
        strict = self.get_option('strict')
        for h in data:
            self.inventory.add_host(h['name'])
            self.inventory.set_variable(h['name'], 'ansible_host', h['ip'])
            self.inventory.add_group(h['env']); self.inventory.add_child(h['env'], h['name'])
            self._set_composite_vars(self.get_option('compose'), h, h['name'], strict)
            self._add_host_to_composed_groups(self.get_option('groups'), h, h['name'], strict)
            self._add_host_to_keyed_groups(self.get_option('keyed_groups'), h, h['name'], strict)
```
Enable with `[inventory] enable_plugins = cmdb, yaml, ini` (local) and an inventory file
`inventories/prod/cmdb.yml` containing `plugin: cmdb`. Mixing in `Constructable` gives users
`compose`/`groups`/`keyed_groups` for free; `Cacheable` gives `cache`/`cache_plugin`/`cache_timeout`.
Debug with `ansible-inventory -i inventories/prod/cmdb.yml --graph -vvv`.

## 5. Callback plugins
```python
# callback_plugins/slack_summary.py
from ansible.plugins.callback import CallbackBase
class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'     # 'stdout' marks the plugin that renders screen output
    CALLBACK_NAME = 'slack_summary'
    CALLBACK_NEEDS_ENABLED = True
    def __init__(self):
        super().__init__()
        self.failed = []
    def v2_runner_on_failed(self, result, ignore_errors=False):
        # result.host, result.task, result.result exist from ansible-core 2.19;
        # older releases used result._host, result._task, result._result
        self.failed.append((result.host.get_name(), result.task.get_name(), result.result.get('msg')))
    def v2_playbook_on_stats(self, stats):
        ...  # post summary; use self._display.display() for console
```
Enable: `callbacks_enabled = slack_summary` (notification/aggregate) or `stdout_callback = name`.
Hooks: `v2_playbook_on_start`, `v2_playbook_on_task_start`, `v2_runner_on_ok/failed/skipped/unreachable`,
`v2_runner_item_on_*`, `v2_playbook_on_stats`. Do not log results of `no_log` tasks (from ansible-core 2.22, registered secrets in `result.result` are masked before a callback receives them).
Options declared in `DOCUMENTATION` are read with `self.get_option()`; the engine calls `set_options()` for callback plugins.

## Gotchas
- Plugins run on the control node with the control node's Python; dependencies go in the EE/venv, not on targets.
- Filters and tests that ship in a collection are called by FQCN (`acme.platform.cidr_hosts`).
- An inventory plugin that `auto` does not pick up must be listed in `[inventory] enable_plugins` (short name for a local plugin, FQCN for one in a collection).
- `CALLBACK_TYPE = 'stdout'` plugins: only one can be active; use `aggregate`/`notification` to coexist with `default`.
- Lookup plugins are expected to return a list, even for a single element.

## Verify
- [ ] `ansible-doc -t filter|lookup|inventory|callback <name>` renders the DOCUMENTATION.
- [ ] `ansible localhost -m debug -a "msg={{ ... | your_filter }}"` works and a bad input yields your `AnsibleFilterError` text.
- [ ] `ansible-inventory --graph` with the plugin shows hosts/groups; a second run with `cache: true` is faster and hits the cache file.
- [ ] A failing task triggers the callback once per host and secrets from `no_log` tasks do not appear in its output.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5 sources.
- Confirmed: plugin directory and path settings; filter and test plugins use documentation only (since 2.14) and should propagate undefined-variable errors; lookups return lists and call `set_options` before `get_option`; inventory plugin methods `verify_file`, `parse`, `_read_config_data`, `get_cache_key`, `_set_composite_vars`, `_add_host_to_composed_groups`, `_add_host_to_keyed_groups` and the `constructed` / `inventory_cache` fragments; `enable_plugins` handling; callback attributes (`CALLBACK_VERSION`, `CALLBACK_TYPE`, `CALLBACK_NAME`, `CALLBACK_NEEDS_ENABLED`), `callbacks_enabled` and `stdout_callback`, and the `v2_*` hook names.
- Fixed: the callback example used `result._host` / `result._task` / `result._result` and an uninitialised `self.failed`; current ansible-core exposes `result.host`, `result.task`, `result.result` (the underscore names remain for compatibility with a deprecation marked for core 2.23).
- Removed as unconfirmed: the sanity-test requirement, silent skipping of broken plugin files, filter-name uniqueness claim and the `self._display` caching remark.

Method: documentation only; no commands were run.
