---
id: computing-software.systems-network-administration.home-assistant.securing-checklist
name: securing-checklist
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [security, mfa, updates]
level: practitioner
status: docs-checked
description: "Apply the Home Assistant securing checklist: strong accounts, MFA, secrets, updates, safe remote access and SSH hardening for manual installs."
sources:
  - https://www.home-assistant.io/docs/configuration/securing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: harden an instance, especially before any access from outside the home network.

Checklist from the docs:

- Use a strong, unique password for every account and turn on multi-factor authentication.
- Centralize sensitive data in secrets and back them up. Storing values in secrets.yaml does not encrypt them.
- Keep the system up to date with each monthly release.

Accounts:

- Give administrator access only to accounts that need it.
- A password manager makes unique passwords practical.

Remote access (do not expose Home Assistant directly to the internet):

- Home Assistant Cloud is described as the easiest and safest option: no port forwarding or certificate setup.
- TLS/SSL using the Duck DNS app with Let's Encrypt.
- A VPN or an SSH tunnel; forward the required port on your router.

Extras for manual installations:

- On systems using SSH, set this in the sshd configuration (usually `/etc/ssh/sshd_config`) and use SSH keys instead of passwords:

```text
PermitRootLogin no
```

- Lock down the host following good practice, for example the Securing Debian Manual (also applies to Raspberry Pi OS) or the Red Hat Enterprise Linux 7 Security Guide and the CIS Red Hat Enterprise Linux 7 Benchmark.

Work through the list before enabling remote access, then see the remote-access-options skill.

## Checked

2026-11-04. Confirmed against the Securing page. Reworded the Duck DNS line and the Red Hat Enterprise Linux 7 guide names to match the page.

Method: documentation only; no commands were run.
