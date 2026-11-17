---
id: computing-software.devops-ci-cd.gitlab-runner.runner-fleet-sizing
name: runner-fleet-sizing
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [fleet, capacity-planning, shared-runners, instance-runners, workload]
level: advanced
status: docs-checked
description: "Plan a shared runner fleet around workload, environment and capacity."
sources: ["https://docs.gitlab.com/runner/fleet_scaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Planning a runner fleet

Before deploying, the docs ask you to:
- list the teams to onboard and the languages, frameworks and libraries they use;
- estimate CI/CD jobs per team per hour and per day;
- check whether any team has build requirements that containers cannot meet, or that suit dedicated runners;
- estimate the compute capacity needed.

Different fleets can run on different stacks, for example public cloud and on-premises. Job performance depends on the fleet environment, and hosting a large number of resource-intensive jobs on a shared computing platform is not recommended.

Each runner is an isolated process that picks up job requests and creates workers according to its configuration. Move from one runner manager with one runner, to multiple runners on a manager, to autoscaling executors as demand grows.

## Checked

2026-11-03. Confirmed against planning questions and runner process description on Fleet scaling.

Method: documentation only; no commands were run.
