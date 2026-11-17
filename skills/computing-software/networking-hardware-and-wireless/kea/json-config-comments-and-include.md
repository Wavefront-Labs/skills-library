---
id: computing-software.networking-hardware-and-wireless.kea.json-config-comments-and-include
name: json-config-comments-and-include
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, configuration, json, include, comments, user-context]
level: practitioner
status: docs-checked
description: "Handle comments and file includes in Kea JSON configuration, and which comment forms survive config-get and config-write."
sources:
  - https://kea.readthedocs.io/en/latest/arm/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea JSON config comments and includes
Kea accepts shell, C and C++ style comments in configuration files, but they are lost on `config-get` and `config-write`. To keep data, use a `comment` string or `user-context`, which are retained.

Split a configuration with the include directive:

```
<?include "/path/to/subnets.json"?>
```

The path can be absolute or relative to the directory Kea was launched from. Includes may nest up to 10 levels.

## Checked

2026-11-08. Read the Kea Configuration chapter sections 6.1.1 to 6.1.4 in full: shell, C and C++ comments, loss on config-get and config-write, the comment string and user-context retention, the include directive form, the path rule and the ten-level nesting limit. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
