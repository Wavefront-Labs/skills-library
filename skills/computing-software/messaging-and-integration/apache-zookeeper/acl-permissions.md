---
id: computing-software.messaging-and-integration.apache-zookeeper.acl-permissions
name: acl-permissions
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, acl, permissions, create, read, write, delete, admin]
level: practitioner
status: docs-checked
description: "ZooKeeper ACL permission model: five permissions, non-recursive ACLs, no owner, which calls need ADMIN or READ, and the standard open/read/creator ACLs."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACL permissions

- Permissions: CREATE (create a child), READ (get data and list children), WRITE (set data), DELETE (delete a child), ADMIN (set permissions). CREATE and DELETE were split out of WRITE for finer control.
- There is no LOOKUP permission; everyone implicitly has it, which allows a stat of a node and nothing more.
- ACLs are not recursive: an ACL applies only to its own znode, not its children. ZooKeeper has no notion of a znode owner; ADMIN plays that role.
- To retrieve a znode's ACL you need READ or ADMIN; without ADMIN the digest hash values are masked out. `set_acl` needs ADMIN.
- From 3.9.2, 3.8.4 and 3.7.3, `exists()` verifies ACLs on existing nodes and the client needs READ, otherwise "Insufficient permission" is raised.
- C constants: ZOO_PERM_READ, ZOO_PERM_WRITE, ZOO_PERM_CREATE, ZOO_PERM_DELETE, ZOO_PERM_ADMIN, ZOO_PERM_ALL.
- Standard ACLs: `ZOO_OPEN_ACL_UNSAFE` (all permissions to anyone), `ZOO_READ_ACL_UNSAFE` (read to anyone), `ZOO_CREATOR_ALL_ACL` (all permissions to the creator, who must already be authenticated, for example with the digest scheme).
- Server option `skipACL` (system property `zookeeper.skipACL`) skips ACL checks: more throughput, but full access to the data tree for everyone.

Verify: `getAcl /path` in the CLI prints the ACL set on that znode.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Programmer's Guide (ACL section) and the Administrator's Guide (skipACL). Removed: the claim that `getAcl` output shows "permission letters" (the pages show `scheme:id` plus a permission string in CLI examples, not specified as a contract).
