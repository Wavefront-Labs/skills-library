---
id: computing-software.systems-network-administration.headscale.register-web-auth
name: register-web-auth
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, web-authentication, auth-id, register, tailscale-up]
level: intro
status: docs-checked
description: "Register a Tailscale client with Headscale through web authentication: tailscale up, the Auth ID, and headscale auth register for the owner."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/registration.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/getting-started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web authentication registration

The default, interactive method. The administrator approves the node via the CLI, the API, or delegation to an identity provider with OIDC.

## Personal device

1. Create the user: `headscale users create <USER>`
2. On the client:

```
tailscale up --login-server <YOUR_HEADSCALE_URL>
```

3. The browser page prints an Auth ID. Approve it on the server:

```
headscale auth register --user <USER> --auth-id <AUTH_ID>
```

4. Confirm: `headscale nodes list` shows the node online with its owner.

## Tagged device

```
tailscale up --login-server <YOUR_HEADSCALE_URL> --advertise-tags tag:<TAG>
headscale auth register --user <USER> --auth-id <AUTH_ID>
```

The user must be authorised in `tagOwners` in the policy. Headscale checks this, then transfers ownership to `tagged-devices`.

## Gotchas

- Pending requests are bounded; see pending-registration-limits.
- The same approval is available through the API: `POST /api/v1/auth/register` with a JSON body holding `user` and `authId`, authenticated with an API key.

## Checked

2026-11-04. Confirmed against the Headscale registration reference, getting-started and API pages: `tailscale up --login-server`, Auth ID, `headscale auth register --user --auth-id`, tagOwners check, `tagged-devices` ownership, and the API register call. Removed an unsourced Android log remark.
Method: documentation only; no commands were run.
