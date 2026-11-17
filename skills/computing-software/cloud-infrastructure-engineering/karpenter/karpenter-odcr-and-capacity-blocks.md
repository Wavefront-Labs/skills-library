---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-odcr-and-capacity-blocks
name: karpenter-odcr-and-capacity-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [odcr, capacity-reservation, capacity-block, reserved, interruptible, feature-gate]
level: advanced
status: docs-checked
description: "Using On-Demand Capacity Reservations and Capacity Blocks: ReservedCapacity gate, selector terms, the reserved capacity type, labels, prioritisation, expiry and draining."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/tasks/odcrs.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using ODCRs and Capacity Blocks

Native ODCR support arrived in v1.3, Capacity Blocks for ML in v1.6, interruptible reservations in v1.10. Enable the `ReservedCapacity` feature gate (beta).

EC2NodeClass selects reservations (terms are ANDed within a term, listed terms ORed):

```yaml
capacityReservationSelectorTerms:
- tags:
    application: foobar
- id: cr-56fac701cc1951b03
```

Capacity blocks are modelled as ODCRs and selected the same way. Open matching is not supported: every ODCR to use, even `open` ones, must be selected here.

NodePool must allow the dedicated capacity type `reserved`:

```yaml
requirements:
- key: karpenter.sh/capacity-type
  operator: In
  values: ['reserved', 'on-demand']
```

Labels, only on reserved nodes and usable in requirements and pod affinity: `karpenter.k8s.aws/capacity-reservation-id`, `karpenter.k8s.aws/capacity-reservation-type` (`default` or `capacity-block`), `karpenter.k8s.aws/capacity-reservation-interruptible` (`true`/`false`).

Behaviour:
- With `reserved`, `on-demand` and `spot` all allowed, Karpenter prefers ODCRs and falls back to spot/on-demand.
- Reservations are pre-paid, so they are modelled as free; consolidation moves spot/on-demand workloads onto them.
- If an instance leaves its ODCR (expired, cancelled, removed), the `karpenter.sh/capacity-type` label becomes `on-demand`.
- Capacity Blocks have an end time; EC2 starts terminating 30 minutes before (60 for UltraServer). Karpenter drains 10 minutes before EC2 starts.
- Interruptible ODCRs give a 2-minute EventBridge warning; Karpenter drains on receipt.

Migration: previously instances could land in open ODCRs by accident. Before enabling the gate, add the reservations to `capacityReservationSelectorTerms` and make NodePools compatible with `reserved`.

## Checked

2026-11-04. Confirmed against the ODCR task page (v1.13), NodeClasses concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
