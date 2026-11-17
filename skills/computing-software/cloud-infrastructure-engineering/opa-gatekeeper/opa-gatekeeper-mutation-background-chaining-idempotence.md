---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-mutation-background-chaining-idempotence
name: opa-gatekeeper-mutation-background-chaining-idempotence
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, mutation, webhooks, chaining, idempotence, latency, external-data]
level: sme
status: docs-checked
description: "Understand why Kubernetes mutating webhooks chain and recurse, why group idempotence breaks, and how Gatekeeper mutators converge."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/mutation-background.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper mutation background chaining idempotence

Mutating webhooks are called in series; validating webhooks run in parallel. Mutation output can change what later webhooks see (one adds a sidecar, another sets imagePullPolicy on every container, including the new one). Latency therefore adds up across mutating webhooks, whereas validating latency is the slowest single webhook. Gatekeeper batches external-data references from many mutators into a single call per provider and calls providers in parallel to limit that cost.

Mutation also recurses, through the Kubernetes reinvocation policy and because controllers rewrite objects. Webhooks must be idempotent, but idempotent in isolation is not idempotent as a group. Example: one rule prepends `gcr.io/` unless present, another prepends `billing.company.com/` in the billing namespace unless present. Chained, they yield `billing.company.com/gcr.io/billing.company.com/gcr.io/my-favorite-image:latest`.

Gatekeeper mutation is designed so global idempotence is an emergent property of all mutators however configured; the project links a proof that its mutation language converges. Using Gatekeeper for mutation also reduces the number of separate mutation webhooks.

## Checked

2026-11-08: read the whole of website/docs/mutation-background.md in the Gatekeeper repo. Confirmed every claim, including the series versus parallel behaviour, the batched external data calls and the image prefix example; nothing removed.

Method: documentation only; no commands were run.
