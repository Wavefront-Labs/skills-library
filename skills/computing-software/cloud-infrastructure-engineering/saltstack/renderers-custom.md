---
id: computing-software.cloud-infrastructure-engineering.saltstack.renderers-custom
name: renderers-custom
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, renderers, custom-renderer, sync-renderers, python]
level: advanced
status: docs-checked
description: "Write a custom Salt renderer module with render(data, saltenv, sls), place it in _renderers and sync it to minions."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/renderers/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom renderers

Create a Python module with a `render` function taking `data`, `saltenv` and `sls`. `data` may be a string or a file-like object, so handle both.

Place it in `salt://_renderers/` so it can sync to minions. It syncs when any of these runs (the `saltutil.sync_renderers` and `saltutil.sync_all` runners sync it to the master):

```
salt '*' state.apply
salt '*' saltutil.sync_renderers
salt '*' saltutil.sync_all
```

A custom renderer with the same name as a built-in replaces that built-in.

Then reference it by name in a shebang pipeline. The complete renderer list is under the renderers `all` index in the docs.

## Checked

2026-11-09. Read in full the Salt Renderers page (doc/ref/renderers/index.rst, master branch): Writing Renderers. Dropped the `renderer` option reference (the page only documents it as the default-renderer setting).

Method: documentation only; no commands were run.
