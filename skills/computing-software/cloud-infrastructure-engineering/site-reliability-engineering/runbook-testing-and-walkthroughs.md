---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.runbook-testing-and-walkthroughs
name: runbook-testing-and-walkthroughs
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [runbook-testing-drills, runbook-walkthrough, runbooks, game-day, fault-injection, on-call-training]
level: practitioner
status: draft
description: "Test runbooks by walking through them with a new on-call and by triggering the alert in staging with injected faults, then fix every gap the test exposes."
sources: ["https://sre.google/workbook/on-call/", "https://sre.google/sre-book/accelerating-sre-on-call/", "https://sre.google/sre-book/testing-reliability/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Runbook testing and walkthroughs

A runbook is only verified when someone who did not write it has executed it.

## Walkthrough (desk check, 30 min)
1. Pick an alert. Newest on-call reads the runbook aloud and states each action they would take.
2. Author stays silent; a scribe records every question, ambiguity, missing permission, dead link.
3. Fix the runbook in the same session or open tickets.
Good for many runbooks quickly; does not catch broken commands.

## Live test in staging (1-2 h)
1. Inject the fault that triggers the alert:
   - error rate: deploy a build with an error flag, or Istio fault injection
     ```yaml
     http:
     - fault: { abort: { percentage: { value: 10 }, httpStatus: 503 } }
       route: [{ destination: { host: api } }]
     ```
   - saturation: `stress-ng --cpu 4 --timeout 600s` on a node / pod
   - dependency down: scale dependency to 0 or NetworkPolicy deny
   - disk fill: `fallocate -l 20G /data/fill`
2. Confirm the alert fires with correct labels and runbook link (alerting itself is tested).
3. Responder follows the runbook literally, using only what it links.
4. Time each step; record where they had to improvise.
5. Remove the fault; update the runbook and its "Last verified" date.

## Cadence
- New alert: walkthrough before it can page.
- Top 10 paging alerts: live test each quarter (rotate).
- After major infra changes (cluster migration, new region): re-test affected runbooks.

## Gotchas
- Staging may lack the permissions prod requires; also verify the responder has prod access (break-glass
  tested) without running the mutation.
- Clean up injected faults with a timer (`--timeout`, TTL) so a forgotten drill does not page tomorrow.

## Verify
- [ ] Each paging runbook has a dated walkthrough or live test in the last 6 months.
- [ ] Gaps found in tests tracked to closure.
