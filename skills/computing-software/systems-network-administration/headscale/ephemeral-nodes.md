---
id: computing-software.systems-network-administration.headscale.ephemeral-nodes
name: ephemeral-nodes
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, ephemeral, inactivity-timeout, ci, short-lived]
level: practitioner
status: docs-checked
description: "Ephemeral Headscale nodes are deleted after going offline; set node.ephemeral.inactivity_timeout and see how OAuth auth keys default to ephemeral."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/api.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral nodes

Headscale supports ephemeral nodes (features page).

```yaml
node:
  ephemeral:
    inactivity_timeout: 30m
```

`inactivity_timeout` is the time before an inactive ephemeral node is deleted (the example config value is `30m`).

## OAuth-created keys

With OAuth client auth keys (oauth-clients skill), the `ephemeral` attribute defaults to `true`: the node is removed after going offline per `node.ephemeral.inactivity_timeout`. Disable it explicitly:

```
tskey-client-<id>-<secret>?baseURL=https://headscale.example.com&ephemeral=false
```

The `preauthorized` attribute (default `false`) is accepted but has no effect, because Headscale always authorizes pre-auth-key nodes. Any other attribute is an error.

## Note

Booleans accept any Go `strconv.ParseBool` value.

## Checked

2026-11-04. Confirmed against config-example.yaml (`node.ephemeral.inactivity_timeout`), the Headscale API page (OAuth client attributes table, default of `ephemeral`) and the features page. Removed the advice about long-lived servers and the verification step, which the pages do not state.

Method: documentation only; no commands were run.
