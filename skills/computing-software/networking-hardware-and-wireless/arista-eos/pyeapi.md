---
id: computing-software.networking-hardware-and-wireless.arista-eos.pyeapi
name: pyeapi
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, pyeapi, arista-python, eapi-client, pyeapi-conf]
level: practitioner
status: draft
description: "Use the pyeapi library with an eapi.conf profile to run commands and edit configuration on EOS."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# pyeapi Python client
Goal: simple Python automation without raw JSON-RPC.

```
# ~/.eapi.conf
[connection:leaf1]
host: 192.0.2.1
username: automation
password: <from-vault>
transport: https
```

```python
import pyeapi
node = pyeapi.connect_to("leaf1")
print(node.enable("show version")[0]["result"]["version"])
node.config(["interface Ethernet3", "description to-core"])
vlans = pyeapi.client.load_config() and node.api("vlans").getall()
```

- Install with `pip install pyeapi`.
- Higher-level API objects: `node.api("vlans")`, `node.api("interfaces")`.
- Use `node.run_commands` for explicit JSON output, and `node.config` for config lines.

Gotcha: `.eapi.conf` holds credentials; protect permissions and prefer vault injection. A failed command in a list aborts the rest and returns an error object; handle `CommandError`.

Operational tip: wrap `node.config` calls in a try/except, log the exact commands, and prefer `configure session` through eAPI for atomic changes with the ability to abort if validation fails. Pin the pyeapi version, and keep the profile names in the config file aligned with your inventory names so scripts need no hard-coded addresses.

## Verify
- `node.enable("show version")` returns the running version matching `show version` on the switch.
