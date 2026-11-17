---
id: computing-software.ai-ml-engineering.seldon-core-2.model-scheduling-onto-servers
name: model-scheduling-onto-servers
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, scheduling, scheduler, schedulefailed, capabilities, requirements, memory]
level: practitioner
status: docs-checked
description: "How the Seldon Core 2 Scheduler picks a Server for a Model: capability match, replica count, memory fit, preference for the current host, and the ScheduleFailed state."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/models/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scheduling Models onto Servers

Core 2 decouples Model and Server resources so many models can share one server replica (Pod). That means Core 2 schedules models onto server pods natively, using sorters and filters.

## Criteria
A candidate Server must satisfy all of these:
- Matching capabilities for the Model `spec.requirements`.
- Enough replicas to load the desired `spec.replicas` of the Model.
- Each Server replica has enough available memory for one model replica, as set by `spec.memory`.
- A Server that already hosts the Model is preferred, which reduces flip-flopping between candidates.

When a suitable server is found, Core 2 loads the model onto it. When none matches, the model is marked `ScheduleFailed`.

## Rule to remember
A given Model can be assigned to at most one Server, so that Server needs enough replicas to host every replica of the Model. If a model sits in `ScheduleFailed`, check these in order: requirements tags against Server capabilities, Server replica count against Model replicas, and Server memory against the model `memory` value.

The process is designed to be extensible, with more filters possible in future versions.

See the partial scheduling skill for loading fewer replicas than requested.

## Checked

Confirmed against the Scheduling page: native scheduling with sorters and filters, the four criteria, ScheduleFailed when no server matches, the one-server-per-model rule, and extensibility. The troubleshooting order in the last paragraph is a reading of those criteria, not a documented procedure.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb models/scheduling.md page (raw markdown).
