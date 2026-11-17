---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-rbac-roles
name: talos-rbac-roles
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [rbac, os-admin, os-reader, os-operator, talosconfig, client-certificate, machine-config]
level: practitioner
status: docs-checked
description: "Talos API RBAC: the four predefined os: roles, generating a role-scoped talosconfig with talosctl config new, and enabling machine.features.rbac without locking yourself out."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/security/rbac.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos authorizes API users by certificate: the certificate subject's organization field encodes the user's role. Predefined roles:

- `os:admin` grants access to all methods.
- `os:operator` grants everything `os:reader` does, plus rebooting, shutting down, etcd backup, etcd alarm management and similar.
- `os:reader` grants "safe" methods, for example listing files but not reading file content.
- `os:etcd:backup` grants only the `/machine.MachineService/EtcdSnapshot` method.

Check the role in your current client config:

```sh
$ talosctl config info

[...]
Roles:               os:admin
[...]
```

RBAC is enabled by default in new clusters created with `talosctl` v0.11+ and disabled otherwise.

To enable it on an existing cluster without losing access, first upgrade both the Talos cluster and the `talosctl` tool. Then use `talosctl config new` to generate a fresh client configuration with the `os:admin` role. Further configurations for other roles come from the `--roles` flag:

```sh
talosctl config new --roles=os:reader reader
```

That writes a client configuration file named `reader` containing a certificate with the `os:reader` role. Only after the admin config is safely in hand, turn enforcement on in the machine configuration:

```yaml
machine:
  features:
    rbac: true
```

Hand `os:etcd:backup` configs to backup jobs and `os:reader` configs to monitoring, keeping `os:admin` for operators.

## Checked

Whole page read; roles, commands and the rbac setting confirmed.

Method: docs-checked 2026-11-09 against Talos v1.15 docs security/rbac.mdx (read in full).
