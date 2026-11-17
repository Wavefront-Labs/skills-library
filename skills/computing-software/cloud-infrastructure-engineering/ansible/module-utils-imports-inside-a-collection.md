---
id: computing-software.cloud-infrastructure-engineering.ansible.module-utils-imports-inside-a-collection
name: module-utils-imports-inside-a-collection
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collection-development, collection-module-utils, collection-imports, module-utils, relative-imports, ansiballz, plugin-imports]
level: advanced
status: docs-checked
description: "Share code between modules and plugins in a collection through plugins/module_utils with correct absolute or relative imports that survive AnsiballZ packaging and ansible-test."
sources: ["Collection structure, module_utils (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)", "Using and developing module utilities (https://docs.ansible.com/ansible/latest/dev_guide/developing_module_utilities.html)", "ansible-test import sanity test (https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/import.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# module_utils imports inside a collection

Goal: one shared client/helper in `plugins/module_utils/` used by many modules and plugins,
imported in a way the module packager (AnsiballZ) can find and ship to the target.

## Layout
```
ansible_collections/acme/platform/plugins/
  module_utils/
    api_client.py
    _version.py
  modules/
    app_user.py
  lookup/
    app_secret.py
```

## In modules
Import with the FQCN and the `ansible_collections` convention:
```python
from ansible_collections.acme.platform.plugins.module_utils.api_client import ApiClient
```
The `ansible.module_utils` namespace is constructed dynamically for each task invocation by extracting imports from the module and resolving them, so the helpers a module imports are shipped with it. Modules may only import from `ansible.module_utils.*` (the rest of the `ansible` package is not guaranteed on the target). Importing something from an `__init__.py` requires using the file name in the path.

## From another collection
```python
from ansible_collections.community.general.plugins.module_utils.version import LooseVersion
```
Add that collection to `dependencies` in `galaxy.yml`, or the import fails on users' machines.

## In controller-side plugins (lookup, filter, action, inventory)
They run on the control node and can import anything installed there. `module_utils` is usable not only by modules but by most plugins, through its FQCN, which lets you distribute modules, lookups and filters without importing a role in every play.

## Third-party Python dependencies
```python
import traceback
from ansible.module_utils.basic import missing_required_lib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    REQUESTS_IMP_ERR = traceback.format_exc()
...
if not HAS_REQUESTS:
    module.fail_json(msg=missing_required_lib("requests"), exception=REQUESTS_IMP_ERR)
```
The `ansible-test` sanity `import` test requires non-core imports in modules and plugins to be guarded (handled import errors) so users get an actionable message.

## Gotchas
- Use the full `ansible_collections.<ns>.<collection>.plugins.module_utils...` path for collection code; the short `ansible.module_utils.x` namespace is for core and local `module_utils` directories.
- module_utils must run on the target's Python; do not use controller-only syntax or libraries there.
- Changing a module_utils signature affects every module using it; run `ansible-test units` and `integration` across all dependants before release.

## Verify
- [ ] `ansible-test sanity --test import --docker default` passes.
- [ ] A module run on a managed host succeeds and imports the helper from the collection path.

## Checked

Checked 2026-10-26 against the Ansible developer documentation (collection structure `module_utils` section, module utilities guide, `import` sanity test and best practices for `missing_required_lib`). Confirmed: FQCN import convention, dynamic construction of the `ansible.module_utils` namespace per task, the `__init__.py` note, `module_utils` use by plugins, guarded third-party imports with `missing_required_lib`. Removed unconfirmed relative import, version gate, static import limitation, `plugin_utils`, circular import and `ANSIBLE_KEEP_REMOTE_FILES` claims.

Method: documentation only; no commands were run.
