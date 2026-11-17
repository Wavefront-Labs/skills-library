---
id: computing-software.messaging-and-integration.temporal.worker-entities-and-identity
name: worker-entities-and-identity
category: computing-software
field: messaging-and-integration
product: temporal
tags: [worker, worker-identity, worker-entity, worker-process, worker-program, pollers]
level: practitioner
status: docs-checked
description: "Temporal worker terminology: program, process, entity and identity, default identity format, container pitfalls, and how many open workflows one Worker can hold."
sources:
  - https://docs.temporal.io/workers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vocabulary:
- Worker Program: the static code built with an SDK that sets constraints for the process.
- Worker Process: the running process that polls a Task Queue, dequeues Tasks, runs your code and reports results. It can be a Workflow Worker, Activity Worker or both, and is external to the Temporal Service, which never executes your code.
- Worker Entity: one Worker inside a process, listening to exactly one Task Queue, containing a Workflow Worker and/or Activity Worker. Several entities per process means several queues.

Activity Worker processes need whatever the Activities need: network for external APIs, credentials for provisioning, GPUs for ML. Event History is protected in transit by mTLS but readable at rest unless you use the Data Converter API to encrypt payloads before they leave the Worker.

Capacity: Workers are stateless, so a blocked execution can be dropped from the cache and later resumed on any Worker. One Worker can therefore hold millions of open executions if update rate allows, at the price of latency.

Identity: SDKs default to process id at hostname (process.pid, then os.hostname()), shown in Event History and the Task Queue poller list. In Docker the PID is always 1; on Amazon ECS the hostname is random; sometimes it is an ephemeral IP. Set an explicit identity that ties to the environment (for example the ECS Task ID), adds context such as staging or production and region, is unique, and stays short.

## Checked

2026-11-08. Read in full on the Workers page: every concrete claim (names, events, rules, fields) matches the page. Removed the two tuning-guide paths: the page names the guides but the paths were not confirmed.

Method: documentation only; no commands were run.
