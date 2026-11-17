---
id: computing-software.networking-hardware-and-wireless.tailscale.tailscale-funnel-command
name: tailscale-funnel-command
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tailscale-funnel, funnel-ports, funnel-relay]
level: practitioner
status: docs-checked
description: "Publish a local resource to the internet through a Funnel URL and allowed ports."
sources: ["https://tailscale.com/kb/1223", "https://tailscale.com/kb/1311"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailscale Funnel

Goal: share a local resource with the public internet.

```
tailscale funnel [flags] <target>
tailscale funnel --https=443 --bg localhost:3000
```

**Allowed ports.** For Funnel, `--https` must be 443, 8443 or 10000.

**Flags.** `--bg`, `--https=<port>`, `--set-path=<path>`, `--tcp=<port>`, `--tls-terminated-tcp=<port>`, `--proxy-protocol=<version>` (1 or 2), `--yes`. Subcommands: `status`, `reset`. Targets work like `serve`: reverse proxy, file, directory or static text; HTTPS uses an automatically provisioned certificate.

**How it works**

1. Funnel creates a unique Funnel URL pointing only to the resource you shared.
2. A visitor's device resolves that URL via public DNS to a Funnel relay server.
3. The relay creates a TCP proxy to your device over Tailscale.
4. The relay does not decrypt traffic; the Tailscale server on your device terminates TLS and hands the request to your local service.
5. Responses are encrypted and travel back the same way.

**Checklist**

1. Use only the allowed ports.
2. Verify with `tailscale funnel status`.
3. Remove with `tailscale funnel reset`.

## Checked

2026-11-03. Read tailscale funnel command (kb/1223) and Funnel (kb/1311) and confirmed ports 443, 8443 and 10000, flags, `status`/`reset`, and the relay flow where relays do not decrypt traffic; reworded the `--proxy-protocol` flag form. Nothing else was removed.

Method: documentation only; no commands were run.
