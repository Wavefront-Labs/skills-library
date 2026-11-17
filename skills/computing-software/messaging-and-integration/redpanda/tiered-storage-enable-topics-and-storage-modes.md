---
id: computing-software.messaging-and-integration.redpanda.tiered-storage-enable-topics-and-storage-modes
name: tiered-storage-enable-topics-and-storage-modes
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [tiered-storage, storage-mode, remote-read, remote-write, tiered-v2, topic-properties]
level: practitioner
status: docs-checked
description: "Turn Tiered Storage on per cluster or topic with redpanda.storage.mode (26.1+), the legacy remote.read and remote.write properties, and choose v1 or v2 (beta in 26.2)."
sources:
  - https://docs.redpanda.com/streaming/current/manage/tiered-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `cloud_storage_enabled` to `true` first. Enabling Tiered Storage on a topic with data uploads existing local data from the earliest offset on local disk.

**Cluster-wide.** Set `cloud_storage_enable_remote_write` and `cloud_storage_enable_remote_read` to true; this applies to all existing topics and requires a restart. They act only as creation-time defaults for topics with `redpanda.storage.mode=unset`.

**Per topic, v26.1 and later (recommended).**

```bash
rpk topic create <topic_name> -c redpanda.storage.mode=tiered
rpk topic alter-config <topic_name> --set redpanda.storage.mode=tiered
```
With a mode other than `unset`, `redpanda.remote.read` and `redpanda.remote.write` have no effect.

**Legacy, mode `unset`.**

```bash
rpk topic create <topic_name> -c redpanda.remote.read=true -c redpanda.remote.write=true
rpk topic alter-config <topic_name> --set redpanda.remote.read=true --set redpanda.remote.write=true
```
At creation, topic-level true enables and false disables regardless of the cluster value; unset follows the cluster. Other properties: `redpanda.remote.recovery` (creation time only) and `redpanda.remote.delete` (topic deletion also removes its objects).

**Versions (26.2).** `tiered_v1` is the default. `tiered_v2` is beta, unsupported in production, and adds compaction on object storage including tombstone removal after `delete.retention.ms`. Default for new topics: `rpk cluster config set default_redpanda_storage_mode_tiered_impl=tiered_v2` (no restart). Per topic, set both `redpanda.storage.mode=tiered` and `redpanda.storage.mode.impl=tiered_v2` at creation. v2 topics need every broker on 26.2+; v1 and v2 cannot be converted; check with `rpk topic describe`.

## Checked

2026-11-04. Property names, commands, the resolution table and v2 restrictions were confirmed on the Tiered Storage page.

Method: documentation only; no commands were run.
