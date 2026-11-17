---
id: computing-software.systems-network-administration.kopia.kopia-repository-server-and-acls
name: kopia-repository-server-and-acls
category: computing-software
field: systems-network-administration
product: kopia
tags: [repository-server, kopia-server, acl, tls, server-user, multi-user]
level: advanced
status: docs-checked
description: "Run a Kopia repository server so clients need no storage credentials, and control users and ACLs."
sources: ["https://kopia.io/docs/repository-server/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default every client connects straight to storage with read-write credentials, so a malicious user could delete data. A repository server proxies storage; clients need only a username and password. Each user sees only their own snapshots and policies, but only manifests are access-controlled, not contents: users who guess or know a content ID can read that content. Deduplicated identical files share IDs.

## Setup

Create the repository first, then add users. Users are lowercase `username@hostname`.

```console
kopia server user add myuser@mylaptop
kopia server user list
kopia server user set myuser@mylaptop
kopia server user delete myuser@mylaptop
kopia server refresh
```

Credential changes take 5 to 10 minutes or a restart or `server refresh`. Start with an auto-generated certificate the first time, which prints the SHA256 fingerprint:

```console
kopia server start --tls-generate-cert --tls-cert-file CERT --tls-key-file KEY --address 0.0.0.0:51515 --server-control-username control
```

Omit `--tls-generate-cert` on later starts or the server fails. Pass `KOPIA_PASSWORD` and `KOPIA_SERVER_CONTROL_PASSWORD` in the environment. A CA-issued certificate can be used with PEM files.

## Client

```console
kopia repository connect server --url https://ADDRESS:51515 --server-cert-fingerprint FINGERPRINT
```

Low-level commands such as `repository status` fail on server connections. Override identity with `--override-username` and `--override-hostname`.

## ACLs

Default rules let each user read and write their own policies and snapshots, read global and own-host policies, and append content. `kopia server acl enable` installs them for editing; `acl list`, `acl add --user U --access A --target T` define more. Access is `READ`, `APPEND` or `FULL`; targets are `type=snapshot|policy|user|acl` plus labels, with `OWN_USER` and `OWN_HOST` placeholders.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Repository Server page (rationale, user commands, 5-10 minute credential refresh, TLS generate-once, client connect, low-level command failure, override flags, default ACL rules, access levels, target types, OWN_USER/OWN_HOST).
Method: documentation only; no commands were run.
