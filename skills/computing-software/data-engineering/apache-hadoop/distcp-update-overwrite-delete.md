---
id: computing-software.data-engineering.apache-hadoop.distcp-update-overwrite-delete
name: distcp-update-overwrite-delete
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, distcp, update, overwrite, delete, preserve]
level: practitioner
status: docs-checked
description: "DistCp copy semantics: -update versus -overwrite, the directory-contents rule, -delete, -append, -p preservation flags, -i failure handling, atomic and cross-version copies."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-distcp/DistCp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DistCp semantics

Basic: `hadoop distcp hdfs://nn1:8020/foo/bar hdfs://nn2:8020/bar/foo`. Many sources can be listed or read with `-f <urilist_uri>`. Source collisions abort; by default existing destination files are skipped.

- `-update`: copy files missing or different (compares size, block size, checksum); changed files are replaced, not synced.
- `-overwrite`: replace existing targets.
- With either, the contents of source directories are copied, not the directories themselves.
- `-append` (with `-update`, not with `-skipcrccheck`): copy only the extra tail when the common part matches.
- `-delete`: remove destination files absent from the source; needs `-update` or `-overwrite`; goes through the FS shell so trash applies.

Preserve with `-p[rbugpcaxte]`: replication, block size, user, group, permission, checksum type, ACL, XAttr, timestamp, erasure coding policy. With `-update`, status updates are not synchronised unless file sizes also differ (the file is re-created). `-pa` also preserves permissions since ACLs are a superset; `-pr` is only valid if neither source nor target is erasure coded. Raw xattrs (encryption metadata) are preserved solely by using `/.reserved/raw` prefixes on all source and target paths, not by `-p`; using the prefix on only some paths is an error. `-skipcrccheck` skips CRC checks.

Failures: `-i` ignores failures and lets other splits continue; without it a map failing `mapreduce.map.maxattempts` times kills the others. `-log <dir>` writes per-file logs; `-v` needs `-log`.

`-atomic [-tmp dir]` copies then moves into place (avoid on object stores); `-direct` writes straight to destination (for object stores); `-async` returns after launch.

Across major versions use `webhdfs://<nn>:<http_port>`; `swebhdfs://` for SSL.

The page recommends cross-checking source and destination listings after a copy, since problems in MapReduce, the FileSystem API or either cluster can silently affect it; some have run a second pass with `-update`, but you should know its semantics first. A source file still being written by another client will likely fail the copy, and a source removed before copying fails with FileNotFoundException. With object stores, `-atomic` does not really deliver atomicity and should be avoided, and `-append` is not supported.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (DistCp.md.vm in the apache/hadoop repo, Usage, Command Line Options and object store sections). Claims were accurate; added the erasure-coding flag, raw xattr rule and listing cross-check, and replaced an unsupported "Verify" line.
