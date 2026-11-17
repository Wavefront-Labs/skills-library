---
id: computing-software.cybersecurity-defensive.pomerium.ssh-configure-pomerium-and-routes
name: ssh-configure-pomerium-and-routes
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [ssh-address, ssh-routes, ssh-host-key-files, native-ssh, ssh-user-ca-key-file]
level: practitioner
status: docs-checked
description: "Set ssh_address, the User CA and host key files, and define ssh:// routes with a policy in Pomerium Core, Enterprise or Zero."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core `config.yaml`:

```yaml
ssh_address: 0.0.0.0:22 # choose another port if sshd already uses 22
ssh_user_ca_key_file: '/path/to/pomerium_user_ca_key'
ssh_host_key_files:
  - '/path/to/pomerium_ssh_host_ed25519_key'
  - '/path/to/pomerium_ssh_host_rsa_key'
  - '/path/to/pomerium_ssh_host_ecdsa_key'
```

Enterprise and Zero: Settings, SSH in the respective console.

Inline alternatives to the file settings: `ssh_user_ca_key` and `ssh_host_keys`.

Routes use the `ssh://` prefix in both `from` and `to`:

```yaml
routes:
  - from: ssh://route1
    to: ssh://upstream-server-1:22
    policy:
      - allow:
          and:
            - email:
                is: your.email@example.com
```

Prerequisites on the IdP side: for v0.31.x or lower the Device Code OAuth grant; for v0.32.0 or later Authorization Code OAuth. Pomerium needs network connectivity to the SSH servers. For SSH-specific policy criteria see ssh-policy-criteria.

## Checked

2026-11-04. Read the Native SSH Access page: Core settings, console location, ssh:// route syntax, and the IdP grant requirements by version all confirmed. Removed the description of what the inline settings contain, which the page's table does not state clearly.

Method: documentation only; no commands were run.
