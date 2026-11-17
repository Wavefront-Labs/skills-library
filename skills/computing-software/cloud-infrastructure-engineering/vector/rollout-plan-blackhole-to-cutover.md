---
id: computing-software.cloud-infrastructure-engineering.vector.rollout-plan-blackhole-to-cutover
name: rollout-plan-blackhole-to-cutover
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [rollout, migration, blackhole, vector-top, vector-tap, soak, cutover, vector]
level: practitioner
status: docs-checked
description: "Introduce Vector incrementally with a black hole, a data copy, a 24 hour soak and a safe cutover."
sources:
  - https://vector.dev/docs/setup/going-to-prod/rollout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The strategy is incremental adoption: one network partition and one system at a time, safe failure (Vector works on a redundant stream first), and no "big switch". By cutover Vector should already have run in production capacity for a sustained period.

Plan per network partition:

1. **Deploy a black hole.** Run Vector with a single `blackhole` sink (the default) in the partition. Size for the conservative 10 MiB/s/vCPU.
2. **Stream a copy.** Send a copy of data from agents to Vector. Confirm receipt with `vector top` and `vector tap`.
3. **Configure Vector.** Process the data for your use cases, connect downstream systems and verify the data in each destination.
4. **Size, scale and soak.** Enable autoscaling so it can scale down, then soak at least 24 hours while monitoring performance.
5. **Cut over.** Shut agents down so they drain without loss, reconfigure them to send only to Vector, restart them. Repeat for each partition.

Why it works: duplicate streams make failure harmless, and the soak removes doubt about performance before dependence.

## Checked

Method: docs-checked 2026-11-09 against the full Vector rollout page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced `vector tap` flag explanation, command block and verification line.
