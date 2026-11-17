---
id: computing-software.networking-hardware-and-wireless.arista-eos.eapi
name: eapi
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, eapi, http-commands, json-rpc, command-api]
level: practitioner
status: draft
description: "Enable the EOS eAPI over HTTPS and run show/config commands with JSON-RPC from curl or Python."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# eAPI (command API)
Goal: programmatic CLI access with JSON.

```
management api http-commands
   protocol https
   no shutdown
   vrf MGMT
      no shutdown
username automation privilege 15 role network-admin secret sha512 <hash-placeholder>
```

```
curl -sk -u automation:<password> https://192.0.2.1/command-api -d '{"jsonrpc":"2.0","method":"runCmds","params":{"version":1,"cmds":["show version"],"format":"json"},"id":"1"}'
```

```python
from jsonrpclib import Server
sw = Server("https://automation:<password>@192.0.2.1/command-api")
print(sw.runCmds(1, ["show version"])[0]["modelName"])
```

- Config commands: `["enable","configure","interface Ethernet1","description x"]`.
- `format: text` returns CLI text.
- `show management api http-commands` shows listeners and VRFs.

Gotcha: eAPI is off by default and bound per VRF; self-signed certs fail validation unless you trust or disable verification in a lab. Use a service ACL and strong credentials.

Operational tip: create a dedicated least-privilege eAPI user and role, restrict with a service ACL, and rotate its password. Prefer certificate-based HTTPS with a proper CA over self-signed certificates. Pair this with `show management api http-commands` in monitoring so a disabled or mis-bound API is noticed before automation fails.

## Verify
- `show management api http-commands` shows `Enabled: Yes` and the curl call returns a `modelName`.
