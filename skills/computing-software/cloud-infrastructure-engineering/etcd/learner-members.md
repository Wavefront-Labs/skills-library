---
id: computing-software.cloud-infrastructure-engineering.etcd.learner-members
name: learner-members
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [learner, non-voting, member-promote, learner-add, catch-up, raft-learner, cluster-expansion]
level: advanced
status: docs-checked
description: "Add a non-voting learner member, wait for it to catch up and promote it, with limits and request restrictions."
sources:
  - "https://etcd.io/docs/v3.5/learning/design-learner/"
  - "https://etcd.io/docs/v3.5/op-guide/runtime-configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A learner is a member that receives log replication but does not vote, so it does not count toward quorum. Adding a member as a learner first makes adding a new member safer and reduces cluster downtime.

Workflow:

```bash
etcdctl member add node4 --peer-urls=http://10.0.1.14:2380 --learner
# start node4 with --initial-cluster-state existing (the member add output prints ETCD_INITIAL_CLUSTER_STATE=existing)
etcdctl member promote MEMBER_ID
```

Rules from the learner design document:

- In v3.4 the server limits a cluster to one learner (adding a second fails with `etcdserver: too many learner members in cluster`), to limit the extra load on the leader.
- A learner rejects client reads and writes, so the client balancer must not route requests to it, and leadership cannot be transferred to it. Do not list it in client endpoints.
- `member promote` fails with `etcdserver: can only promote a learner member which is in sync with leader` if the learner's log is too far behind; retry after it catches up.
- Promoting a member that is not a learner fails with `etcdserver: can only promote a learner member`.
- A learner never promotes itself; the operator makes the final decision.

Why it helps: a learner receives all data from the leader but does not change the size of the quorum, so misconfiguration stays reversible without losing quorum. Only after promotion does it count toward quorum.

The design document says member list and member status responses indicate which node is a learner.

## Checked

2026-11-03. Confirmed on the v3.5 learner design page and runtime reconfiguration guide: learner introduced in v3.4 as a non-voting member that still receives data, member add --learner and member promote commands, ETCD_INITIAL_CLUSTER_STATE=existing, promotion only after the log catches up, the one-learner limit in v3.4 and its error, the promote error messages, learner rejects client reads and writes, never promotes itself. Removed: the no-quorum promotion, removal and Raft-commit statements, the muddled serializable-read claim, and the IS LEARNER column on endpoint status/member list (the page only says responses should indicate the learner).

Method: documentation only; no commands were run.
