---
id: computing-software.data-engineering.apache-hadoop.hdfs-acls
name: hdfs-acls
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, acl, setfacl, getfacl, access-control]
level: practitioner
status: docs-checked
description: "HDFS POSIX ACLs: enabling with dfs.namenode.acls.enabled, setfacl/getfacl, named entries, mask, default ACLs on directories, and the 32-entry limits."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsPermissionsGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDFS ACLs

Property `dfs.namenode.acls.enabled` defaults to `true`; when false the NameNode rejects every attempt to set an ACL.

Commands:

```
hdfs dfs -getfacl [-R] /path/to/dir
hdfs dfs -setfacl [-R] [-b | -k -m | -x <acl_spec> <path>] | [--set <acl_spec> <path>]
```

`ls` marks items having an ACL with a trailing `+`.

Entry types: unnamed user (owner), unnamed group, named user, named group, mask, other. The mask filters named user, named group and unnamed group entries. If you do not supply a mask one is calculated automatically; `chmod` on an ACL'd file changes the mask.

Default ACL entries (prefix `default:`) exist only on directories and are copied to children at creation time. `dfs.namenode.posix.acl.inheritance.enabled` is on by default, so parent defaults apply to new files and the client umask is ignored for compatible clients.

Limits: 32 access entries and 32 default entries per item (64 total).

Default ACLs must contain the minimum entries (owner, group, other) and a mask; missing ones are filled in by copying from the access ACL, or from permission bits if none. The copy to a child happens at creation, so later changes to the parent's default ACL do not change existing children. `getfacl` also shows a directory's default ACL; `getAclStatus` and the modify/remove/set ACL operations are also in the Java API.

Permission check with an ACL: owner entry, then named user entries (filtered by mask), then the file group and named group entries (filtered by mask), denying if a group matched but none granted access, otherwise other. The page's best practice is to rely mainly on permission bits and add few ACLs, since an ACL costs the NameNode extra memory.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HdfsPermissionsGuide.md in the apache/hadoop repo). Core claims were accurate; added the check order and default ACL rules, removed an unsupported "Verify" step.
