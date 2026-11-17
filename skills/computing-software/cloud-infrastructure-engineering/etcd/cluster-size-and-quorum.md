---
id: computing-software.cloud-infrastructure-engineering.etcd.cluster-size-and-quorum
name: cluster-size-and-quorum
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [cluster-size, quorum, fault-tolerance, odd-members, majority, members, sizing]
level: intro
status: docs-checked
description: "Quorum arithmetic for etcd: majority size and tolerated failures for 1 to 9 members, and why odd sizes are better."
sources:
  - "https://etcd.io/docs/v3.5/faq/"
  - "https://etcd.io/docs/v3.5/op-guide/failures/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Quorum is a majority: (n/2)+1 members for n members (rounded down). The cluster operates as long as a member quorum can be established.

Members, quorum, failures tolerated (the FAQ table):

- 1: quorum 1, tolerates 0
- 2: quorum 2, tolerates 0
- 3: quorum 2, tolerates 1
- 4: quorum 3, tolerates 1
- 5: quorum 3, tolerates 2
- 6: quorum 4, tolerates 2
- 7: quorum 4, tolerates 3
- 8: quorum 5, tolerates 3
- 9: quorum 5, tolerates 4

Takeaways:

- An even size tolerates the same number of failures as the odd size below it, so choose odd numbers. Adding a member to reach an even size buys no extra fault tolerance.
- During a network partition, an odd number of members guarantees there is always a majority partition that can keep operating.
- More members does not mean more write throughput: the FAQ says write performance suffers because data must be replicated across more machines. A cluster should probably have no more than seven nodes; a 5-member cluster tolerates two failures, which is enough in most cases.
- Losing a majority stops the cluster from accepting writes. It recovers when a majority of members is available again; if a majority cannot return, disaster recovery is needed.
- Fewer than half of the followers failing does not disrupt the cluster: two follower failures do not affect a five-member cluster.

## Checked

2026-11-08. Read in full: etcd v3.5 FAQ and Failure modes pages. Confirmed the quorum formula, the size table (including 8), the odd-size argument, the seven-node guideline and the failure behaviour. Removed: learners and proxies not counting toward quorum, availability-zone placement advice, the 3 to 5 learner reconfiguration step and the member list command (none of these are on the two cited pages).
Method: documentation only; no commands were run.
