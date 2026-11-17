---
id: computing-software.systems-network-administration.ceph.rbd-exclusive-lock
name: rbd-exclusive-lock
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rbd, exclusive-lock, object-map, fast-diff, blocklist]
level: advanced
status: docs-checked
description: "How RBD exclusive locks work, what depends on them, and the warning that they do not stop two clients writing in turn."
sources:
  - https://docs.ceph.com/en/latest/rbd/rbd-exclusive-locks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `exclusive-lock` feature is enabled on newly created images. Override the default through the `rbd_default_features` configuration option or the `--image-feature` and `--image-shared` options of `rbd create`.

Behaviour:

- A client (a librbd process, or a krbd client node's kernel) that must write acquires the lock; if another client holds it, that client is asked to release it.
- A client asked to release stops handling writes, flushes its caches and releases the lock.
- A client terminating gracefully releases it as well, which lets another client acquire it.

Important warning from the docs: by default the feature does not prevent two or more concurrently running clients opening the same image and writing in turns, on the same node or not. Their writes just get linearized as the lock transitions back and forth cooperatively. It protects internal image structures (the object map, the journal, the PWL cache) from concurrent modification.

Many image features, including `object-map` and `fast-diff`, depend upon exclusive locking; disabling it negatively affects the performance of some operations. It is a prerequisite for journaling in journal-based mirroring and for fast incremental diffs in snapshot-based mirroring. It is incompatible with RBD advisory locks (`rbd lock add` and `rbd lock rm`).

To disable automatic lock transitions, the `RBD_LOCK_MODE_EXCLUSIVE` flag may be specified when acquiring the lock; this is exposed as the `--exclusive` option of `rbd device map`.

## Blocklisting

When a lock holder dies abruptly (a KILL or ABRT signal, a hard reboot or a power failure), the lock is never released and a new client must break it. The old holder might only be hung or disconnected, so the new client also blocklists it, negotiated with the Ceph Monitor: the monitor tells the relevant OSDs to stop serving the old client, then after the OSD map update the new client breaks the lock and starts writing. This is storage-level resource fencing. The client needs the `osd blocklist` capability, included in the `profile rbd` capability profile.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "RBD Exclusive Locks" on docs.ceph.com. Corrected the mirroring statement to what the page says (prerequisite for journaling and for fast incremental diffs) and added the advisory-lock incompatibility note.
