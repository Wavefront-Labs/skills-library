---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.runbooks-and-playbooks
name: runbooks-and-playbooks
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, runbooks, runbook, playbooks, playbook, runbook-template, runbook-url, alert-annotations, runbook-automation, docs-as-code, markdown-runbooks, mkdocs, backstage, runbook-testing, wheel-of-misfortune, operational-documentation, mitigation-steps, escalation-paths, dashboards-links, copy-paste-commands, runbook-rot, runbook-review, service-catalog]
level: practitioner
status: draft
description: "Write runbooks responders actually use: one per alert linked from runbook_url, a fixed template (meaning, impact, triage, mitigation, escalation, verify)."
sources: ["https://sre.google/sre-book/practical-alerting/", "https://sre.google/sre-book/accelerating-sre-on-call/", "https://sre.google/workbook/on-call/", "https://sre.google/sre-book/monitoring-distributed-systems/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Runbooks and playbooks

**Goal:** at 3 a.m. the pager links to a page that tells the responder what the alert
means, how bad it is, the first three things to check, and the mitigation to run — in a
form that still works six months after it was written.

## 1. Rules
- **One runbook per alert** (or per tightly related alert family), reachable from the
  alert itself: `annotations.runbook_url: https://runbooks.example.com/<service>/<AlertName>`.
  Lint rules in CI: every `severity=page` alert must have a `runbook_url` that returns 200.
- **Playbook vs runbook**: a *playbook* is the broader "how to operate this service"
  document (architecture, dashboards, dependencies, common operations); *runbooks* are
  alert-specific procedures that link back to it. Keep both in the same repo.
- Written for the **least-context responder** (new on-caller, other team's secondary),
  not for the author. No tribal knowledge, no "ask Priya".
- **Short**: if it needs more than a screen, the alert is too vague or the system needs
  automation. The SRE Book's point: a runbook that says "restart X" is a sign X should
  restart itself.
- Docs-as-code: Markdown in git next to the alert rules, rendered by MkDocs/Backstage/
  Docusaurus; changes go through PR with the on-call rotation as reviewers.

## 2. Template
```markdown
# ApiHighErrorRate
**Severity:** page · **Owner:** payments-oncall · **Dashboard:** [API overview](...) · **Last reviewed:** 2026-09-30 by @name

## Meaning
5xx ratio on `api` > 5% for 10 m (expr: `...`). Fires on user-visible failures; does not fire on client 4xx.

## Impact
Checkout fails for the affected share of users; revenue impact ~£X/min at 100% failure. SLO budget burn: 14× at 5%.

## Triage (first 5 minutes)
1. Scope: `sum by (pod, version) (rate(http_requests_total{job="api",code=~"5.."}[5m]))` — one pod/version or all?
2. What changed: [deploys](grafana annotations link) · [flags](link) · [infra changes](link) in the last 2 h.
3. Dependencies: [payments-gateway status](link) · `sum by (dependency) (rate(client_errors_total{job="api"}[5m]))`.
4. Logs: `{app="api"} | json | status >= 500 | line_format "{{.path}} {{.error}}"` (Explore link with time range).

## Mitigation
- Bad version isolated → rollback: `kubectl argo rollouts undo rollout/api -n payments` (≈2 min). Verify with step 1.
- Dependency down → enable degraded mode: `kubectl -n payments set env deploy/api PAYMENTS_FALLBACK=queue` (orders queued, not lost).
- Single pod → `kubectl -n payments delete pod <POD>`; if recurring, cordon the node and open a ticket.
- Overload → scale: `kubectl -n payments scale deploy/api --replicas=<CURRENT+50%>`; check HPA max.

## Escalation
After 15 min without mitigation or if data loss suspected → page `payments-secondary`; Sev-1 criteria: > 50% errors for > 10 min → declare incident (`/incident declare`).

## Verify resolution
Error ratio < 1% for 10 min on the dashboard; alert resolves; note the cause in the incident channel.

## Known causes / history
- 2026-08-12: connection pool exhaustion after dependency latency spike → fixed by timeout tuning (PM-123).
```

## 3. Writing the commands
- Copy-pasteable, with explicit placeholders `<POD>` and a line explaining how to find
  the value; include the namespace/cluster context (`--context prod-eu1`).
- Pre-link Grafana Explore/dashboard URLs with variables and `from=now-1h`.
- Dangerous commands get a **confirmation line** above them ("this drops traffic to the
  canary; safe if < 10% weight") and an undo command below.
- Prefer scripts/automation in a tools repo (`./ops api rollback`) over long inline
  sequences; the runbook then documents *when* to run them.
- Never include secrets; link to where they live.

## 4. Keeping them alive
- **Review cadence**: every runbook has `Last reviewed` and an owner; a scheduled job
  lists runbooks older than 6 months or whose alert no longer exists; on-call handover
  includes "runbooks I used and what was wrong".
- **Test**: Wheel-of-Misfortune sessions execute runbooks on staging; every real page
  that found a gap produces a PR within the week (count this in the postmortem actions).
- **Metrics**: pages without a runbook (lint), runbook page views per alert (which ones
  are used), postmortems citing "runbook outdated".
- Delete runbooks for alerts you removed; archive history to the playbook's "known causes".
- Automate what the runbook repeats: if step 2 of mitigation is always "restart", make
  the alert trigger the restart and page only on recurrence (`...site-reliability-engineering.toil-reduction-and-automation`).

## 5. Service playbook contents (the parent document)
Architecture diagram and request path · dependency list with their on-call/status pages ·
dashboards (overview, per-component, SLO) · deploy/rollback procedure · scaling knobs and
limits · data stores with backup/restore links · feature flags that matter in incidents ·
contacts and escalation · links to all runbooks · recent postmortems.

## Gotchas
- A runbook that explains the system instead of what to do: move theory to the playbook.
- Hard-coding values that drift (pod names, IPs, replica counts) — use queries and placeholders.
- Links into tools that need VPN/SSO without saying so; the responder learns at 3 a.m.
- "Escalate to the team" with no name/rotation; every escalation line names a schedule.
- Multiple competing wikis; one canonical location, the alert link is the index.

## Verify
- [ ] `promtool`/CI lint: 100% of paging alerts have a reachable `runbook_url`.
- [ ] A responder unfamiliar with the service mitigated a staged fault using only the runbook, and timed it.
- [ ] No runbook older than 6 months unreviewed; last month's postmortems contain at least one runbook PR.
- [ ] Every mitigation command in the top-10 runbooks was executed successfully in staging this quarter.
