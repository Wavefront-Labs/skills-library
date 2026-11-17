---
id: computing-software.systems-network-administration.incus.remote-add-and-switch
name: remote-add-and-switch
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, remote, client-certificate, token, keepalive, default-remote, https]
level: practitioner
status: docs-checked
description: "Manage Incus remotes: client certificate, add by trust token, keepalive, switch the default remote, and global remotes in /etc/incus."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/remotes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote servers

The target server must expose its API with `core.https_address`, then you authenticate with a trusted client certificate or token.

```
incus remote generate-certificate --tls-cert ./my-client.crt --tls-key ./my-client.key
incus remote add my-remote <token> --tls-cert ./my-client.crt --tls-key ./my-client.key
incus remote add my-remote 192.0.2.10 --keepalive 30
incus remote switch <remote_name>
incus remote get-default
incus remote set-keepalive my-remote 30
```

- `--encrypt` on generate-certificate passphrase-protects the key; it fails if either file already exists.
- The CLI ships with a remote named `local` (the local daemon).
- Keepalive holds the connection open for the given seconds (0 disables); useful when running many commands.

Global remotes: define them in `config.yml` under `/etc/incus/`; each entry has `addr`, `auth_type`, `project`, `protocol`, `public`. Server certificates go in `/etc/incus/servercerts/<remote>.crt`; optional client certs in `clientcerts/`. A user can override one with `incus remote rename` or `incus remote set-urls`, which copies it into their own configuration.

## Checked

2026-11-09. Confirmed against the Incus doc remotes.md: core.https_address requirement, generate-certificate and add forms, --encrypt and overwrite failure, local remote, switch and get-default, keepalive including 0 to disable, and global remote layout. Removed: nothing needed removing.

Method: documentation only; no commands were run.
