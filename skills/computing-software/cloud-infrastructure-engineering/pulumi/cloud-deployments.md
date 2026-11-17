---
id: computing-software.cloud-infrastructure-engineering.pulumi.cloud-deployments
name: cloud-deployments
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-deployments, deployments-api, git-push-to-deploy, review-stacks]
level: practitioner
status: docs-checked
description: "Pulumi Deployments overview: managed runners that run up, preview, refresh and destroy, deployment settings, triggers, review stacks, TTL, drift and runners."
sources:
  - https://www.pulumi.com/docs/pulumi-cloud/deployments/
  - https://www.pulumi.com/docs/pulumi-cloud/deployments/get-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pulumi Deployments

A managed service that runs `pulumi up`, `preview`, `refresh` and `destroy` on Pulumi-managed or customer-managed runners instead of a developer's machine. You configure a stack once; operations then run on demand, on version control events, on a schedule, or through the REST API. The runner environment already has the Pulumi CLI and language runtimes, cloud credentials and secrets come from Pulumi ESC and OIDC rather than laptops or pipeline config, and every run is recorded in Pulumi Cloud.

Parts of the feature:
- **Deployments Settings**: per-stack config: source, credentials, environment variables, path and tag filters, runner pool. Captures everything a run needs so a deployment behaves the same however it is triggered.
- **Deployment Triggers**: console Click to Deploy, REST API, webhooks, version control events.
- **Drift Detection**: detect when infrastructure no longer matches the program, optionally remediating on a schedule.
- **TTL Stacks**: destroy a stack at a set time for temporary environments.
- **Review Stacks**: ephemeral environments created per pull request and torn down when it closes.
- **Scheduled operations**: any Pulumi operation on a recurring schedule (see `scheduled-drift-detection`).
- **Pulumi-managed runners** (default) and **customer-managed runners**, the latter also run Discovery scans and audit policy evaluations.
- **Webhooks**: notify external systems or trigger other stacks.

Getting started: create a project with the Pulumi Cloud New Project Wizard (configures Deployments for your repo automatically), or use the Getting Started guides (wizard, or the Pulumi and GitHub CLIs) to set it up on an existing project.

## Gotchas
- Supply credentials through ESC and OIDC, not static keys in settings.
- Concurrency limits apply to scheduled deployments, and pausing deployments on a stack queues them (Schedules page).
- The overview page does not document settings-file keys, CLI subcommands or the REST body; read the Deployments Settings and REST API pages before scripting them.

## Checked
2026-11-03. Confirmed on the Pulumi Deployments overview and Get Started pages (and the Schedules page for the concurrency point). Removed: the `Pulumi.prod.deploy.yaml` sample, `pulumi deployment settings/run` commands, the curl REST call (the API response was 401), static-key and queueing claims and the Verify paragraph.
Method: documentation only; no commands were run.
