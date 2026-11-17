---
id: computing-software.systems-network-administration.patch-management.blue-green-deployment
name: blue-green-deployment
category: computing-software
field: systems-network-administration
product: patch-management
tags: [blue-green-deployment, deployment-management, release-management, rollback-plan, load-balancer-drain, immutable-infrastructure]
level: practitioner
status: docs-checked
description: "Run blue-green deployments for infrastructure and app releases: two matching environments, switch the router, roll back by switching back, and handle database schema changes."
sources:
  - https://martinfowler.com/bliki/BlueGreenDeployment.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blue-green deployment

Keep two production environments, as identical as possible. One (say blue) is live. Do final
testing of the new release (or patched OS image) in the other (green). When green works,
switch the router so all incoming requests go to green; blue goes idle.

## Steps
1. **Build green** with the same configuration as blue (use the same IaC for both so they
   cannot drift).
2. **Test green** in its final stage before it takes any live traffic.
3. **Switch** the router so all requests go to green. Variations: bounce the web server
   instead of changing the router, or share one database and blue-green only the web and
   domain layers.
4. **Observe** green before declaring the release done.
5. **Roll back** by switching the router back to blue. Keep blue intact until you are happy
   with green's stability.
6. **Cycle**: use blue as the staging environment for the next release, then switch green to
   blue the same way. The two environments alternate between live, previous version (for
   rollback) and staging.

## Missed transactions
After a switch, transactions handled by green may be missing from blue. Depending on design,
feed transactions to both environments so blue stays a usable backup, or put the application
in read-only mode before cut-over, run read-only for a while, then switch to read-write.

## Databases
Separate the deployment of schema changes from the application upgrade. First apply a
database refactoring that supports both the old and new application versions, deploy it,
and check everything works (this is a rollback point). Then deploy the new application.
When it has bedded down, remove database support for the old version.

## Infrastructure patching use
For stateless tiers, build green from the patched image and switch, instead of patching in
place. The same mechanism as a hot standby, so each release also exercises your
disaster-recovery procedure.

## Verify
Rehearse the switch and the rollback, and record the rollback trigger criteria in the change
record.

## Checked
2026-11-08. Confirmed against Martin Fowler's BlueGreenDeployment page: two near-identical
environments, router switch, rollback by switching back, missed-transaction options, hot
standby and disaster-recovery testing, server-bounce and shared-database variations, and
the schema-separation approach. Removed claims that the page does not make: specific load
balancer products, weighted 10/50/100 shifts, session, queue and cache handling, cost and
websocket notes, and the unreadable ITIL source.
Method: documentation only; no commands were run.
