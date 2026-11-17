---
id: computing-software.messaging-and-integration.apache-zookeeper.acl-schemes
name: acl-schemes
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, acl-schemes, world, auth, digest, ip, x509, addauth]
level: practitioner
status: docs-checked
description: "ZooKeeper ACL schemes world, auth, digest, ip and x509: id formats, the auth quirk, and zkCli addauth and setAcl usage."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACL schemes

- `world`: single id `anyone`.
- `auth`: uses the current authenticated user; the expression is ignored when persisting the ACL (but must still be present in the scheme:expression:perms form), and setting it fails if nobody is authenticated.
- `digest`: `username:password`; the password travels in clear text. In an ACL the expression is the username plus the base64 SHA1 password digest. The Programmer's Guide also mentions MD5; the admin guide's `digestAlg` (3.7.0+) default is SHA1.
- `ip`: `addr/bits`, the most significant bits of addr are matched against the client IP.
- `x509`: exact X500 Principal name; on the secure port clients are authenticated automatically.
- An ACL applies only to its own znode, not to children.

zkCli:
- `addauth scheme auth` adds credentials, e.g. `addauth digest user1:12345`.
- `setAcl [-s] [-v version] [-R] path acl` (`-R` recursive).
- `getAcl [-s] path`; `whoami` shows the session's auth info.

Verify: `getAcl` shows the scheme and an unauthenticated session is denied the restricted operation.

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Programmer's Guide (ACL section), CLI guide (addauth, getAcl, setAcl, whoami) and Admin guide (digestAlg).
