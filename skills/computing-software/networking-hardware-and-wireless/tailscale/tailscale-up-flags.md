---
id: computing-software.networking-hardware-and-wireless.tailscale.tailscale-up-flags
name: tailscale-up-flags
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tailscale-up, advertise-tags, reset-flag]
level: practitioner
status: docs-checked
description: "Know the key flags and how up treats omitted flags."
sources: ["https://tailscale.com/kb/1241"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tailscale up

Goal: connect a node and set options without surprises.

**Flags persist; omissions warn.** Pass all non-default flags each time. In v1.8 or later, if you omit a flag you set before, the CLI warns and gives a copyable command including existing flags. `--reset` resets unspecified settings to defaults. To clear a value pass it empty:
```
tailscale up --advertise-tags=
```

**Common flags**

- `--auth-key=<key>`: authenticate non-interactively; `file:` prefix reads from a file.
- `--advertise-tags=<tags>`: you must be listed in `tagOwners`.
- `--advertise-routes=<ip>`, `--advertise-exit-node`, `--advertise-connector`.
- `--accept-routes`: default depends on the OS.
- `--accept-dns`: defaults to accepting admin console DNS settings.
- `--exit-node=<ip|name>` (or `auto:any` to follow the suggested exit node) and `--exit-node-allow-lan-access`.
- `--hostname=<name>`: changes the MagicDNS machine name.
- `--login-server=<url>`: custom control server such as Headscale.
- `--netfilter-mode`: Linux, `off`, `nodivert` or `on` (default `on`, Synology `off`).
- `--shields-up`: block incoming connections from other tailnet devices.
- `--ssh`, `--operator=<user>`, `--qr`, `--force-reauth`, `--json`.
- Workload identity: `--client-id`, `--id-token`, `--audience`.

**Checklist**

1. Re-state flags on every `up`.
2. Use `--advertise-tags=` to clear tags.
3. Take care with `--netfilter-mode`.

## Checked

2026-11-03. Read tailscale up command (kb/1241) and confirmed the v1.8 warning on omitted flags, `--reset`, clearing with an empty value, and the listed flags. Nothing else was removed.

Method: documentation only; no commands were run.
