---
id: computing-software.systems-network-administration.backup-and-recovery.chaos-engineering-game-days
name: chaos-engineering-game-days
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [chaos-engineering, game-day, fault-injection, resilience-testing, aws-fis]
level: advanced
status: docs-checked
description: "Run game days: program and scenario planning, AWS FIS experiment templates with stop conditions, running the simulation, and post-exercise review."
sources:
  - https://docs.aws.amazon.com/fis/latest/userguide/what-is.html
  - https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_testing_resiliency_game_days_resiliency.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chaos engineering game days

A game day is a scheduled exercise that simulates events in production-like environments to test systems, processes and team responses. The team performs the same actions it would if the event actually occurred.

## Planning (AWS Well-Architected REL12-BP05)
- Establish a program that defines frequency, scope and objectives; involve stakeholders and subject matter experts.
- Identify the business-critical services in focus; catalogue the people, processes and technologies behind them.
- Set the agenda, prepare the teams and prepare automation to simulate the scenarios and run recovery. The guide names AWS Fault Injection Service, Step Functions and Systems Manager for this.
- Inform all stakeholders in advance of date, time and scenarios, especially for the first game day, which should involve all team members. Include business decision makers.
- Game days can run on replicas of production built with infrastructure as code.

## AWS Fault Injection Service
- AWS FIS performs fault injection experiments based on chaos engineering principles. It carries out real actions on real AWS resources, so AWS strongly recommends a planning phase and running experiments in pre-production before production.
- An **experiment template** is the blueprint, containing actions, targets and stop conditions.
- An **action** is an activity on a resource, preconfigured by resource type, which can run for a duration and sequentially or in parallel. A **target** is one or more resources chosen individually or by criteria such as tags or state.
- A **stop condition** stops the experiment if a threshold you define as a CloudWatch alarm is reached.
- Single-account experiments must target resources in the same account; multi-account experiments reach other accounts.

## During
Run the planned scenario and observe and document how people, processes and technology react. If users are negatively affected, roll back the test and fix the issue by automation or by manual steps documented in the runbooks. CloudWatch and X-Ray can monitor behaviour.

## After
Hold a retrospective: record lessons learned, identify improvements, track changes to completion. Avoid the listed anti-patterns: documented procedures never exercised, stakeholders not informed, only technical failures covered, lessons not fed into recovery processes, and blaming teams.

## Gotchas
Game days without monitoring cannot show whether the problem was detected; AWS rates not establishing this practice a medium risk.

## Verify
Findings and action items are tracked to closure, and the next game day is scheduled.

## Checked

2026-11-09. Confirmed against the AWS FIS "What is AWS FIS?" page and Well-Architected REL12-BP05 "Conduct game days regularly". Removed: Principles of Chaos list and URL (not read), the steady-state and blast-radius wording, Azure Chaos Studio, Chaos Mesh, LitmusChaos, Gremlin, `tc netem` and `stress-ng`, the specific FIS fault list, and "game days that always pass are too gentle".

Method: documentation only; no commands were run.
