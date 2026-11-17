---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.twelve-factor-assessment
name: twelve-factor-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor, twelve-factor-assessment, cloud-readiness, app-modernisation-assessment, cloud-native-checklist]
level: practitioner
status: draft
description: "Assess an existing application against the twelve factors: evidence per factor, scoring, remediation backlog and which gaps block containers, autoscaling or PaaS."
sources: ["https://12factor.net/", "https://learn.microsoft.com/dotnet/architecture/cloud-native/definition", "https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-net-applications-security/twelve-factor.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Twelve-factor assessment of an existing app

## Evidence per factor
| Factor | Check | Red flags |
|---|---|---|
| I Codebase | One repo per app, deploys from it | Copy-pasted forks per customer |
| II Dependencies | Declared and isolated (lockfile, image) | Relies on host-installed libraries |
| III Config | Env vars / external config | Config files per environment in repo, secrets in code |
| IV Backing services | Attached via URLs/credentials | Hard-coded hostnames, local DB assumption |
| V Build/release/run | Immutable artefacts promoted | Building on servers, editing in place |
| VI Processes | Stateless | Sticky sessions, local file uploads |
| VII Port binding | Self-contained HTTP | Requires external app server config |
| VIII Concurrency | Scale by processes | Only vertical scaling possible |
| IX Disposability | Fast start, graceful SIGTERM | Minutes to start, loses work on stop |
| X Dev/prod parity | Same backing services | SQLite dev vs Oracle prod |
| XI Logs | stdout event stream | Writes rotating log files |
| XII Admin processes | One-off tasks in same release | Manual SQL on prod servers |

## Steps
1. Gather evidence from code, deployment scripts and interviews.
2. Score each factor (met / partial / not met).
3. Map gaps to target platform needs: containers need II, III, VI, IX, XI; autoscaling needs VI,
   VIII, IX; PaaS needs VII, III, XI.
4. Create remediation backlog with effort; sequence before or during replatforming.

## Verify
- [ ] Assessment stored with evidence; blockers for the chosen 7 R path addressed.
