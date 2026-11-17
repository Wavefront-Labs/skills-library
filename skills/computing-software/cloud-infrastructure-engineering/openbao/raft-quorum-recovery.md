---
id: computing-software.cloud-infrastructure-engineering.openbao.raft-quorum-recovery
name: raft-quorum-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, raft, peers-json, quorum, remove-peer]
level: sme
status: docs-checked
description: "Recover an OpenBao raft cluster: remove-peer when quorum holds, raft/peers.json when quorum is lost, and the data-loss risks."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/integrated-storage/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raft quorum recovery

## Quorum still holds

Restore the failed server, or remove it:

```
bao operator raft list-peers
bao operator raft remove-peer
```

## Quorum lost

Partial recovery uses a `raft/peers.json` file in each remaining server's configured data path, listing only the surviving servers by `id`, cluster-port `address` and `non_voter` flag. Stop all remaining servers first, make the file identical on all of them, then restart. Confirm the servers you leave out have failed and will not rejoin. Servers introduced later can be fresh and join normally.

## Warnings

- Using `peers.json` can implicitly commit uncommitted log entries.
- Make sure no automated process puts the peers file in place on a schedule.
- Partial quorum-loss recovery may lose data, because committed state on the surviving servers may be incomplete.

For other, non-quorum related recovery, OpenBao's recovery mode can be used.

## Checked

2026-11-04. Read the OpenBao Integrated Storage concepts page in full (outage recovery sections). Confirmed: quorum-maintained options, the `peers.json` procedure and fields, the implicit commit of log entries, the warning about automated processes and the possible data loss. Removed: a snapshot recommendation and an `AppliedIndex` selection rule that the page does not state.
Method: documentation only; no commands were run.
