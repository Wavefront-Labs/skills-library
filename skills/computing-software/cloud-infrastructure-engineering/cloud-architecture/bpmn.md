---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.bpmn
name: bpmn
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, business-architecture, bpmn, process-modelling, bpmn-2, swimlanes, process-automation, camunda]
level: practitioner
status: draft
description: "Model business processes in BPMN 2.0 at the right level (descriptive vs executable) to find automation, integration and event boundaries for cloud solutions."
sources: ["https://www.omg.org/spec/BPMN/2.0.2/", "https://docs.camunda.io/docs/components/modeler/bpmn/", "https://pubs.opengroup.org/togaf-standard/adm/chap04.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business process modelling (BPMN)

## Levels
- **Descriptive**: pools/lanes, tasks, start/end events, exclusive gateways - for business review.
- **Analytic**: adds message flows, intermediate events, error/timer events, data objects.
- **Executable**: fully specified for a workflow engine (Camunda/Zeebe, Flowable) or mapped to a
  cloud orchestrator (Step Functions, Logic Apps, Workflows).

## Core notation
- Pool = participant (organisation/system); lane = role within it.
- Sequence flow (solid) inside a pool; **message flow** (dashed) only between pools.
- Gateways: exclusive (X), parallel (+), inclusive (O), event-based. Always close what you open.
- Events: start, intermediate (timer, message, signal, error), end; boundary events on tasks for
  timeouts and errors.

## Using it for cloud architecture
1. Model the as-is process with the people who do it.
2. Mark manual hand-offs, waits and re-keying: automation candidates.
3. Message flows between pools = integration points (APIs or events).
4. Timer and boundary events = long-running workflow needs (durable orchestration, sagas).
5. Derive the to-be process and the services/events required.

## Gotchas
- Sequence flows crossing pools (invalid).
- Modelling every exception at descriptive level; keep happy path plus key exceptions.
- Unbalanced gateways that make the model ambiguous.

## Verify
- [ ] Model validates in the tool (no BPMN errors).
- [ ] Business owner walked through it and agreed.
