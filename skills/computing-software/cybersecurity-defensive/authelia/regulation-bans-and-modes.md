---
id: computing-software.cybersecurity-defensive.authelia.regulation-bans-and-modes
name: regulation-bans-and-modes
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, regulation, brute-force, ban, max-retries, find-time, ban-time]
level: practitioner
status: docs-checked
description: "Tune Authelia's login regulation with modes user and ip, max_retries, find_time and ban_time, and know that stored bans override current settings."
sources:
  - https://www.authelia.com/configuration/security/regulation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Regulation temporarily bans after repeated failures on the username and password endpoint.

```yaml
regulation:
  modes:
    - 'user'
    - 'ip'
  max_retries: 3
  find_time: '2m'
  ban_time: '5m'
```

- `modes`: the default is `['user']`. `user` bans the account; `ip` bans the remote address. The documentation recommends `ip`, and lists both together in its example.- `max_retries` (default 3): failures before a ban. `0` disables regulation entirely.
- `find_time` (default 2 minutes): the window in which failures are counted. Three failures within two minutes triggers a ban at the defaults.
- `ban_time` (default 5 minutes): how long the ban lasts. After this the account or address can log in again.

An important detail: whatever modes are currently configured, any ban stored in the database still denies that user or IP. Changing the configuration does not lift existing bans.

Manage bans through `authelia storage bans`. Regulation is separate from endpoint rate limiting, which protects other endpoints such as password reset.

Check: fail a login deliberately max_retries times from a test account and confirm further attempts are refused until `ban_time` passes.

## Checked

2026-11-08. Read the full Authelia Regulation page. Confirmed modes, max_retries, find_time, ban_time defaults, the stored-ban note and the recommended ip mode; confirmed the separate endpoint rate limits on the Server Endpoint Rate Limits page. Removed the unconfirmed claim about proxy forwarding of the client address.

Method: documentation only; no commands were run.
