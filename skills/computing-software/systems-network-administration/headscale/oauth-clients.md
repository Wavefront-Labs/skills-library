---
id: computing-software.systems-network-administration.headscale.oauth-clients
name: oauth-clients
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, oauth-clients, tskey-client, base-url, github-action]
level: advanced
status: docs-checked
description: "Use Headscale OAuth clients to mint tagged auth keys for CI and containers: create the client, build the tskey-client string, and the baseURL trap."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth clients

```
headscale oauth-clients create --scope auth_keys --tag tag:ci
```

The secret is shown once. Scopes include `auth_keys`, `oauth_keys` and `devices:core:read`. Each tag you advertise must exist in the policy's `tagOwners` and be one of the client's tags, or owned by one of them.

## Auth key string

Replace the prefix `hskey-client-` with `tskey-client-` (the client only runs the exchange for that prefix) and append your base URL:

```
tskey-client-<id>-<secret>?baseURL=https://headscale.example.com
```

```shell
tailscale up --login-server https://headscale.example.com --advertise-tags tag:ci \
  --auth-key 'tskey-client-<id>-<secret>?baseURL=https://headscale.example.com&ephemeral=false'
```

| Attribute | Default | Effect |
|---|---|---|
| `baseURL` | `https://api.tailscale.com` | exchange target; no trailing slash |
| `ephemeral` | `true` | removed after offline (`node.ephemeral.inactivity_timeout`) |
| `preauthorized` | `false` | accepted, no effect |

## Gotchas

- Without `baseURL`, the client sends the secret to `https://api.tailscale.com`.
- GitHub Action: `tailscale/github-action@v4` with input `authkey`; the deprecated `oauth-secret` corrupts `baseURL`.
- A client keeps its newest 1000 access tokens. Deleting a client revokes its secret and tokens, not the nodes it made.
- Containers: `TS_AUTHKEY` and `TS_EXTRA_ARGS='--login-server=... --advertise-tags=tag:ci'`.

## Checked

2026-11-04. Confirmed against the Headscale API reference (Join nodes with an OAuth client): create command, scopes, prefix swap, baseURL and its trap, attribute table, GitHub Action and container examples, the 1000-token limit, and deletion behaviour. Tightened the tag rule to the page wording.
Method: documentation only; no commands were run.
