---
id: computing-software.systems-network-administration.home-assistant.auth-providers
name: auth-providers
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [auth-providers, lockout, fallback]
level: advanced
status: docs-checked
description: "Configure auth_providers in Home Assistant without locking yourself out: always keep type homeassistant as a fallback, and keep the block in configuration.yaml."
sources:
  - https://www.home-assistant.io/docs/authentication/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add an extra login method while keeping password login.

The default Home Assistant provider is enabled automatically. You only configure `auth_providers` to add a method such as trusted networks. Built-in providers: `homeassistant` (username and password stored locally), `trusted_networks`, and command line.

Danger: adding `auth_providers` disables every provider not listed. A typo or missing entry can block all access, and the UI cannot recover it; you need file system access. Using only `trusted_networks` without the fallback lets anyone on that network log in by choosing a username, with no password.

Always include `type: homeassistant`:

```yaml
homeassistant:
  auth_providers:
    - type: homeassistant
    - type: trusted_networks
      trusted_networks:
        - 192.168.0.0/24
```

Steps:

1. Edit configuration.yaml.
2. Under `homeassistant:`, list every provider you want.
3. Include `type: homeassistant`.
4. Keep this block in configuration.yaml; if you move configuration into packages, `auth_providers` cannot be moved into a package file.
5. Restart Home Assistant.

The first user created is the owner and can create other users under Settings > People, Users tab. Passwords are stored hashed and salted in the `.storage` directory.

## Checked

2026-11-04. Confirmed against the Authentication providers page. Nothing removed.

Method: documentation only; no commands were run.
