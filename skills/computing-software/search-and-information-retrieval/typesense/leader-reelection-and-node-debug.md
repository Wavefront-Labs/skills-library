---
id: computing-software.search-and-information-retrieval.typesense.leader-reelection-and-node-debug
name: leader-reelection-and-node-debug
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [raft-vote, leader-election, debug-endpoint, typesense]
level: advanced
status: docs-checked
description: "Force Typesense leader re-election with POST /operations/vote on a follower and read node role and version from GET /debug (state 1 leader, 4 follower)."
sources: ["https://typesense.org/docs/30.2/api/cluster-operations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leader re-election and debug

## Re-elect

`POST /operations/vote` triggers the follower node you call to start the Raft voting process, which triggers leader re-election. The follower you run it against becomes the new leader once the command succeeds.

## Debug

`GET /debug` returns debugging information about a node. `version` is the version of Typesense running. `state` tells the role: `1` is LEADER, `4` is FOLLOWER. Use it to find which node to target before a vote, or to confirm the result afterwards.

## Checked

Method: 2026-11-09 docs-only read of the cited Cluster Operations page in full. Confirmed both endpoints, the follower-becomes-leader behaviour and the state values. Removed the client-library form and example response bodies, which the page text does not show.
