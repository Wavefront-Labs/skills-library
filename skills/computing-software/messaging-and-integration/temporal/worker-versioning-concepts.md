---
id: computing-software.messaging-and-integration.temporal.worker-versioning-concepts
name: worker-versioning-concepts
category: computing-software
field: messaging-and-integration
product: temporal
tags: [worker-versioning, worker-deployment, build-id, pinned, auto-upgrade, ramping-version, draining, independent-activities]
level: practitioner
status: docs-checked
description: "Temporal Worker Versioning model: deployments, Build IDs, pinned versus auto-upgrade behavior, current, ramping and target versions, draining statuses and independent activities."
sources:
  - https://docs.temporal.io/worker-versioning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Worker Deployment is a logical service (named, for example, after your service) grouping Workers. A Deployment Version is deployment name plus Build ID; its Workers share a code build and report the version when they poll.

Each Workflow Type declares a Versioning Behavior in SDK config or the CLI:
- Pinned: guaranteed to finish on one Deployment Version. To move one, run `temporal workflow update-options`.
- Auto-Upgrade: moves to the latest version whenever Current changes; you must keep it replay-safe with patching.

Definitions:
- Current: where Workflows route unless pinned elsewhere; if none is set, default is unversioned.
- Ramping: receives a ramp percentage in [0, 100] of new and auto-upgrade Workflows; the remainder go to Current. Workflow ID decides which group a workflow falls in.
- Target: the version an Auto-Upgrade workflow upgrades to next (Current or Ramping).

Statuses: Inactive (a Worker polled but it never became Current or Ramping), Active (Current or Ramping), Draining (open pinned workflows remain; status refreshes periodically), Drained (all pinned workflows closed).

Activities start on their Workflow's version: pinned version for Pinned, Target version for Auto-Upgrade (the workflow moves to the Target just before starting the Activity). Independent Activities run on the Current or Ramping version of their own Task Queue instead, when that queue is outside the workflow's version: a separate Deployment holding only that Activity, an unversioned queue, or a Deployment with its own workflows reused by others.

## Checked

2026-11-08. Read in full on the Worker Versioning page: every concrete claim (names, events, rules, fields) matches the page.

Method: documentation only; no commands were run.
