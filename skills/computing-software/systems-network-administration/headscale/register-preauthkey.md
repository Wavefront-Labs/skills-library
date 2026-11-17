---
id: computing-software.systems-network-administration.headscale.register-preauthkey
name: register-preauthkey
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, preauthkeys, authkey, automation, one-hour]
level: practitioner
status: docs-checked
description: "Create a pre-authenticated key and register a node non-interactively with tailscale up --authkey; default one-time use and one-hour expiry."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/registration.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/getting-started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-authenticated key registration

Non-interactive; suited to automation. By default a key can be used once and expires after one hour.

## Personal device

```
headscale preauthkeys create --user <USER>
tailscale up --login-server <YOUR_HEADSCALE_URL> --authkey <YOUR_AUTH_KEY>
```

`--user` accepts the username or the numeric ID from the users list.

## Tagged device

```
headscale preauthkeys create --tags tag:<TAG>
tailscale up --login-server <YOUR_HEADSCALE_URL> --authkey <YOUR_AUTH_KEY>
```

Tags come from the key, so `--advertise-tags` is not needed. If you do advertise tags, a subset of the key's tags is accepted; other tags are rejected.

## Verify

`headscale nodes list` should show the node online, with the owner (User column) and Tags column as expected.

## Gotchas

- The default key is valid for one hour and can be used once, so create it shortly before use.
- Registration through a pre-authenticated key keeps working even when the web-authentication pending queue is full.

## Checked

2026-11-04. Confirmed against the Headscale registration reference and getting-started pages: key defaults (once, one hour), `--user` by name or ID, `--tags`, tags read from the key with a subset accepted, nodes list columns, and availability when the pending queue is full. Removed unsourced generic gotchas (credential handling, Android and container remarks).
Method: documentation only; no commands were run.
