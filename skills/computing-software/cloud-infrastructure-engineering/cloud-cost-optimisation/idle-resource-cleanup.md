---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.idle-resource-cleanup
name: idle-resource-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimisation, idle-resource-cleanup, orphaned-resources, unattached-volumes, unused-elastic-ips, cloud-custodian]
level: practitioner
status: docs-checked
description: "Remove idle and orphaned AWS resources with Cloud Custodian: mark-for-op, notify owners, unmark if reused, then act after a grace period."
sources: ["https://cloudcustodian.io/docs/aws/examples/ebsgarbagecollect.html", "https://cloudcustodian.io/docs/aws/examples/eipgarbagecollect.html", "https://cloudcustodian.io/docs/aws/examples/elbgarbagecollection.html", "https://cloudcustodian.io/docs/aws/examples/rdsdeleteunused.html", "https://cloudcustodian.io/docs/quickstart/index.html", "https://www.finops.org/framework/capabilities/workload-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idle and orphaned resource cleanup

The FinOps Framework's Workload Optimization capability lists turning off idle resources
among optimisation opportunities, and its mature end state has automation that alerts on,
actions or cleans up idle and wasteful resources with minimal manual intervention.
Cloud Custodian's example policies show a safe pattern.

## The mark, unmark, act pattern
Cloud Custodian's `mark-for-op` action tags a resource with metadata about a future
operation (for example delete in n days). It does not perform the operation: a separate
policy that filters on `marked-for-op` must run on or after the marked date, and the
filter includes every resource marked up to and including the current date. A companion
policy unmarks (removes the tag from) resources that became compliant in the meantime.

Per the docs, three policies chain together per resource type:
1. Mark: find the unused resource that has no marker tag and mark it for the operation.
2. Unmark: if a marked resource is in use again, remove the marker tag.
3. Act: filter `marked-for-op` and run the action.

## Examples published in the Custodian docs
| Resource | Idle signal in the example | Grace period used | Action |
|---|---|---|---|
| EBS volume | `Attachments: []` | 30 days | `delete` |
| Elastic IP | `InstanceId` and `AssociationId` absent | 7 days | `release`, then notify |
| Classic ELB | `Instances: []` | 14 days | `delete`, with owner email |
| RDS instance | `DatabaseConnections` metric equal to 0 over 14 days, instance older than 14 days | staged over several policies | notify, stop hourly, then delete |

These grace periods are the example values in the docs, not recommendations. The RDS
example emails the resource owner at each stage, unmarks the database if connections
appear, and its final step uses `skip-snapshot: true`, so add your own snapshot step if
the data might matter. The `notify` action needs the Cloud Custodian mailer installed and
configured.

```yaml
policies:
  - name: ebs-mark-unattached-deletion
    resource: ebs
    filters:
      - Attachments: []
      - "tag:maid_status": absent
    actions:
      - type: mark-for-op
        op: delete
        days: 30
  - name: ebs-delete-marked
    resource: ebs
    filters:
      - type: marked-for-op
        op: delete
    actions:
      - delete
```

## Test before enabling
Validate a policy with `custodian validate custodian.yml`, and use
`custodian run --dryrun -s . custodian.yml` to see which resources it identifies without
acting.

## Verify
- [ ] Policies were dry-run and reviewed before any delete action was enabled.
- [ ] The act policy runs on a schedule that reaches the marked date.
- [ ] Owners are notified before deletion.

## Checked
Method: docs-checked 2026-11-09 against the Cloud Custodian example pages for EBS, EIP, ELB and RDS garbage collection, the quickstart (validate and dryrun), and the FinOps Framework Workload Optimization page (all fetched and read in full or grepped).
Removed as unconfirmed by the pages read: detection table for Azure and GCP disks, snapshots, idle VMs (CPU 5%, 14 days), NAT gateways, namespaces; AWS public IPv4 charging date; Trusted Advisor, Azure Advisor and GCP Recommender claims (unreadable hosts); stop/detach then snapshot then delete sequence stated as fact; finops-exempt tag convention; weekly idle report.
