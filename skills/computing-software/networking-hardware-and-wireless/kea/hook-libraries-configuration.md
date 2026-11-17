---
id: computing-software.networking-hardware-and-wireless.kea.hook-libraries-configuration
name: hook-libraries-configuration
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, hooks, hooks-libraries, parameters, parked-packet-limit]
level: practitioner
status: docs-checked
description: "Load Kea hook libraries with hooks-libraries and parameters, order them correctly, and cap parked packets with parked-packet-limit."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# configuring hook libraries
Hooks are listed under `hooks-libraries` in a daemon's configuration (note the plural). It is an array of maps, each with `library` and optional `parameters`:

```json
"hooks-libraries": [
  { "library": "first_custom_hooks_example.so" },
  { "library": "second_custom_hooks_example.so",
    "parameters": { "floor": 13, "debug": false } } ]
```

- Libraries are reloaded on every reconfiguration even if the list is unchanged, since parameters or files they reference may have changed.
- Since Kea 2.7.9 libraries load only from the compiled hooks directory (shown as "Hooks directory" in the config report), overridable with `KEA_HOOKS_PATH`. Give the file name only; path components are deprecated since 2.7.8.
- Most hooks ship in the base sources and need no special install; some subscriber-only packages need extra steps.

Order matters when several libraries implement the same callout. Example from the docs: Flex ID must come before HA so the client ID is formed before HA uses it for load balancing. Put Forensic Logging last so other hooks have contributed first.

`parked-packet-limit` (global) caps how many responses can be parked awaiting hook work. At the limit new responses are dropped and logged until space frees up; it acts as congestion handling. Smaller values cause more drops.

## Checked

2026-11-08. Read sections 16.1 to 16.3.3 of the Hook Libraries chapter (the rest of the page was not read): the hooks-libraries array form, reload behaviour, KEA_HOOKS_PATH and the 2.7.8 and 2.7.9 path notes, base versus subscriber hooks, the Flex ID before HA and Forensic Logging last ordering advice, and parked-packet-limit. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
