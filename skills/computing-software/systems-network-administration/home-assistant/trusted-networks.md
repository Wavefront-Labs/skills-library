---
id: computing-software.systems-network-administration.home-assistant.trusted-networks
name: trusted-networks
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [trusted-networks, allowlist, cidr]
level: advanced
status: draft
description: "Skip the Home Assistant password prompt for specific IP ranges with the trusted_networks provider, plus trusted_users and allow_bypass_login options."
sources:
  - https://www.home-assistant.io/docs/authentication/providers/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: let devices on a specific network log in without a password.

The `trusted_networks` provider allowlists IP ranges. From those networks you are asked which user to use but need no password. MFA does not take part in login when this provider is used.

```yaml
homeassistant:
  auth_providers:
    - type: homeassistant
    - type: trusted_networks
      trusted_networks:
        - 192.168.0.0/24
        - fd00::/8
```

Options:

- `trusted_networks` (required, list): IPv4 or IPv6 addresses or networks to allow.
- `trusted_users` (optional, map): a list of user IDs available for selection when logging in from a given address or network (`USER_ID`).
- `allow_bypass_login` (optional, boolean, default `false`): skip the login page if only one user is available for selection.

Cautions:

- Keep `type: homeassistant` as fallback. With only trusted_networks, anyone on that network can sign in by picking a username.
- You cannot trust a network you use in `trusted_proxies`; authentication fails with a message that your computer is not allowed.

Steps: choose the narrowest CIDR range that covers the devices, add it, restart, then test from a device inside and outside the range.
