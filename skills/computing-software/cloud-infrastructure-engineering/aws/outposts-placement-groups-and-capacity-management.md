---
id: computing-software.cloud-infrastructure-engineering.aws.outposts-placement-groups-and-capacity-management
name: outposts-placement-groups-and-capacity-management
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, outposts, capacity-management, capacity-task]
level: practitioner
status: docs-checked
description: "Manage fixed AWS Outposts capacity: view it and reconfigure instance sizes with capacity tasks. Placement groups are not covered here."
sources: ["https://docs.aws.amazon.com/outposts/latest/userguide/outposts-capacity.html", "https://docs.aws.amazon.com/outposts/latest/userguide/view-capacity-management.html", "https://docs.aws.amazon.com/outposts/latest/userguide/modify-instance-capacity.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Outposts capacity management

## Capacity is finite
The compute and storage on an Outpost is determined by the size and number of assets installed at your site, so
you decide how much EC2, EBS and S3 on Outposts capacity to reserve. Plan headroom yourself.

## View
In the Outposts console, open the Outpost: Instance view shows the configured instances by size and family; Rack
view shows instances per asset and offers Modify instance capacity.

## Reconfigure with a capacity task
Each new order starts with a default capacity configuration; a capacity task converts it to the instance sizes and
quantities you want, for a whole Outpost or a single asset. Use the console, a JSON capacity configuration plan, or
the `StartCapacityTask` API (which exposes all supported instances).
- Only the account that owns the Outpost resources can run capacity tasks, not consumers.
- Assets can be isolated while a task runs: create one when you do not expect to launch new instances.
- Run instantly (shorter isolation, but it fails if instances need stopping) or keep trying periodically for 48 hours.
- Instances to keep as-is: select running instances you must not stop and keep enough of that size in the new configuration.
- Reconfiguring an instance family completely means stopping its running instances first, including those owned by other accounts or layered services.
- Sizes must come from instance families your asset model supports; over-provisioning an asset fails the task, and Auto-balance helps when mixing sizes in a family.

```bash
aws outposts list-capacity-tasks --outpost-identifier "$OUTPOST"
```
Use the console or `aws outposts start-capacity-task` to start a task; check the CLI reference for its options.

## Verify
- [ ] The task shows completed and Instance view matches the intended mix.

## Checked
2026-10-28. Confirmed in the AWS Outposts User Guide pages in `sources` (capacity management, view capacity, modify instance capacity); the command was checked with check_commands.
Removed (not confirmed on any fetched page): CloudWatch capacity metric names, rack and host spread placement groups, capacity reservations, Auto Scaling, Dedicated Hosts, the dry-run option and host-failure notes. The description now says placement groups are out of scope.
Method: documentation only; no commands were run.
