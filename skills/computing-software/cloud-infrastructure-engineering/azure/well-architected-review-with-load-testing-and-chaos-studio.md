---
id: computing-software.cloud-infrastructure-engineering.azure.well-architected-review-with-load-testing-and-chaos-studio
name: well-architected-review-with-load-testing-and-chaos-studio
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, well-architected, azure-well-architected, waf-review, design-review, reliability, security, cost-optimisation, operational-excellence, performance-efficiency, azure-load-testing, load-testing, performance-testing, jmeter, locust, chaos-studio, chaos-engineering, fault-injection, chaos-experiments, azure-review-checklist, advisor-waf, service-guides, failure-mode-analysis, health-model, mission-critical]
level: advanced
status: draft
description: "Run a Well-Architected review that changes the design (pillar checklists, review-checklists tooling, failure-mode analysis), then prove it with Azure Load Testing and Chaos Studio."
sources: ["Microsoft Learn - Azure Well-Architected Framework pillars, design principles and service guides", "Azure Well-Architected Review assessment (learn.microsoft.com/assessments)", "GitHub Azure/review-checklists (Azure Review Checklists)", "Microsoft Learn - Azure Load Testing overview, CI/CD integration and pass/fail criteria", "Microsoft Learn - Azure Chaos Studio overview, faults library and experiments"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Well-Architected review, load testing and chaos — assess, then prove it

**Goal:** a review that produces a prioritised, owned backlog rather than a slide, and
two kinds of evidence afterwards: the system meets its performance targets under load,
and it degrades the way the design says when a dependency fails.

## 1. The review, done properly
1. **Scope and targets first**: write the workload's SLO (availability %, p95 latency,
   RTO/RPO, cost ceiling, compliance). A review without numbers produces opinions.
2. **Pillars** (each with design principles + checklists): Reliability (RE:01–RE:10),
   Security (SE:01–SE:12), Cost Optimization (CO:01–CO:14), Operational Excellence
   (OE:01–OE:12), Performance Efficiency (PE:01–PE:12). Walk the checklist items that apply; record
   *met / partially / not met / N/A* with evidence (resource IDs, screenshots, policy state).
3. **Service guides**: per-service WAF recommendations (AKS, App Service, SQL, Cosmos, Firewall, Front Door, Storage…) with the exact config checks — these are the bulk of actionable findings.
4. **Tooling**: the *Azure Well-Architected Review* assessment (learn.microsoft.com/assessments)
   gives a scored questionnaire and links; the **Azure Review Checklists** repo (`Azure/review-checklists`)
   supplies spreadsheets + a Resource Graph-based *checklist graph queries* script that auto-fills many items from the live estate; **Advisor's WAF view** maps recommendations to pillars; Defender for Cloud secure score covers Security.
5. **Failure-mode analysis** (RE:03): table of components × failure (zone loss, dependency down, cert expiry, quota, throttling, bad deploy) → detection → mitigation → RTO. Every row without a mitigation is a finding.
6. **Health model** (mission-critical guidance): per-flow health scores from metrics/logs so "healthy" is computed, not felt.
7. Output: findings with severity, effort, owner, due date in the backlog; architecture decision records for accepted risks; re-review quarterly or on major change. Typical top findings: no zone redundancy on the data tier, no tested restore, shared keys in app settings, no Service Health alerts, over-provisioned SKUs, no load test before launch.

## 2. Azure Load Testing (prove performance)
```bash
az load create -g rg-test -n alt-orders -l uksouth
az load test create --load-test-resource alt-orders -g rg-test --test-id orders-peak --display-name "orders peak" \
  --test-plan orders.jmx --engine-instances 4 --env host=api.example.com --secret token="https://kv.vault.azure.net/secrets/api-token" \
  --keyvault-reference-id <uami-id> --autostop-error-rate 90 --autostop-error-rate-time-window 60
az load test-run create --load-test-resource alt-orders -g rg-test --test-id orders-peak --test-run-id run-$(date +%s) --display-name "pre-release"
```
- Engines: JMeter (`.jmx`, plugins supported) or **Locust** (`locustfile.py`); ~250 virtual users per engine, up to 400 engines; private endpoint testing by deploying engines into your VNet (`--subnet-id`).
- Upload CSV data, config fragments, and secrets/certs from Key Vault (test identity needs *Secrets User*).
- **App components**: link the Azure resources under test → server-side metrics (CPU, DB DTU, SNAT, 5xx) plotted beside client-side latency/throughput so you see the bottleneck, not just the symptom.
- **Pass/fail criteria** in the YAML config (`failureCriteria: - avg(response_time_ms) > 300`, `- percentage(error) > 2`, per-request `GetOrders: p95(response_time_ms) > 500`) → the run fails → CI gate. GitHub Action `azure/load-testing` and Azure Pipelines task `AzureLoadTest@1` take `config.yaml`.
- Compare runs (baseline vs candidate) in the portal; set the baseline run; export results to JMeter dashboards/CSV.
- Test design: ramp to 1.5× expected peak for ≥ 30 min (longer than any burst credit), include think time, run from the region users come from; run against staging with production-equivalent SKUs and real data volume, with autoscale on.

## 3. Chaos Studio (prove resilience)
```bash
az rest --method put --url "https://management.azure.com/<vm-id>/providers/Microsoft.Chaos/targets/Microsoft-VirtualMachine?api-version=2024-01-01" --body '{"properties":{}}'   # onboard target
az rest --method put --url ".../targets/Microsoft-VirtualMachine/capabilities/Shutdown-1.0?api-version=2024-01-01" --body '{}'         # enable capability
# experiment (ARM/Bicep Microsoft.Chaos/experiments): steps → branches → actions (continuous fault with duration/parameters, or discrete), selectors (list of targets), system-assigned identity
# then: az rest --method post --url ".../Microsoft.Chaos/experiments/exp-zone-loss/start?api-version=2024-01-01"
```
- Fault library: **service-direct** (no agent) — VM shutdown, VMSS shutdown (by zone!), AKS Chaos Mesh faults (pod/network/stress/IO), Cosmos DB failover, Key Vault deny access, NSG security rule injection (block a dependency), App Service stop, Redis reboot, Event Hub/Service Bus disable (the library grows — check the current fault reference); **agent-based** (Chaos agent on VM/VMSS with identity) — CPU/memory/disk pressure, network latency/packet loss/disconnect, DNS failure, kill process, time change.
- Experiment identity needs RBAC on each target (e.g. *Virtual Machine Contributor*) — least-privilege per fault documented in the fault reference.
- Design each experiment as a hypothesis: "If zone 1 goes down, the API stays under 1 % errors and p95 < 500 ms within 2 min" → run during a load test → check the metrics/alerts → stop condition (abort if error rate > X via the *stop* of experiment from an alert action/Logic App).
- Start in non-prod; run in prod only for experiments whose blast radius is understood (one instance, one zone) and with the on-call aware. Keep a game-day calendar.
- Results: experiment execution details show per-action status; your evidence is the dashboards/alerts/SLO burn during the window.

## Gotchas
- A review scored high because every item was marked N/A is worthless; the reviewer should challenge N/A.
- Load tests from a single engine region against a multi-region app test the wrong path; an Azure Load Testing resource runs in one region, so create one per source region you care about.
- Load testing a shared staging environment during business hours takes down other teams; schedule.
- Chaos faults that remove the last healthy instance (`VMSS shutdown` with all instances selected) make the experiment "succeed" and the service fail — selectors are the blast radius.
- Forgetting to turn off continuous faults when an experiment is cancelled: Chaos Studio reverts them, but agent-based network faults on a rebooted VM may need the agent to clean up — check `iptables`/`netsh` after.
- Pass/fail on average latency hides tail problems; criteria must be p95/p99.

## Verify
- [ ] Review artefact: every pillar has checklist results with evidence and a backlog item for each *not met* High; SLO numbers written at the top.
- [ ] Load test run at 1.5× peak passes all criteria; app-component metrics show headroom (CPU < 70 %, no SNAT/DB throttling).
- [ ] Chaos experiment "zone loss" under load: error rate and latency stay inside SLO; alerts fired as designed; experiment status `Success` and faults reverted.
- [ ] CI pipeline fails on a deliberately degraded build (criteria breached) and passes on main.
