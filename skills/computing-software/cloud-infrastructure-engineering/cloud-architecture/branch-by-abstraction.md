---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.branch-by-abstraction
name: branch-by-abstraction
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, branch-by-abstraction, refactoring, trunk-based-development, strangler-fig]
level: practitioner
status: draft
description: "Replace a component inside a running system with branch by abstraction: introduce an abstraction layer, migrate callers, switch implementations behind a toggle, remove the old."
sources: ["https://martinfowler.com/bliki/BranchByAbstraction.html", "https://www.branchbyabstraction.com/", "https://trunkbaseddevelopment.com/branch-by-abstraction/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Branch by abstraction during modernisation

## When
The component to replace is called from inside the codebase (a persistence layer, a messaging
library, an internal module), so a strangler fig at the edge cannot intercept it, and a long
-lived feature branch would rot.

## Steps
1. **Create an abstraction** (interface) that captures what callers need from the old
   component, not its whole surface.
2. **Move callers** to the abstraction one at a time, committing to trunk; the old
   implementation sits behind it. The system stays releasable throughout.
3. **Build the new implementation** behind the same abstraction (e.g. a cloud-managed queue
   client replacing an on-prem broker library).
4. **Switch with a toggle** per caller or per percentage; run both and compare outputs
   (dark launching / parallel run) for risky paths.
5. **Remove the old implementation** once all callers use the new one, and delete the toggle.
   Optionally remove the abstraction if it has no other value.

## Gotchas
- Abstractions that mirror the old component's API leak its design into the new one.
- Forgotten toggles accumulate; give each a removal date.
- Data migration is separate; pair with dual writes or CDC when the component owns state.

## Verify
- [ ] Trunk stayed releasable throughout (no long-lived branch).
- [ ] Old implementation and toggle deleted.
