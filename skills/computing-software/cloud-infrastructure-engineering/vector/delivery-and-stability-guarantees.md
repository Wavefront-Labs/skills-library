---
id: computing-software.cloud-infrastructure-engineering.vector.delivery-and-stability-guarantees
name: delivery-and-stability-guarantees
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [guarantees, at-least-once, best-effort, stability, beta, alpha, vector]
level: practitioner
status: docs-checked
description: "Read Vector's delivery guarantee and stability labels so you can pick components for production."
sources:
  - https://vector.dev/docs/architecture/guarantees/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each component is labelled by delivery guarantee and by stability.

**Delivery guarantees**

- At-least-once: an event received by a component is ultimately delivered at least once. Rarely it can be delivered more than once, and the docs have an FAQ on exactly-once delivery. To keep it across restarts, the sink needs a disk buffer.
- Best-effort: Vector tries but cannot guarantee delivery, usually due to protocol limits. This is not the same as at-most-once, because duplicates are still possible in extreme cases.

```yaml
sinks:
  my_sink_id:
    buffer:
      type: disk
      when_full: block
      max_size: 104900000
```

**Stability labels**

- Stable: generally more than 4 months of community testing, stable API, no major open bugs, positive production signal.
- Beta: not yet meeting those criteria; use with caution in production.
- Alpha: experimental and incomplete; for early testing only.
- Deprecated: to be removed in the next major version, with time to transition.

Use the components page filters to see which sources and sinks support given guarantees, and check the badge at the top of each reference page.

Verify a component's label on its reference page before depending on it.

## Checked

2026-11-03. Read architecture/guarantees. Confirmed: at-least-once and best-effort definitions, the disk-buffer example, and the stable, beta, alpha and deprecated criteria including the 4-month guideline. Removed: the claim that trace support is alpha, which the page does not state.

Method: documentation only; no commands were run.
