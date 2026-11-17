---
id: computing-software.cybersecurity-defensive.threat-modelling.c4-model-threat-modelling
name: c4-model-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [c4-model, threat-modelling, architecture-diagrams, structurizr, trust-boundaries, dfd]
level: practitioner
status: docs-checked
description: "Reuse C4 diagrams as the threat model's system model: Structurizr DSL elements, relationships, tags and groups, with trust boundaries and protocols added."
sources: ["https://c4model.com/", "https://docs.structurizr.com/dsl/language", "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Threat_Modeling_Cheat_Sheet.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threat modelling on C4 diagrams

## What C4 gives you (c4model.com)
- Hierarchical abstractions: software systems, containers, components and code.
- Hierarchical diagrams: system context, containers, components and code, plus supporting
  diagrams: system landscape, dynamic and deployment.
- Notation independent and tooling independent, so the model can carry extra security
  information in whatever notation the team already uses.

## What the threat model needs (OWASP Threat Modeling Cheat Sheet)
System modelling answers "what are we working on?". Data flow diagrams are the most common
approach, but any model works if it gives a clear view of trust boundaries, data flows, data
stores, processes and the external entities that interact with the system, since these often
represent possible attack points. For complex systems, use a high-level overview alongside
more detailed diagrams of individual components. STRIDE categories can then be applied as
prompts to components, data flows and trust boundaries. Save the model in a form the team can
update.

## Adding security information to C4
1. Put protocol and authentication in each relationship's description or technology, and
   mark data classification on data stores (for example with tags), so a flow can be read as
   a data flow.
2. Represent trust boundaries with groups or deployment nodes (Structurizr supports both) so
   a boundary is part of the model rather than an annotation on a picture.
3. Record threats against element names so they can be traced back to the model.

## Structurizr DSL facts used above
- `softwareSystem <name> [description] [tags]` and
  `container <name> [description] [technology] [tags]` define elements; relationships use
  `<identifier> -> <identifier> [description] [technology] [tags]`.
- Elements and relationships can be tagged, and groups collect elements of the same level of
  abstraction. Deployment nodes can be nested.
- Example:
```
workspace {
  model {
    user = person "Customer"
    shop = softwareSystem "Shop" {
      spa = container "SPA" "" "React"
      api = container "API" "" "Go" "internet-facing"
      db  = container "Orders DB" "" "PostgreSQL" "pii"
    }
    user -> spa "Uses" "HTTPS"
    spa -> api "Calls" "HTTPS"
    api -> db "Reads and writes" "TLS"
  }
}
```

## Verify
- [ ] Every relationship crossing a trust boundary states protocol and authentication.
- [ ] Each recorded threat names an element that exists in the model.

## Checked
Confirmed 2026-11-09 against c4model.com (home page, read in full), the Structurizr DSL language reference (element and relationship syntax, tags, groups, deployment nodes) and the OWASP Threat Modeling Cheat Sheet (read in full).
Removed as unconfirmed: the recommendation of the container level as the default for threat modelling, the claim that C4 arrows are almost data flows, the views block (autolayout, include) which is documented on a page not read, the gotchas about shared infrastructure and asynchronous flows, and the Threat Modeling Manifesto source, which was not used.
Method: docs-checked 2026-11-09 against c4model.com, docs.structurizr.com dsl language and the OWASP Threat Modeling Cheat Sheet raw markdown
