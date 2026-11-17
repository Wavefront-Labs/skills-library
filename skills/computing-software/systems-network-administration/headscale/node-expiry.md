---
id: computing-software.systems-network-administration.headscale.node-expiry
name: node-expiry
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, expiry, node-expire, reauthentication, oidc-expiry]
level: practitioner
status: docs-checked
description: "Control how long Headscale nodes stay registered: node.expiry default of 0, tagged nodes never expiring, OIDC overrides, and forcing re-auth."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/registration.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/oidc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node expiry

```yaml
node:
  expiry: 0
```

- `node.expiry` is the default key expiry for non-tagged nodes, whatever the registration method. Default 0: no default expiry unless a node is explicitly expired with `headscale nodes expire`. Tagged nodes are exempt and never expire.
- If a client explicitly requests a specific expiry, the client value is used.
- OIDC can override it via `oidc.expiry`, per the example config.

## OIDC interaction

```yaml
oidc:
  use_expiry_from_token: true
```

Uses the Access Token's expiry instead of `node.expiry` (default false). Access Tokens are short-lived, so raise the token lifetime at the identity provider first, or nodes will expire quickly. The OIDC docs show `node.expiry: 30d` as an example, with `0` disabling expiration.

## Force re-authentication

```
headscale node expire -i <NODE_ID>
```

Expires a node immediately; the client must re-authenticate.

## Gotchas

- Tagged nodes are exempt from expiry (register-tagged-nodes).
- Ephemeral nodes are deleted after `node.ephemeral.inactivity_timeout` of inactivity (ephemeral-nodes).
- A pre-authenticated key created with default settings is valid for one hour and can be used once; this is separate from node expiry.

## Checked

2026-11-04. Confirmed against config-example.yaml (`node.expiry`, tagged exemption, `use_expiry_from_token`), the OIDC page (node expiration, `headscale node expire -i`) and the registration page (preauthkey defaults). Removed the claim that expired nodes stay disconnected until re-registered, which the pages do not state.

Method: documentation only; no commands were run.
