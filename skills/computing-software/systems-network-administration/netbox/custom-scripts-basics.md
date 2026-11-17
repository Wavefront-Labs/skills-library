---
id: computing-software.systems-network-administration.netbox.custom-scripts-basics
name: custom-scripts-basics
category: computing-software
field: systems-network-administration
product: netbox
tags: [custom-scripts, script-class, run-method]
level: advanced
status: docs-checked
description: "Subclass Script, declare variables and implement run()."
sources: ["https://netboxlabs.com/docs/netbox/customization/custom-scripts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom scripts

Goal: run custom Python logic from the NetBox UI.

Scripts can populate devices and cables for a new site, create reserved prefixes, import external data, fix incomplete objects, or validate data (for example every router has a loopback with an IP).

**Deprecation.** From v4.7 the built-in scripts feature is deprecated in favour of a dedicated open source plugin. The core implementation remains supported through v4.7 and v4.8 and is scheduled for removal in v5.0. Existing scripts continue to work.

**Rules**

- The file name (without `.py`) becomes the module name. Do not match a NetBox app such as `dcim.py` or `circuits.py`.
- Inherit from `extras.scripts.Script`.

```python
from extras.scripts import Script, StringVar, IntegerVar, ObjectVar

class MyScript(Script):
    var1 = StringVar(...)
    def run(self, data, commit):
        ...
```

`data` is a dictionary of form values; `commit` is a boolean for whether changes will be committed. Variables are optional.

**Safety.** Scripts have unrestricted database access. Install only trusted scripts and review who may run them.

**Checklist**

1. Unique file name.
2. Implement `run(self, data, commit)`.
3. Restrict run permission.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Custom scripts page: deprecation from v4.7 and removal in v5.0, module naming rule, Script base class, run(self, data, commit) signature, unrestricted database access warning. Removed: Nothing.

Method: documentation only; no commands were run.
