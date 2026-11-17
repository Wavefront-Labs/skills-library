---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.executable-runbooks-and-automation-tools
name: executable-runbooks-and-automation-tools
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [runbook-automation-tools, executable-runbooks, runbooks, rundeck, toil-reduction]
level: practitioner
status: docs-checked
description: "Turn runbook steps into executable automation: human-backed interfaces, self-service jobs (Rundeck), and automated responses with safety guards."
sources: ["https://sre.google/workbook/eliminating-toil/", "https://docs.rundeck.com/docs/manual/jobs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Executable runbooks and automation tools

SRE Workbook "Eliminating Toil": move from documented procedures to partly automated, then self-service, then
automated responses, in small steps.

## Maturity ladder (Workbook)
1. **Human-backed interface**: for a complex problem with many edge cases, accept structured requests (usually
   via a defined API) while engineers still handle some operations behind the curtain. Fewer free-form
   requests moves you toward handling everything programmatically, without a big-bang design.
2. **Self-service**: a web form, binary or script, API, or even documentation on how to open a pull request
   against your configuration files. The Workbook's example: give engineers a form or script that provisions a
   development VM instead of a ticket, and let it degrade gracefully to a ticket for specialised requests or on
   failure.
3. **Automate toil response**: mirror the human workflow in software, but rarely transcribe it literally;
   break it into composable components other automation can reuse. Automation should not remove human
   understanding of what is going wrong.
Start small: automate a few high-priority items first, then improve using the time gained, and pick clear
metrics such as MTTR. Measure automated tasks by latency, error rate, rework rate and human time saved.

## Rundeck jobs
A Rundeck Job encapsulates a process: input options, the steps, a node filter expression and execution control
(run in parallel or not, what to do on error). Documented behaviour:
- Access is governed by an access control policy declaring who may read, create, edit, run and kill jobs; job
  groups help define that policy.
- Run dialog prompts for job options (defaults, menus, required or optional, value patterns).
- Each execution is stored with nodes, success and duration of each step; output can be downloaded, forwarded
  to an external log store or sent in notifications (email, IRC, ticketing).
- Each job has a UUID; assign your own only carefully, since non-UUID values can cause inconsistent loading. The
  UUID keeps a renamed or regrouped job matched on the server and helps port definitions between instances.
- Killing a running job forcibly kills the Java thread and does not guarantee child processes on the node end.

## Assess risk within automation (Workbook)
- Validate input defensively, even from upstream systems.
- Build safeguards equivalent to the indirect alerts a human operator would get: command timeouts, checks of
  current metrics or the number of current outages. Even naive read operations can spike device load.
- Every action should be assessed for safety before execution, including changes that reduce serving capacity or
  redundancy.
- Automation should default to human operators when it hits an unsafe condition.

## Gotchas
- Automating a symptom can mask the severity of an underlying problem: the Workbook's example is a script that
  would truncate logs on full-disk machines instead of fixing the network driver that wrote them; a teammate pointed out that fixing
  root causes is better.
- Keep the written runbook for when the automation platform itself is down.

## Verify
- [ ] Top runbook procedures exist as parameterised jobs with access control and execution history.
- [ ] Automation stops and hands over to a human on unsafe conditions.

## Checked

Checked 2026-11-09. Confirmed against the SRE Workbook Eliminating Toil page (human-backed interfaces, self-service, risk in automation, case study) and the Rundeck Jobs manual page (job contents, access control, executions, UUIDs, kill warning). Removed: the AWS Systems Manager Automation document and CLI command (docs.aws.amazon.com not readable), the sample Rundeck YAML, notebook runbooks, Alertmanager webhook remediation and its rate-limit numbers, and the StackStorm and workflow_dispatch mentions, none confirmed on a page read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
