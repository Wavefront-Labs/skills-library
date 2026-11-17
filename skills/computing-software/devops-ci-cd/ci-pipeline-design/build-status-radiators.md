---
id: computing-software.devops-ci-cd.ci-pipeline-design.build-status-radiators
name: build-status-radiators
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, build-radiator, pipeline-observability, ci-dashboards]
level: intro
status: docs-checked
description: "Make mainline build status visible to everyone: dashboards, chat notifications, physical displays and history views, and what the CI sources actually recommend."
sources: ["https://martinfowler.com/articles/continuousIntegration.html", "https://dora.dev/capabilities/continuous-integration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build status visibility and radiators

Continuous integration is about communication, so everyone should be able to see the state
of the system and of recent changes. The most important thing to communicate is the state of
the mainline build.

## What the sources recommend
- **Dashboards:** CI services have dashboards showing the state of the builds they run.
- **Chat:** they often link to other tools to broadcast build information to internal social
  media tools such as Slack; IDEs can have hooks so developers are alerted inside the tool
  they use. DORA agrees: notifications in a chat system are better than email, because
  many people ignore email or filter it out.
- **What to notify:** Fowler notes many teams only send notifications for failures, but he
  thinks it is worth sending messages on success too: people get used to the regular
  signals and get a sense of the build's length. (Team-dependent; this contradicts the
  common advice to alert on failures only.)
- **Physical displays:** teams sharing a space often use an always-on large screen with a
  simplified dashboard, valuable for alerting everyone to a broken build, often with
  red/green colours for the mainline commit build. Fowler cites red and green lava lamps
  (the idea: fix the build before the red lamp starts to bubble). DORA mentions klaxons
  or traffic lights for a broken build.
- **History:** displays can show recent history, an indicator of project health. Fowler's
  example is a wall calendar with a green or red square per day, depending on whether QA
  received one stable build that passed the commit tests.

## What to show (judgement, not from the sources)
Mainline commit-build status first; keep the radiator simple so a break is obvious at a
glance. Remove abandoned pipelines so they do not train people to ignore red.

## Verify
- [ ] The mainline build state is visible to the whole team without opening a tool.
- [ ] A broken mainline build reaches the team through a channel people actually read.
- [ ] The team has decided whether to notify on success as well as failure.

## Checked
Confirmed 2026-11-09 against Fowler's Continuous Integration article (section "Everyone can see what's happening", lines 738-775) and the DORA continuous integration capability page (status visibility, no email, chat notifications, klaxons or traffic lights). The originally cited martinfowler.com/bliki/BuildRadiator.html returned 404 and the DORA monitoring and observability page did not discuss CI radiators, so both were dropped from `sources`.
Removed as unconfirmed: the gh, GitLab and Jenkins API commands, tool names (Nevergreen, CCTray, Grafana exporters), "post only state changes", the 10-minute red escalation and the 5-minute visibility test.
Method: docs-checked 2026-11-09 against martinfowler.com continuousIntegration and dora.dev/capabilities/continuous-integration
