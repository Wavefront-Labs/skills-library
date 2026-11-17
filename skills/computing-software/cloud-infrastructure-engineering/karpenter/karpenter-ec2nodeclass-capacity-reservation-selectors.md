---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-capacity-reservation-selectors
name: karpenter-ec2nodeclass-capacity-reservation-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [capacityreservationselectorterms, odcr, capacity-block, instancematchcriteria, ownerid, beta, reserved]
level: advanced
status: docs-checked
description: "capacityReservationSelectorTerms (beta): select ODCRs by id, tags, instanceMatchCriteria and ownerID, priority over on-demand and spot, IAM actions, and status fields."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass capacityReservationSelectorTerms

Beta, gated by a feature flag in settings. Optional. Selects on-demand capacity reservations (ODCRs) for NodePools using this EC2NodeClass; Karpenter prioritises reservation capacity before falling back to on-demand and spot. Terms are ORed; conditions within a term are ANDed.

```yaml
spec:
  capacityReservationSelectorTerms:
  - id: cr-123
  - tags: {key: foo}
    ownerID: "012345678901"
  - instanceMatchCriteria: open
    tags: {key: foo}
```

- A term can use `id`, `tags`, `instanceMatchCriteria` (`open` or `targeted`) and an optional `ownerID`. Tag terms select all reservations accessible from the account with matching tags.
- IAM: the Karpenter role needs `ec2:DescribeCapacityReservations` and `ec2:RunInstances`.
- Resolved reservations appear in status with `id`, `availabilityZone`, `instanceType`, `instanceMatchCriteria`, `ownerID`, `reservationType` (`default` or `capacity-block`), `state` (`active` or `expiring`) and `interruptible`.
- The `CapacityReservationsReady` condition ("Referenced capacity reservations are discovered") is only present when the feature is enabled.
- Not in the page: the feature-gate name, `ownerID` format, how `open` versus `targeted` behave, and any NodePool capacity-type value for reserved capacity.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 nodeclasses.md page; removed the open/targeted semantics, the NodePool `reserved` capacity-type instruction and the Capacity Blocks selection claim as not stated. Priority, IAM and status fields unchanged.
