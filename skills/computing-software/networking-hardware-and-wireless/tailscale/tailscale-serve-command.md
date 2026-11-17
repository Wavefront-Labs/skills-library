---
id: computing-software.networking-hardware-and-wireless.tailscale.tailscale-serve-command
name: tailscale-serve-command
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tailscale-serve, reverse-proxy, set-path]
level: practitioner
status: docs-checked
description: "Serve a port, file or directory inside the tailnet with HTTPS, HTTP or TCP forwarding."
sources: ["https://tailscale.com/kb/1242"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tailscale serve

Goal: expose a local resource to tailnet devices only.

```
tailscale serve localhost:3000
tailscale serve --http=80 localhost:3000
tailscale serve --https=<port> <target> [off]
```

**Targets.** Four modes: HTTP reverse proxy, file, directory or static text. HTTPS uses an automatically provisioned TLS certificate and is the default. HTTP servers are reachable by short MagicDNS names.

**Flags**

- `--bg`: run as a background process.
- `--http=<port>`, `--https=<port>`, `--tcp=<port>`, `--tls-terminated-tcp=<port>`.
- `--set-path=<path>`: slash-separated mount path; `/` is the root.
- `--proxy-protocol=<version>`: PROXY protocol version (1 or 2) for TCP forwarding.
- `--service=<virtual-ip>`: serve for a Tailscale Service with its own virtual IP.
- `--tun`: Layer 3 Service forwarding to the local machine, Services only.
- `--accept-app-caps=<capability-1,capability-2,...>`: comma-separated app capabilities to forward to the server.
- `--yes`: no interactive prompts.

**Subcommands:** `status`, `reset`, `drain`, `advertise`, `get-config`, `set-config`.

To expose publicly use `tailscale funnel` instead.

**Checklist**

1. Use `status` to inspect.
2. Use `--bg` for persistence.
3. Use `reset` to clear config.

## Checked

2026-11-03. Read tailscale serve command (kb/1242) and confirmed flags, subcommands, target modes, MagicDNS HTTP access and `reset`/`--bg` behaviour; reworded the `--proxy-protocol` and `--accept-app-caps` flag forms to the documented ones. Nothing else was removed.

Method: documentation only; no commands were run.
