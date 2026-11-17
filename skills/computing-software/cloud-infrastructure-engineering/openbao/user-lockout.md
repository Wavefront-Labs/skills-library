---
id: computing-software.cloud-infrastructure-engineering.openbao.user-lockout
name: user-lockout
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, user-lockout, lockout-threshold, disable-lockout, auth-tune]
level: practitioner
status: docs-checked
description: "OpenBao user lockout defaults (5 attempts, 15 minutes), the user_lockout stanza, per-mount tuning and the disable precedence."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/user-lockout.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User lockout

Defaults:

- lockout threshold: 5 failed attempts
- lockout duration: 15 minutes
- counter reset: 15 minutes without attempts resets the failure count to zero

## Configure

Use a `user_lockout` stanza in the config file, for all auth methods or one of userpass, ldap or approle. Override one mount with the auth tune command or API.

## Disable

- Globally: set the `BAO_DISABLE_USER_LOCKOUT` environment variable.
- Per auth method: `disable_lockout` in the `user_lockout` stanza.
- Per mount: through auth tune.

Precedence: environment variable, then per-mount tune, then per-method config, then the "all" config, then defaults.

## Gotcha

Only userpass, ldap and approle support lockout.

## Checked

2026-11-04. Confirmed against the User lockout page: enabled by default, threshold 5, duration 15 minutes, counter reset 15 minutes, BAO_DISABLE_USER_LOCKOUT, disable_lockout in the user_lockout stanza, auth tune, both precedence orders and the userpass, ldap and approle limitation. Removed an extrapolation about token and cert logins that the page does not state.

Method: documentation only; no commands were run.
