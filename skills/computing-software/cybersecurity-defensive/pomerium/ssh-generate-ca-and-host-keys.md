---
id: computing-software.cybersecurity-defensive.pomerium.ssh-generate-ca-and-host-keys
name: ssh-generate-ca-and-host-keys
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [ssh-user-ca, ssh-host-keys, ssh-keygen, native-ssh, user-ca-key]
level: practitioner
status: docs-checked
description: "Generate the Pomerium native SSH User CA key pair and host keys with ssh-keygen, including key types and defaults."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Native SSH needs Pomerium v0.30.0 or later. Create the keys first.

**User CA key pair**

```
ssh-keygen -N "" -f pomerium_user_ca_key -C "Pomerium User CA"
```

`-N ""` (empty password) is required; `-f` sets the filename; `-C` is an optional comment. Output: `pomerium_user_ca_key` (private, used by Pomerium to sign ephemeral certificates) and `pomerium_user_ca_key.pub` (public, distributed to upstream servers). It is a standard SSH key pair, not a certificate.

**Host keys**

```
ssh-keygen -N "" -t ed25519 -f pomerium_ssh_host_ed25519_key
ssh-keygen -N "" -t rsa -f pomerium_ssh_host_rsa_key
ssh-keygen -N "" -t ecdsa -f pomerium_ssh_host_ecdsa_key
```

Defaults: RSA 3072 bits, ECDSA 256 bits.

Next steps: point Pomerium at them (ssh-configure-pomerium-and-routes) and trust the public CA on upstreams (ssh-trust-user-ca-upstream).

## Checked

2026-11-04. Read the Native SSH Access page: v0.30.0 minimum, ssh-keygen commands and flags, output files, host key types and default sizes all confirmed. Removed an unsourced warning sentence about the CA key.

Method: documentation only; no commands were run.
