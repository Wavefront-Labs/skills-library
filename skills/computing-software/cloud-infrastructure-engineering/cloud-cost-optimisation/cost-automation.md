---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-automation
name: cost-automation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-tools, cost-automation, automated-remediation, cloud-custodian]
level: practitioner
status: docs-checked
description: "Automate cost remediation safely with Cloud Custodian: scheduling, mark-then-act garbage collection, dry runs, and build-versus-buy criteria."
sources: ["https://cloudcustodian.io/docs/", "https://cloudcustodian.io/docs/aws/examples/offhours.html", "https://cloudcustodian.io/docs/aws/examples/ebsgarbagecollect.html", "https://cloudcustodian.io/docs/quickstart/index.html", "https://www.finops.org/framework/capabilities/finops-tools-services/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated remediation tooling

## Choosing automation
The FinOps Framework's Automation, Tools and Services capability has teams define when to
"build", "buy" and/or "automate", evaluate automation against requirements such as
functionality, integration complexity, cost and scalability, compare native provider
tooling with third-party and in-house automation, and measure adoption and impact over
time.

## What Cloud Custodian is
An open source stateless rules engine. Policies are YAML with a resource type, filters
to narrow the set, and actions on the filtered set. It follows a compliance-as-code
principle so you can validate, dry-run and review policy changes, and it can run on
serverless runtimes. Its docs name garbage collection of unused resources, tag policies
and cost management among its uses.

## Two patterns from its docs
**Scheduling (offhours).** Time-based `offhour` and `onhour` filters, each used in its own
policy, stop and start instances or suspend and resume auto scaling groups. Options include
a default timezone (required), the tag name used for per-resource schedules (default
`maid_offhours`), opt-in or opt-out mode, and `skip-days` for public holidays. Policies are
evaluated hourly, so a resource is acted on only in the exact hour specified, and a manual
start after a stop is left alone until the next day.

**Mark, then act.** `mark-for-op` only tags a resource with metadata about a future
operation; a separate policy filtering `marked-for-op` must run on the due date. A third
policy unmarks resources that became compliant. See the idle-resource-cleanup skill for
worked examples. The `notify` action needs the Custodian mailer installed and configured.

```yaml
policies:
  - name: offhours-stop
    resource: ec2
    filters:
      - type: offhour
    actions:
      - stop
  - name: offhours-start
    resource: ec2
    filters:
      - type: onhour
    actions:
      - start
```

## Safety
- Validate with `custodian validate custodian.yml`, and preview with
  `custodian run --dryrun -s . custodian.yml` before enabling actions.
- Use the mark-then-act pattern so owners have a window to react.

## Verify
- [ ] Every automation has dry-run history before actions are enabled.
- [ ] Opt-in or opt-out behaviour for scheduled resources is deliberate.

## Checked
Method: docs-checked 2026-11-09 against the Cloud Custodian docs home, offhours, EBS garbage collection and quickstart pages, and the FinOps Framework Automation, Tools and Services page (all fetched and read).
Removed as unconfirmed by the pages read: AWS Instance Scheduler, Azure Start/Stop VMs and GCP schedules (unreadable hosts), unattached-EBS example with 30-day age and snapshot-before-delete, exemption-tag expiry, IaC drift advice, audit/savings reporting items, time-zone and holiday gotcha beyond what the offhours page states, rightsizing pull-request automation.
