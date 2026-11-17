---
id: computing-software.cloud-infrastructure-engineering.ansible.writing-a-custom-cache-plugin
name: writing-a-custom-cache-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, plugin-development, custom-cache-plugin, fact-caching, inventory-cache, basecachemodule, basefilecachemodule]
level: sme
status: docs-checked
description: "Write a cache plugin for fact and inventory caching backed by your own store: BaseCacheModule or BaseFileCacheModule, options, timeouts, and how to enable and test it."
sources: ["Cache plugins (https://docs.ansible.com/ansible/latest/plugins/cache.html)", "Developing plugins, cache plugins (https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html)", "BaseCacheModule and BaseFileCacheModule source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/cache/__init__.py)", "jsonfile cache plugin source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/cache/jsonfile.py)", "inventory_cache doc fragment (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/doc_fragments/inventory_cache.py)", "Configuration settings source (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a custom cache plugin

Goal: store gathered facts and inventory-plugin results in a backend your platform already runs
(an internal KV store, S3-compatible bucket, Postgres) when `jsonfile`, `redis`, `memcached`
or `mongodb` do not fit. Check `community.general` first.

## File-based store: subclass BaseFileCacheModule
Gets `_timeout`, `_prefix`, key-to-file mapping, expiry checks and atomic writes (temporary file, then rename) for free; you implement the two abstract methods `_load(filepath)` and `_dump(value, filepath)`. The built-in `jsonfile` plugin is the reference implementation.
`plugins/cache/gzjsonfile.py`:
```python
from __future__ import annotations
DOCUMENTATION = r"""
name: gzjsonfile
short_description: gzip-compressed JSON files cache
description: [Facts/inventory cached as gzip-compressed JSON files.]
options:
  _uri:
    required: true
    description: Directory to store the cache in.
    env: [{name: ANSIBLE_CACHE_PLUGIN_CONNECTION}]
    ini: [{key: fact_caching_connection, section: defaults}]
    type: path
  _prefix:
    description: File name prefix.
    env: [{name: ANSIBLE_CACHE_PLUGIN_PREFIX}]
    ini: [{key: fact_caching_prefix, section: defaults}]
  _timeout:
    default: 86400
    description: Expiry in seconds, 0 = never.
    env: [{name: ANSIBLE_CACHE_PLUGIN_TIMEOUT}]
    ini: [{key: fact_caching_timeout, section: defaults}]
    type: integer
"""
import gzip
import json
from ansible.plugins.cache import BaseFileCacheModule

class CacheModule(BaseFileCacheModule):
    def _load(self, filepath):
        with gzip.open(filepath, "rt", encoding="utf-8") as f:
            return json.load(f)

    def _dump(self, value, filepath):
        with gzip.open(filepath, "wt", encoding="utf-8") as f:
            json.dump(value, f)
```

## Network store: subclass BaseCacheModule
Implement the abstract interface: `get(key)`, `set(key, value)`, `keys()`, `contains(key)`,
`delete(key)`, `flush()`. The base `__init__` calls `set_options`, so read options such as
`self.get_option('_uri')` after `super().__init__(*args, **kwargs)`. Store an expiry timestamp
with each value and treat expired entries as missing in `get`/`contains` (the file-based
class raises `KeyError` from `get` for a missing or expired key). Set `_persistent = False` on
a plugin that does not persist data between runs.

## Enable it
```ini
[defaults]
gathering = smart
fact_caching = acme.platform.gzjsonfile
fact_caching_connection = ~/.cache/ansible-facts
fact_caching_timeout = 7200
```
Inventory plugins with `cache: true` can use it via `cache_plugin: acme.platform.gzjsonfile`
and `cache_connection:` in the inventory source YAML.

## Gotchas
- Multiple concurrent `ansible-playbook` runs share the cache; the file-based base class writes atomically, a network store must make `set` safe itself.
- The cache stores whatever facts were gathered, including secrets in custom facts; protect the store accordingly.
- `ansible-playbook --flush-cache` clears the fact cache for every host in inventory; implement `flush()` and `delete()` properly or stale facts never clear.

## Verify
- [ ] `ansible-doc -t cache acme.platform.gzjsonfile` renders.
- [ ] Run `ansible all -m setup` then a play with `gather_facts: false` using `{{ ansible_facts.hostname }}` — it resolves from cache; after `fact_caching_timeout` it does not.

## Checked

Checked 2026-10-26 against ansible-core 2.21.5 sources (devel, 2026-10-23) and ansible-documentation main (2026-10-21).
- Confirmed in `plugins/cache/__init__.py`: the abstract methods are `get`, `set`, `keys`, `contains`, `delete`, `flush` (there is no `copy()`); `BaseFileCacheModule` requires `_load` and `_dump`, reads `_uri` and `_timeout`, writes through a temporary file and `os.rename`, and raises `KeyError` for missing or expired keys.
- Confirmed in `jsonfile.py`: option names and ini/env keys (`fact_caching_connection`, `fact_caching_prefix`, `fact_caching_timeout`, `ANSIBLE_CACHE_PLUGIN_*`), default timeout 86400, plain `json` in `_load`/`_dump`; `gathering` values and `inventory_cache` options (`cache`, `cache_plugin`, `cache_timeout`, `cache_connection`, `cache_prefix`).
- Replaced: the third-party `msgpack` example (not checkable here) with a standard-library gzip plus JSON one; removed the `copy()` method and the `AnsibleJSONEncoder` advice, which current core does not use in its own file cache.

Method: documentation only; no commands were run.
