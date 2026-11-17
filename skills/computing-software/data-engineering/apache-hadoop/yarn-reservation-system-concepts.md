---
id: computing-software.data-engineering.apache-hadoop.yarn-reservation-system-concepts
name: yarn-reservation-system-concepts
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, reservation-system, rdl, admission-control]
level: advanced
status: docs-checked
description: "YARN ReservationSystem model: RDL, ReservationAgent, Plan, SharingPolicy, PlanFollower and replanning, and how a job joins a reservation via its ReservationId."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ReservationSystem.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reservation system

The ReservationSystem, a ResourceManager component, lets users reserve resources over and ahead of time so important production jobs run predictably. It does admission control and guarantees absolute amounts of resources (not a percentage of the cluster). Reservations can be malleable or have gang semantics, and can vary over time.

Setup: mark any leaf queue in capacity-scheduler.xml or fair-scheduler.xml as available for reservations (the property names are on the CapacityScheduler and FairScheduler pages, not here). The queue's capacity or fair share can then be used for reservations.

Parts:
- RDL (Reservation Definition Language): resource needs over time (a skyline) plus temporal constraints such as a deadline.
- ReservationAgent: finds a plausible allocation in the Plan.
- Plan: tracks accepted reservations and available resources.
- SharingPolicy: enforces invariants and may reject reservations. Example `CapacityOvertimePolicy` limits both instantaneous max capacity across a user's reservations and the integral over a period (the page's example: up to 50% instantaneously, but no more than 10% average in any 24h).
- PlanFollower: publishes the plan to the scheduler by dynamically creating, tweaking or destroying queues.
- Replanning: to adapt to capacity drops, it moves a reservation if possible, otherwise rejects the smallest amount of previously accepted reservation so others get their full amount.

Flow:
1. Step 0: submit a reservation creation request; the response holds the ReservationId.
2. Step 1: submit the RDL with that ReservationId, via the client-to-RM protocols or the RM REST API. Same id and same RDL succeeds without creating a new reservation; same id with different RDL is rejected.
3. Steps 2-4: the agent finds an allocation, the SharingPolicy validates it, and a ReservationId is returned (think airline ticket).
4. Steps 5-7: at the due time the PlanFollower publishes the plan; submit one or more jobs to the reservable queue with the ReservationId in the `ApplicationSubmissionContext`. Containers come from a special queue; within the reservation access is guaranteed, above it normal Capacity/Fairness sharing applies.

Jobs submitted to the reservable queue without a reservation run best-effort in whatever capacity is left over by active reservations.

## Checked

Method: 2026-11-08, read the project's ReservationSystem markdown source in full against this skill. Removed an unsupported "Verify" step; added Fair Scheduler support, guarantee semantics and the sharing-policy example from the page. The flow and component definitions were unchanged.
