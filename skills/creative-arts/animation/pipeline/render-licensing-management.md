---
id: creative-arts.animation.pipeline.render-licensing-management
name: render-licensing-management
category: creative-arts
field: animation
product: pipeline
tags: [render-licensing, licence-management, license-server, floating-licences, limit-groups, render-farm, flexlm]
level: advanced
status: draft
description: "Manage render licences on a farm: node-locked versus floating models, licence servers and ports, limits per renderer, failure handling, usage tracking and costs."
sources:
  - https://docs.thinkboxsoftware.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Render licence management

Renderers, plug-ins and DCC applications often require licences for each concurrently running task. Plan for them as a limited resource.

## Models
- **Free/open**: some renderers (for example Blender's Cycles) need no licence for render nodes.
- **Node-locked**: tied to a machine; poorly suited to dynamic farms.
- **Floating (network)**: a licence server hands licences to hosts on request; common managers include FlexNet (FlexLM), RLM and vendor-specific servers. The pool size limits concurrent use.
- **Subscription/online**: user or machine tokens validated online; check what the vendor allows for render nodes and cloud workers.
- Terms differ by product: some include a number of render licences with each artist seat, others sell render nodes separately. Read each vendor's current licensing documentation.

## Farm configuration
1. **Reachability**: the licence server must be reachable from every render host, with the right ports open (vendor docs list them) and stable hostnames.
2. **Environment variables** or config files point each renderer at its server (`rez-package-environments.md`).
3. **Limits**: tell the render manager how many licences exist so jobs wait instead of failing. Thinkbox Deadline has *Limits* (limit groups) for this; other managers have equivalents, for example resource or limit features in OpenCue (check docs for your version).
4. Put licence-hungry jobs behind limits; give priority to important jobs.
5. **Failure handling**: configure retries with delay for licence-checkout failures; do not count them as scene errors.

## Monitoring
- Track **usage over time** with the licence manager's reports or logs, to plan purchases and spot hogs, such as idle sessions that hold a licence.
- Alert when the server is unreachable or the pool is exhausted.
- Keep the licence files and server config in backup (`backup-strategy-3-2-1.md`).

## Cost
- Include licences in the render budget (`render-time-estimation-and-budgets.md`) and cloud burst plans: check that cloud workers can use licences from your server or use usage-based licensing.

## Verify
- [ ] Limit values match the purchased pool.
- [ ] A test job on each OS gets a licence.
- [ ] Usage reporting is available and reviewed.
