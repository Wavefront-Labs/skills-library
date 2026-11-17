---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-task-placement-strategies-and-constraints
name: ecs-task-placement-strategies-and-constraints
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, placement-strategy, placement-constraints, binpack, spread, cluster-query-language]
level: practitioner
status: docs-checked
description: "Place ECS tasks on EC2 capacity deliberately: spread by AZ then binpack by memory, distinctInstance and memberOf constraints with cluster query language, and custom attributes."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html", "https://docs.aws.amazon.com/scheduler/latest/APIReference/API_EcsParameters.html", "https://github.com/aws/amazon-ecs-agent/blob/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS task placement strategies and constraints

Applies to the **EC2 launch type** and EC2 capacity providers; the ECS guide describes strategies and constraints for tasks on container instances. Fargate places tasks itself across the AZs of the subnets you give it.

## 1. Order of evaluation
1. Find instances that satisfy CPU, memory, ports (and GPU, ENI) requirements.
2. Apply **constraints** (filter).
3. Apply **strategies** in order. Strategies are best effort; constraints are binding and can prevent placement. The API accepts up to 5 strategy items.

## 2. Strategies
| Type | Field | Effect |
|---|---|---|
| `spread` | `attribute:ecs.availability-zone`, `instanceId` (or `host`), any attribute | even distribution |
| `binpack` | `cpu` or `memory` | least unused CPU or memory, fewest instances |
| `random` | - | random |
Common production choice:
```json
"placementStrategy": [
  {"type": "spread", "field": "attribute:ecs.availability-zone"},
  {"type": "binpack", "field": "memory"}]
```
AZ resilience first, then cost efficiency within each AZ. Pure binpack can put all tasks on
one instance (one failure takes everything); pure spread by instanceId wastes capacity.
For services the default strategy is `spread` on `attribute:ecs.availability-zone`; set the strategy explicitly in IaC so it is visible.

## 3. Constraints
- `distinctInstance`: each active task on a different instance. It can be set on RunTask and CreateService only, and ECS looks at desired status, so a task being stopped can briefly share an instance. For strong isolation the ECS guide suggests Fargate.
- `memberOf` with a **cluster query language** expression:
```json
"placementConstraints": [
  {"type": "memberOf", "expression": "attribute:ecs.instance-type =~ g5.*"},
  {"type": "memberOf", "expression": "attribute:ecs.availability-zone in [eu-west-1a, eu-west-1b]"},
  {"type": "memberOf", "expression": "attribute:workload == batch and attribute:ecs.os-type == linux"}]
```
Built-in attributes: `ecs.ami-id`, `ecs.availability-zone`, `ecs.instance-type`,
`ecs.os-type`, `ecs.os-family`, `ecs.cpu-architecture`, `ecs.vpc-id`, `ecs.subnet-id`.
Expressions support `==`, `!=`, `in`, `!in`, `=~` (Java regular expression), `exists`, `and`, `or`, `not`. Task groups: `task:group == service:production` for affinity and `not(task:group == database)` for anti-affinity.

## 4. Custom attributes
```bash
aws ecs put-attributes --cluster prod --attributes \
  name=workload,value=batch,targetType=container-instance,targetId=<container-instance-arn>
```
Or set at boot in `/etc/ecs/ecs.config`: `ECS_INSTANCE_ATTRIBUTES={"workload":"batch"}` (takes effect only at first registration; use PutAttributes afterwards).
Attribute names and values are 1-128 characters. Use them to pin workloads to instance pools.

## 5. Interaction with capacity providers
With capacity provider strategies, managed scaling launches instances to fit pending
tasks. Constraints that no instance type in the ASG can satisfy leave tasks unplaced. Keep constraints consistent with what the ASG can launch;
separate capacity providers (and ASGs) per instance class are cleaner than complex
constraints.

## 6. Testing an expression
```bash
aws ecs list-container-instances --cluster prod --filter "attribute:ecs.instance-type =~ g5.*"
```
An empty result means no container instance matches, so a task with that constraint stays `PENDING`.

## Gotchas
- Strategies and constraints on a **service** can be updated (`update-service
  --placement-strategy`) and apply to new tasks; existing tasks are not moved. Force a new
  deployment to rebalance.
- `distinctInstance` with more desired tasks than instances leaves tasks pending.
- Host port mapping (bridge mode with static ports) limits one task per instance per port;
  use dynamic ports or awsvpc.

## Verify
- [ ] `describe-tasks` shows replicas spread across AZs and instances as intended.
- [ ] Constraint expressions return matching instances via `list-container-instances --filter`.
- [ ] Killing one instance leaves the service serving from other AZs.

## Checked
Checked 2026-10-24 against the ECS developer guide (task placement strategies, constraints and attributes, cluster query language), the EventBridge Scheduler EcsParameters reference (strategy limit of 5) and the amazon-ecs-agent README.
Confirmed: strategy types and fields, default spread by AZ for services, constraint evaluation order, distinctInstance and memberOf, built-in attributes, operators, task:group examples, custom attribute name/value limits, ECS_INSTANCE_ATTRIBUTES behaviour, memberOf updatable on running services while distinctInstance is not.
Removed as unconfirmed: console versus API default differences, the PROVISIONING state claim, managed scaling remark, wording that Fargate ignores strategies.

Method: documentation only; no commands were run.
