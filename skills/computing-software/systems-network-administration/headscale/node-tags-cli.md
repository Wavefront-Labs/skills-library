---
id: computing-software.systems-network-administration.headscale.node-tags-cli
name: node-tags-cli
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, tags, nodes-tag, force-reauth, tagged-devices]
level: practitioner
status: docs-checked
description: "Set, change and remove tags on Headscale nodes with the CLI, and convert nodes between personal and tagged ownership."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/tags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing tags

Tags can be applied at registration (`--advertise-tags` or a tagged pre-authenticated key) or later by an administrator via the CLI or API.

```
headscale nodes list
headscale nodes tag -i 1 -t tag:server,tag:prod
```

- `nodes list` shows each node's tags.
- At least one tag is required; give several as a comma-separated list.

## Personal to tagged

```
headscale nodes tag -i <NODE_ID> -t <TAG>
```

The node is then owned by the special user `tagged-devices`.

## Tagged back to personal

Re-authenticate the client:

```
tailscale up --login-server <YOUR_HEADSCALE_URL> --advertise-tags= --force-reauth
headscale auth register --user <USER> --auth-id <AUTH_ID>
```

A browser window with instructions usually opens and prints an Auth ID. All previously assigned tags are removed, and the node becomes owned by the user named in `auth register`.

## Gotchas

- Tagged nodes are exempt from default key expiry (config-example.yaml; see node-expiry).

## Checked

2026-11-04. Confirmed against the Headscale tags page: registration paths, nodes list and nodes tag with -i and -t, the at-least-one-tag rule, both conversions, tagged-devices ownership, and tag removal on re-authentication. Removed an unsourced tagOwners remark.
Method: documentation only; no commands were run.
