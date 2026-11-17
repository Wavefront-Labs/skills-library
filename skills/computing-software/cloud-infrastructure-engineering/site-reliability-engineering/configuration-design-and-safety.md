---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.configuration-design-and-safety
name: configuration-design-and-safety
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, configuration-design, config-safety, configuration-best-practices, configuration-management, config-validation, config-rollback, defaults, mandatory-vs-optional]
level: advanced
status: docs-checked
description: "Design and ship configuration so it stops causing outages, following the SRE Workbook: minimal knobs, safe defaults, tooling, ownership, gradual rollout and rollback."
sources: ["https://sre.google/workbook/configuration-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration design and safety

**Goal:** configuration changes are as safe as code changes, and the configuration surface is small enough
that humans get it right. Source: SRE Workbook chapter 14, "Configuration Design and Best Practices".

## 1. Why configuration deserves engineering
Configuration is a human-computer interface for modifying system behaviour. Unlike code, one changed option
can have dramatic effects (one bad firewall rule can lock you out), and configuration often lives in an
untested or untestable environment. It may be changed under pressure during incidents. Design it like an
API and a UI, purposefully, not as a side effect of implementation.

## 2. Philosophy
- Ideal: no configuration at all. Minimise questions; favour the user-centric view; questions close to user goals.
- Minimise mandatory questions by providing safe defaults, static or dynamic. Most users use the default.
- Add knobs only for a real need; allow optional overrides for power users.

## 3. Mechanics
- Separate configuration from resulting data: infrastructure operates on plain static data (for example
  Protocol Buffers, YAML or JSON), and users may use a higher-level interface that generates it (a DSL,
  Jsonnet, or a web UI). Avoid tight coupling between the interface format and the internal data format.
- Store metadata on how configuration was ingested, to find authors.
- Tooling: semantic validation at commit time; syntax highlighting, a linter and an automatic formatter.
- Ownership and versioning: a clear owner per snippet, versioned history, and logged changes and applications.

## 4. Safe application of a change
A change is safe when it has three properties:
1. It can be deployed gradually, not all-or-nothing (avoid a global all-at-once push; abort a problematic push before a 100% outage).
2. It can be rolled back (rolling back usually mitigates faster than a temporary fix).
3. It rolls back automatically, or at least stops progressing, if it leads to loss of operator control.

Rollback needs hermetic configuration: configuration referencing external resources that can change (for
example data on a network filesystem) is hard to roll back. Be careful with changes that can cut off operator
control, such as firewalling yourself out; desktop display settings that revert unless confirmed are the
chapter's analogy. The same principles apply to binary upgrades and data pushes.

## 5. Reviewing a configuration surface
Count the knobs; for each, ask whether it is mandatory, whether it could be inferred or defaulted, and
whether it has a real use case. Delete or default what you can.

## Gotchas
- Whitespace-oriented formats: incorrect indentation can have great consequences; standard formatting helps prevent it.
- Committing a configuration does not necessarily apply it, so track both.

## Verify
- [ ] Changes roll out gradually and can be rolled back; the configuration is hermetic.
- [ ] Semantic validation runs at commit time; every snippet has an owner and versioned history.

## Checked
2026-11-01. Confirmed against SRE Workbook chapter 14 (sre.google/workbook/configuration-design/): philosophy, mechanics, data separation, tooling, ownership, safe change application and hermetic configuration.
Removed: the Helm, kubeconform, conftest, promtool, otelcol, CUE and Jsonnet command lines and comparisons, the Kubernetes ConfigMap checksum pattern, admission-controller names, drift-detection tools, feature-flag hygiene rules and metric names, and the canary-subset check, because chapter 14 does not state them.
Method: documentation only; no commands were run.
