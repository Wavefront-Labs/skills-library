---
id: computing-software.cybersecurity-defensive.pomerium.ssh-trust-user-ca-upstream
name: ssh-trust-user-ca-upstream
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [trusted-user-ca-keys, sshd-config, upstream-ssh-server, root-owned, sshd-restart]
level: practitioner
status: docs-checked
description: "Configure upstream sshd to trust the Pomerium User CA with TrustedUserCAKeys, including file ownership and restart steps."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On each upstream server:

1. Copy `pomerium_user_ca_key.pub` to a root-owned location, e.g. `/etc/pomerium/`, `/var/lib/pomerium/` or `/etc/ssh/`.
2. Create `/etc/ssh/sshd_config.d/50-pomerium.conf` (or edit `/etc/ssh/sshd_config`) containing:

```
TrustedUserCAKeys /path/to/pomerium_user_ca_key.pub
```

3. Restart sshd: `sudo systemctl restart ssh` or `sshd` (the unit is `ssh` on Ubuntu/Debian, `sshd` elsewhere), then check with `systemctl status` on the same unit.

Caveat: OpenSSH does not enforce ownership or permissions on the `TrustedUserCAKeys` file, so make sure it is root-owned and read-only yourself.

Users then connect as `user@route@pomerium` (see ssh-connect-syntax-and-cli); the Linux username is the `user` part.

If you use jump-host mode instead, upstreams do not need to trust the Pomerium User CA (see ssh-jump-host-mode).

## Checked

2026-11-04. Read the Native SSH Access page: key locations, sshd config file path and directive, ssh versus sshd unit names, and the ownership caveat all confirmed. Nothing removed.

Method: documentation only; no commands were run.
