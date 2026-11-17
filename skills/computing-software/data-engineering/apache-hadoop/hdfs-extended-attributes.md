---
id: computing-software.data-engineering.apache-hadoop.hdfs-extended-attributes
name: hdfs-extended-attributes
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, xattr, setfattr, getfattr, metadata]
level: practitioner
status: docs-checked
description: "HDFS extended attributes: the user, trusted, system, security and raw namespaces, setfattr/getfattr usage and value encodings, and the xattr limits."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/ExtendedAttributes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extended attributes

Xattrs let applications attach metadata to a file or directory; the system does not interpret them. Each is a name-value pair with a string name and binary value, and the name carries a namespace prefix, e.g. `user.myXattr`. An inode can have several. They are modelled on Linux xattrs.

Five namespaces:
- `user`: for client applications; access follows file permissions.
- `trusted`: HDFS superusers only.
- `system`: reserved for internal HDFS use; not accessible through userspace methods.
- `security`: reserved for internal use, generally not accessible from userspace. The exception is `security.hdfs.unreadable.by.superuser`: file-only, set and read by any user subject to normal permissions, write-once (cannot be removed), takes no value, and stops the superuser reading file contents (metadata such as owner and permissions stays readable and modifiable).
- `raw`: internal attributes, visible only through getXAttr/getXAttrs on paths under `/.reserved/raw`, superuser only. Encryption zone metadata lives in `raw.*` xattrs, so with `/.reserved/raw` paths for source and target, distcp copies encrypted files transparently.

Shell commands:

```
hadoop fs -getfattr [-R] -n name | -d [-e en] <path>
hadoop fs -setfattr -n name [-v value] | -x name <path>
```

getfattr: `-R` recursive, `-n` one named attribute, `-d` all attributes, `-e` encoding of text, hex or base64 (text values are shown in double quotes, hex prefixed 0x, base64 prefixed 0s). setfattr `-v`: a double-quoted argument is the literal string, a 0x/0X prefix is hexadecimal, a 0s/0S prefix is base64; `-x` removes the attribute.

Configuration (works without extra setup; the limits matter because xattrs add on-disk and in-memory inode size):
- `dfs.namenode.xattrs.enabled`: enabled by default.
- `dfs.namenode.fs-limits.max-xattrs-per-inode`: default 32.
- `dfs.namenode.fs-limits.max-xattr-size`: combined name and value size, default 16384 bytes.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (ExtendedAttributes.md in the apache/hadoop repo). Rewrote to the page's wording, replaced the invented example attribute commands, and removed an unsupported "Verify" step.
