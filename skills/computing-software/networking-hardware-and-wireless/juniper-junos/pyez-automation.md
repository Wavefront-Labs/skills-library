---
id: computing-software.networking-hardware-and-wireless.juniper-junos.pyez-automation
name: pyez-automation
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, pyez, junos-pyez, python-automation, junos-eznc]
level: practitioner
status: draft
description: "Use the Python PyEZ library to connect over NETCONF, run RPCs, and load and commit configuration with rollback."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Junos PyEZ automation
Goal: automate Junos with Python.

```python
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

with Device(host="192.0.2.1", user="automation", ssh_private_key_file="~/.ssh/id_ed25519") as dev:
    print(dev.facts["version"])
    with Config(dev, mode="exclusive") as cu:
        cu.load("set system host-name edge1", format="set")
        print(cu.diff())
        cu.commit_check()
        cu.commit(comment="pyez change", confirm=5)
```

- Install with `pip install junos-eznc`; the target needs `set system services netconf ssh`.
- Use `dev.rpc.get_interface_information(terse=True)` for operational data and `dev.rpc.get_config()` for config.
- `mode="exclusive"` or `private` avoids edit collisions; call `cu.rollback()` on failure.
- Tables/Views YAML maps XML to Python dicts.

Gotcha: commit with `confirm=5` and never follow with a plain commit leaves an auto rollback; also unhandled `ConnectError` / `LockError` exceptions leave locks until the session closes.

Operational tip: store the SSH key or vault credentials outside the script, pin the `junos-eznc` version in requirements.txt, and test against a lab device before running at scale.

## Verify
- `dev.facts` prints model and version; `show system commit` on the device shows your comment.
