---
id: computing-software.systems-network-administration.zfs.zfs-redacted-send
name: zfs-redacted-send
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, redact, redacted-send, redaction-bookmark, privacy]
level: sme
status: docs-checked
description: "Send a ZFS snapshot with sensitive blocks removed using zfs redact and zfs send --redact, and handle the restrictions on redacted datasets."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-mount.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redacted sends

Redaction lets you send a snapshot while omitting data you have changed elsewhere (for example, a clone with secrets replaced).

## Create the bookmark

```
zfs redact tank/data@snap redaction_bookmark redaction_snapshot...
```

This creates a redaction bookmark on the parent snapshot, listing the blocks of the snapshot that no redaction snapshot references. If it fails partway, rerun the same command and it resumes.

## Send

```
zfs send --redact redaction_bookmark [-DLPVcenpv] [-i snapshot|bookmark] snapshot
```

(`-d` is the short form of `--redact`.)

## Behaviour

- The bookmark must come from `zfs redact` on the snapshot being sent.
- Only user data is redacted; redacted blocks become REDACT records.
- A block is omitted only if every redaction snapshot modified it.
- Raw and redacted sends cannot be combined.

## Receiving

The receiver gets a redacted dataset. It cannot be mounted by default; `zfs mount -f` tries to force-mount filesystems that normally cannot be mounted, such as redacted datasets, though a redacted dataset is incomplete and mainly serves as a base for receiving further streams (zfs-send(8), Redaction).

Bookmarking a redaction bookmark produces a regular bookmark, not a redaction bookmark. Check the result with `zfs list -t bookmark` on the sender.

## Checked

2026-11-03. Confirmed against zfs-send(8) (`--redact`, `zfs redact`, REDACT records, resumable redact, raw plus redacted), zfs-mount(8) (`-f`) and zfs-bookmark(8) (bookmark of a redaction bookmark). Replaced the wrong pointer to the receive man page.
Method: documentation only; no commands were run.
