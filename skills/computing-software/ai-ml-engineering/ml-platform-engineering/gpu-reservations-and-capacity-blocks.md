---
id: computing-software.ai-ml-engineering.ml-platform-engineering.gpu-reservations-and-capacity-blocks
name: gpu-reservations-and-capacity-blocks
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, capacity-blocks, gpu-reservations, cost-optimization, on-demand-capacity-reservations, dynamic-workload-scheduler, capacity-planning]
level: practitioner
status: draft
description: "Secure scarce GPUs for training: AWS Capacity Blocks and capacity reservations, GCP reservations and Dynamic Workload Scheduler, commitments, and planning around them."
sources:
  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html
  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-reservations.html
  - https://cloud.google.com/compute/docs/instances/reservations-overview
  - https://cloud.google.com/kubernetes-engine/docs/how-to/provisioningrequest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU reservations and capacity blocks

**Goal:** have the GPUs when a training run is scheduled, without paying for idle reserved capacity the rest of the year.

## Options
| Option | Shape | Good for |
|---|---|---|
| On-demand | none guaranteed | small, flexible jobs; often unavailable for top GPUs |
| AWS EC2 Capacity Blocks for ML | fixed GPU cluster for a set future window (days to weeks), paid upfront | planned large training runs |
| AWS On-Demand Capacity Reservations (ODCR) | reserve instances in an AZ, billed whether used or not | steady inference/training baseline |
| SageMaker training plans | reserved capacity for SageMaker training/HyperPod | managed training on reserved GPUs |
| GCP reservations (specific/shared) | reserve VMs in a zone; can be consumed by GKE node pools | baseline capacity |
| GCP Dynamic Workload Scheduler (flex-start / calendar mode) | queue until all requested GPUs are free, then start together; calendar = fixed window | batch training that can wait |
| Committed use / Savings Plans | discount for spend commitment, not a capacity guarantee | long-running baseline |

Note: a discount commitment does **not** guarantee capacity; a reservation does. Check current durations and limits in the docs - these products change often.

## Planning around fixed windows
- Have the job fully tested on small capacity before the block starts; debugging on reserved H100s burns money.
- Checkpoint frequently and know your restart time; a node failure inside a block should cost minutes, not the window.
- Pre-stage data and container images in the same region/AZ; first-hour data copies waste the block.
- Queue follow-up jobs (evals, ablations) to fill the tail of the window.

## Kubernetes integration
- GKE: `ProvisioningRequest` with Kueue requests capacity via DWS; pods start only when all nodes are provisioned (avoids partial gang starts).
- EKS: launch Capacity Block instances through a launch template with the capacity reservation ID in a dedicated node group; label and taint them so only intended jobs land there.

## Gotchas
- Reservations are AZ/zone specific; your storage and other nodes must be there too.
- Unused reservation hours are not refunded - track utilisation of each reservation as a first-class metric.
- Multi-node training needs the right interconnect (EFA/placement groups on AWS, compact placement on GCP); reserve that topology, not just a GPU count.

## Verify
- [ ] Training job dry-run validated on small capacity before the window.
- [ ] Reservation utilisation tracked and reviewed after each window.
- [ ] Data and images staged in the reserved zone.
