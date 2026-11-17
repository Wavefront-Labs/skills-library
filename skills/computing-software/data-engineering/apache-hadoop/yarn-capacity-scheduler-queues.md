---
id: computing-software.data-engineering.apache-hadoop.yarn-capacity-scheduler-queues
name: yarn-capacity-scheduler-queues
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, capacity-scheduler, queues, capacity, acl]
level: practitioner
status: docs-checked
description: "YARN Capacity Scheduler queue setup: root.queues, capacity and maximum-capacity, user limits, ACLs, application limits, resource calculator, and refreshQueues."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity Scheduler queues

Enable in yarn-site.xml: `yarn.resourcemanager.scheduler.class` = `org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler`. Configure queues in capacity-scheduler.xml. Queue paths start at the predefined `root` and use dots; children do not inherit properties unless noted.

- `yarn.scheduler.capacity.root.queues`: comma-separated children of root; deeper levels use `yarn.scheduler.capacity.<queue-path>.queues`.
- `<queue-path>.capacity`: percentage (float), weight with postfix w (e.g. 2.0w), or absolute resources like `[memory=10240,vcores=12]`. With percentages, siblings at each level must sum to 100. Root is fixed at 100%. Apps may exceed capacity when resources are free (elasticity). With weights, capacity is each weight over the sibling sum, and children of one parent must use the same mode. The Universal Capacity Vector format needs `yarn.scheduler.capacity.legacy-queue-mode.enabled` = false (default true).
- `<queue-path>.maximum-capacity`: elastic ceiling; -1 sets 100%; must be percentage when capacity is percentage or weight.
- `minimum-user-limit-percent` (default 100) and `user-limit-factor` (default 1, -1 disables), settable globally as `yarn.scheduler.capacity.<property>` or per queue. Example from the page: at 25, two users get at most 50% each, three 33%, four or more 25%.
- `<queue-path>.state`: RUNNING or STOPPED; STOPPED blocks new submissions to the queue and its children while existing apps finish. A queue is only deleted once STOPPED with no pending or running apps.
- `<queue-path>.acl_submit_applications` and `acl_administer_queue`: user and group lists in the form `user1,user2 group1,group2`; `*` means anyone, a single space means no one; inherited from the parent, and root defaults to `*`. A user or group with rights on a parent queue also has them on its children.
- `yarn.scheduler.capacity.maximum-applications`: default 10000, hard limit, extra submissions are rejected. `maximum-am-resource-percent`: default 0.1. Both can also be set per queue. `max-parallel-apps` (no limit by default) leaves excess apps ACCEPTED instead of rejecting them; there are per-user variants `yarn.scheduler.capacity.user.max-parallel-apps`.
- `yarn.scheduler.capacity.resource-calculator`: default `org.apache.hadoop.yarn.util.resource.DefaultResourceCalculator` compares memory only; `DominantResourceCalculator` handles multi-dimensional resources such as memory and CPU.

Queue mapping: `yarn.scheduler.capacity.queue-mappings` as `[u or g]:[name]:[queue_name][,next_mapping]*`, evaluated left to right with the first valid mapping used. Placeholders: `%user`, `%primary_group`, `%secondary_group`. `yarn.scheduler.capacity.queue-mappings-override.enable` defaults false.

Applying changes: with the default file-based store, edit capacity-scheduler.xml and run `yarn rmadmin -refreshQueues`. Alternatively add `QueueConfigurationAutoRefreshPolicy` to the monitor policies for periodic refresh (monitor must be enabled; interval default 5000 ms). If `yarn.scheduler.configuration.store.class` is set to an API-mutation store (memory, leveldb, zk), `-refreshQueues` is disabled; that API feature is marked alpha.

## Checked

Method: 2026-11-08, read the project's CapacityScheduler markdown source in full for the queue-configuration, limits, ACL, mapping, calculator and refresh sections. Removed an unsupported "Verify" step (RM scheduler UI); corrected the vague defaults wording and added weights, ACL format, the parallel-apps limit and periodic refresh from the page. Property names and defaults were otherwise unchanged.
