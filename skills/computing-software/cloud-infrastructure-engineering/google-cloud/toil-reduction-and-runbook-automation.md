---
id: computing-software.cloud-infrastructure-engineering.google-cloud.toil-reduction-and-runbook-automation
name: toil-reduction-and-runbook-automation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, toil, sre-practices, runbook-automation, automation, auto-remediation, cloud-run-functions-remediation, workflows-automation, cloud-scheduler, eventarc-automation, pubsub-alert-automation, self-healing, toil-budget, toil-measurement, operational-load, chatops, scheduled-jobs, idempotent-automation]
level: advanced
status: draft
description: "Measure and eliminate toil on GCP: toil inventory and the 50% rule, auto-remediation from alerts via Pub/Sub and Cloud Run functions, Workflows and Scheduler for recurring ops, safety rails."
sources: ["https://sre.google/sre-book/eliminating-toil/", "https://sre.google/workbook/eliminating-toil/", "https://cloud.google.com/architecture/framework/operational-excellence/automate-and-manage-change", "https://cloud.google.com/monitoring/support/notification-options#pubsub", "https://cloud.google.com/workflows/docs/overview", "https://cloud.google.com/scheduler/docs/overview", "https://cloud.google.com/eventarc/docs/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toil reduction and runbook automation

**Goal:** the on-call team spends under half its time on manual, repetitive, automatable,
interrupt-driven work — because the top toil items are measured, ranked and turned into code with guard rails.

## 1. Find it (toil inventory)
- Toil = manual, repetitive, automatable, tactical, no enduring value, scales with service growth. Not toil: design, postmortems, capacity planning, writing the automation.
- Track for two weeks: every ticket/page/chat ask tagged `toil:<category>` (restarts, quota bumps, access grants, cert renewals, disk resizes, re-running failed jobs, "is it down?" questions). PagerDuty/Jira labels or a simple Sheet.
- Rank by `frequency × minutes × people`; the top 5 usually cover 60 %. SRE budget: ≤ 50 % toil per engineer; if above, feature work stops until automation brings it down.
- GCP signals that quantify it: alert counts per policy (`alerting` incidents list), support/IAM request tickets, `SetIamPolicy` audit entries by human principals (manual access grants), `compute.instances.reset` by humans (manual restarts), budget-threshold emails.

## 2. Standard GCP automation shapes
| Pattern | Pieces | Example |
|---|---|---|
| **Alert → remediation** | Monitoring policy → Pub/Sub channel → Cloud Run function (idempotent, scoped SA) → writes a Logging entry + ticket | disk at 90 % → `gcloud compute disks resize` +10 % (max 3×/day), restart a stuck MIG instance, scale Cloud Run max instances |
| **Scheduled ops** | Cloud Scheduler → Workflows / Cloud Run job | nightly snapshot verification, weekly quota headroom report, monthly image rebuild, stale project cleanup |
| **Event → policy** | Eventarc/Asset feed → function | new project → attach budget + default sinks; new bucket without UBLA → fix + notify owner |
| **Self-service** | ChatOps/Slack slash command or a form → Workflow with approval step → IAM/Terraform PR | temporary role grant (JIT via PAM), DB read replica for an analyst |
| **Platform features instead of code** | autohealing, autoscaling, OS patch deployments, Backup and DR plans, Recommender auto-apply, Cloud SQL maintenance windows | most "restart it" runbooks disappear |

Alert payload → function skeleton (Python):
```python
import base64, json, functions_framework
from google.cloud import compute_v1
@functions_framework.cloud_event
def remediate(event):
    msg = json.loads(base64.b64decode(event.data["message"]["data"]))
    inc = msg["incident"]
    if inc["state"] != "open" or inc["policy_name"] != "disk-90pct": return
    res = inc["resource"]["labels"]; disk = res["device_name"]; zone = res["zone"]; project = res["project_id"]
    # guard rails: allow-list of projects, max actions per day via Firestore counter, dry-run flag
    client = compute_v1.DisksClient(); d = client.get(project=project, zone=zone, disk=disk)
    new = int(d.size_gb * 1.1)
    client.resize(project=project, zone=zone, disk=disk, disks_resize_request_resource={"size_gb": new}).result()
    print(json.dumps({"severity": "NOTICE", "message": "auto-resized", "disk": disk, "from": d.size_gb, "to": new, "incident": inc["incident_id"]}))
```
Function SA: `compute.storageAdmin` on the allow-listed projects only; Pub/Sub push subscription with OIDC; `--max-instances=1` and a Firestore/Redis rate limit so a flapping alert cannot run away.

## 3. Workflows for multi-step runbooks
```yaml
main:
  params: [args]
  steps:
  - snapshot:
      call: googleapis.compute.v1.disks.createSnapshot
      args: {project: '${args.project}', zone: '${args.zone}', disk: '${args.disk}', body: {name: '${"pre-resize-" + string(sys.now())}'}}
  - wait: {call: sys.sleep, args: {seconds: 30}}
  - resize:
      call: googleapis.compute.v1.disks.resize
      args: {project: '${args.project}', zone: '${args.zone}', disk: '${args.disk}', body: {sizeGb: '${args.sizeGb}'}}
  - notify:
      call: http.post
      args: {url: '${sys.get_env("SLACK_WEBHOOK")}', body: {text: '${"resized " + args.disk}'}}
```
Workflows calls Google APIs natively with the workflow SA, retries with `try/retry`, waits on long-running operations, and keeps an execution log — the right place for "do A, wait, do B, tell someone". Trigger from Scheduler, Eventarc, or a human with `gcloud workflows run`.

## 4. Guard rails (what separates automation from an outage generator)
- **Idempotent** and **bounded**: every action checks current state first, has a max per hour/day, and a kill switch (env var / Firestore flag) the on-caller can flip.
- **Dry-run first**: ship with `DRY_RUN=true` logging the would-be action for a week.
- **Scoped identity**: one SA per automation, project allow-list in code, no org-level roles.
- **Observable**: structured log per action with incident id; a dashboard of automation actions; alert if the *same* remediation fires > N times (the real fix is elsewhere).
- **Reviewed like code**: in the repo, with tests against the emulator/fake responses; never a console-only function.

## 5. Keep score
Monthly: toil hours per engineer (target < 50 %), number of automations and actions they took, pages avoided (alerts that auto-resolved via remediation), tickets per category trending down. Celebrate deleting a runbook.

## Gotchas
- Automating a bad alert amplifies it; fix thresholds and SLO-based alerting first (see `alerting-policies-and-notification-channels`).
- Remediations that create resources (disks, instances) need quota headroom and cost caps or they become the incident.
- Pub/Sub delivers at-least-once: the function will see the same incident twice; dedupe on `incident_id`.
- Workflows default timeout and callback limits (1 year max, step sizes) are fine; the HTTP step size limit (2 MB) bites on big API responses — use `project`/`fields` filters.
- "Automate everything" is itself toil if nobody maintains it; delete automations whose trigger has not fired in 6 months.

## Verify
- [ ] Toil inventory exists with the last two weeks' data and a ranked top 5; one item from it is in the sprint.
- [ ] Firing the test alert in staging triggers the remediation once (not twice), logs the action with the incident id, and the kill switch stops it.
- [ ] Rate limit: the fourth remediation of the day is refused and pages a human instead.
- [ ] Monthly toil metric is on the team dashboard and trending down over the quarter.
