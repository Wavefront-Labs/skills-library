---
id: computing-software.data-engineering.apache-hadoop.hdfs-permissions-umask-sticky
name: hdfs-permissions-umask-sticky
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, permissions, umask, sticky-bit, superuser]
level: practitioner
status: docs-checked
description: "HDFS POSIX-like permissions: r/w/x meaning, fs.permissions.umask-mode default 0022, sticky bit on directories, superuser and dfs.permissions.superusergroup."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsPermissionsGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDFS permissions

Each file and directory has an owner, a group, and separate permissions for owner, group and others. Files: `r` read, `w` write/append. Directories: `r` list, `w` create/delete children, `x` access a child. There are no setuid/setgid bits. New items get the creating client's user as owner and the parent directory's group.

Umask: `fs.permissions.umask-mode`, default `0022`. With no explicit mode, files are `0666 & ^umask` and directories `0777 & ^umask`.

Sticky bit: on a directory it stops anyone except the superuser, directory owner or file owner from deleting or moving entries inside. It has no effect on files.

Superuser: the identity of the NameNode process; permission checks never fail for it. `dfs.permissions.superusergroup` (default `supergroup`) names a group whose members are also superusers. Only the superuser can change a file's owner.

`dfs.permissions.enabled` (default true): when false, checking is off but nothing else changes, and switching does not alter modes, owners or groups. `chmod`, `chgrp`, `chown` and `setfacl` always check permissions, so owners and modes can be set up before enabling checks.

Details from the page:
- Check order: if the user is the owner, owner bits are tested; else if a group of the user matches the file's group, group bits; else other bits. Operations also need EXECUTE on every existing path component except the last (traversal).
- Mode with an explicit permission P: files `P & ^umask & 0666`, directories `P & ^umask & 0777`. In configuration files the umask may be written as decimal 18.
- `chmod`: owner or superuser. `chgrp`: owner who belongs to the target group, or superuser. `chown` to change the owner: superuser only.
- Identity comes from `hadoop.security.authentication` (simple: host OS user; kerberos: principal's primary component only), and groups from `hadoop.security.group.mapping`. HDFS has no way to create users or groups itself.
- There is no persistent superuser; whoever's identity runs the NameNode process is the superuser, and the page says it need not be the host's superuser.
- `dfs.web.ugi` sets the web server's identity; `dfs.cluster.administrators` is an ACL for who can access default servlets.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HdfsPermissionsGuide.md in the apache/hadoop repo). Core claims were accurate; added the mode formulas and command rules, removed an unsupported "Verify" step.
