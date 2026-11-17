---
id: computing-software.networking-hardware-and-wireless.tailscale.tailscale-lock-cli
name: tailscale-lock-cli
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tailscale-lock, lock-init, revoke-keys]
level: advanced
status: docs-checked
description: "Initialise, sign and disable Tailnet Lock with tailscale lock subcommands."
sources: ["https://tailscale.com/kb/1243"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tailscale lock

Goal: manage Tailnet Lock from a node.

**Subcommands**: `status`, `init`, `sign`, `disable`, `log`, `local-disable`, `revoke-keys`. Running `tailscale lock` alone equals `tailscale lock status`; output reports ENABLED, whether this node is accessible, this node's `tlpub:` key and trusted signing keys.

**Initialise**
```
tailscale lock init --gen-disablements=3 --gen-disablement-for-support --confirm tlpub:1234abcdef
```
- Arguments are space-separated Tailnet Lock public keys that are initially trusted; the key of the node you run it on must be included.
- `--gen-disablements <N>` sets how many disablement secrets (default one, the minimum).
- `--gen-disablement-for-support` generates an extra secret sent to Tailscale support, which could then disable Tailnet Lock.
- `--confirm=false` controls the confirmation prompt.
- Secrets display only at init; record them.

**Other**

- `sign` signs a node key and sends the signature to the coordination server.
- `disable` consumes a disablement secret to shut Tailnet Lock off tailnet-wide.
- `local-disable` disables it for this node only.
- `log` lists applied changes; `revoke-keys` retroactively revokes keys.

**Checklist**

1. Include your own key in init.
2. Save secrets.
3. Check `status` afterwards.

## Checked

2026-11-03. Read tailscale lock reference (kb/1243) and confirmed subcommands, `init` flags and disablement secret behaviour. Nothing else was removed.

Method: documentation only; no commands were run.
