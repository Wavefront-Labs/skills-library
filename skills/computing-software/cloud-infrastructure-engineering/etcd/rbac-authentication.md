---
id: computing-software.cloud-infrastructure-engineering.etcd.rbac-authentication
name: rbac-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [rbac, authentication, roles, users, auth-enable, root-user, grant-permission, permissions]
level: advanced
status: docs-checked
description: "Enable role-based access control: create root, users and roles, grant read/write permissions on keys and prefixes, then auth enable."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/authentication/rbac/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

There is one special user, `root`, and one special role, `root`. The root user must be created before activating authentication; it must have the root role and may change anything inside etcd. The root role can be granted to any user and carries global read-write access, permission to update the authentication configuration, and cluster maintenance privileges (membership changes, defragmentation, snapshots).

Minimal steps to enable auth (users and roles can be set up before or after):

```bash
etcdctl user add root          # prompts for a password
etcdctl auth enable
etcdctl --user root:rootpw auth disable
```

After enabling, pass credentials: `etcdctl --user user:password get foo`, or `--user user` to be prompted, or `--user user --password password`. Users and roles can still be modified but need authentication by a user with the root role. Authentication with an empty password via `--user username:` is not supported.

Users and roles:

```bash
etcdctl user add myusername
etcdctl user grant-role myusername foo
etcdctl role add myrolename
etcdctl role grant-permission myrolename read /foo
etcdctl role grant-permission myrolename --prefix=true read /foo/
etcdctl role grant-permission myrolename readwrite key1 key5
```

- Permission types: `read`, `write`, `readwrite`.
- Targets: a single key, a range `[start-key, end-key)` (start lexically less than end), or `--prefix=true`; the prefix `/foo/` equals the range `[/foo/, /foo0)`.
- Also available: `user list`, `user get`, `user passwd`, `user delete`, `user revoke-role`, `role list`, `role get`, `role revoke-permission` and `role delete`.
- `user add NAME` prompts for a password; `--interactive=false` reads it from standard input and `--new-user-password` supplies it. `user add NAME --no-password` makes a user that can only authenticate with a TLS Common Name.
- With `--client-cert-auth=true` (v3.2 and later) the client certificate CN is used as the etcd user; username and password take priority if both are given. This cannot be used with gRPC-proxy or gRPC-gateway.
- etcd does not enforce a password length.

Scope: authentication protects the V3 gRPC API operations. The `/metrics` and `/health` HTTP endpoints use a separate handler and are not protected by V3 RBAC. To secure them, enable mTLS with `--cert-file`, `--key-file` and `--client-cert-auth`, bind metrics to a private interface with `--listen-metrics-urls`, or use network policies or firewall rules.

## Checked

2026-11-08. Read in full: etcd v3.5 Role-based access control page. Confirmed every command, option and statement above. Removed: `role add root` and `user grant-role root root` as required steps (the page's minimal steps are user add root then auth enable), `--from-key` for permissions, and least-privilege advice (not on the page).
Method: documentation only; no commands were run.
