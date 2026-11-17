---
id: computing-software.devops-ci-cd.nomad.raft-peers
name: raft-peers
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, raft-remove-peer, raft, list-peers, outage-recovery, server-members, force-leave, peer-id, stale, cli]
level: advanced
status: docs-checked
description: "Inspect and repair the Nomad Raft peer set with nomad operator raft list-peers and remove-peer, when to prefer server force-leave, and using -stale during leaderless outages."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/operator/raft/list-peers.mdx", "https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/operator/raft/remove-peer.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad operator raft list-peers and remove-peer

Both need a **management token** when ACLs are enabled.

## list-peers
```
nomad operator raft list-peers
nomad operator raft list-peers -stale
```
Example columns: `Node`, `ID`, `Address`, `State`, `Voter`:
```
nomad-server01.global  10.10.11.5:4647  10.10.11.5:4647  follower  true
nomad-server02.global  10.10.11.6:4647  10.10.11.6:4647  leader    true
```
- `Node` is `(unknown)` for a stale entry the cluster no longer knows.
- `ID` is the same as the address but may become a GUID in a future version.
- `State` is `follower` or `leader`; `Voter` shows whether it has a vote.
- `-stale` (default false) reads from a non-leader server; needed when there is no leader.

## remove-peer
```
nomad operator raft remove-peer -peer-id 10.10.11.7:4647
```
Removes a server left in the Raft configuration after it vanished, so it stops counting toward quorum. If the server still appears in `nomad server members`, clean up with `nomad server force-leave` instead.

The docs point to the Outage Recovery guide for examples of how these commands are used.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 operator raft list-peers and remove-peer pages: management token, -stale, the output columns and meanings, -peer-id, force-leave preference. Removed: the four-step usage pattern and the take-a-snapshot-first advice.

Method: documentation only; no commands were run.
