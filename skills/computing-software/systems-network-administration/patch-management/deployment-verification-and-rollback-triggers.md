---
id: computing-software.systems-network-administration.patch-management.deployment-verification-and-rollback-triggers
name: deployment-verification-and-rollback-triggers
category: computing-software
field: systems-network-administration
product: patch-management
tags: [deployment-verification, rollback-triggers, smoke-test, release-deployment-mgmt, patch-management]
level: practitioner
status: docs-checked
description: "Verify a deployment and trigger rollback on evidence: post-deploy smoke and synthetic checks, SLO-based automatic rollback (CodeDeploy alarms, Argo analysis) and manual triggers."
sources:
  - https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
  - https://sre.google/workbook/canarying-releases/
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_blocks.html
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deployment verification and rollback triggers

A deployment is complete when it is verified, not when the installer exits 0.

## Verification layers
1. **Install-level**: package/version present (`rpm -q`, `Get-HotFix`, image digest running).
2. **Service-level**: process running, ports listening, health endpoints 200 (`curl -fsS https://app/healthz`).
3. **Functional smoke**: scripted key transactions (log in, search, submit) via synthetic monitoring or test suite.
4. **Telemetry**: error rate, latency, saturation vs pre-deploy baseline over a defined bake time.

## Automatic rollback triggers
- **AWS CodeDeploy**: a deployment or deployment group can roll back automatically when a deployment fails or a monitoring threshold you specify is met, redeploying the last known good revision. In the API this is the deployment group's `AlarmConfiguration` (alarms, for example on 5xx rate or latency) plus `AutoRollbackConfiguration`, whose events are `DEPLOYMENT_FAILURE`, `DEPLOYMENT_STOP_ON_ALARM` and `DEPLOYMENT_STOP_ON_REQUEST`. Without automatic rollback you roll back manually by creating a new deployment of a previous revision.
- **Argo Rollouts**: a Rollout's canary or blue-green strategy can run AnalysisRuns; a Failed run makes the update abort, Inconclusive pauses it, Successful continues. An analysis metric fails via `failureCondition`, and the run is Failed after `failureLimit` failed measurements.
- **Ansible/pipeline**: post-task health checks; on failure run the rollback tasks in a `rescue` section of a `block`.
```yaml
- block:
    - ansible.builtin.package: {name: myapp-2.4.1, state: present}
    - ansible.builtin.uri: {url: "http://localhost:8080/healthz", status_code: 200}
      register: h
      retries: 10
      delay: 6
      until: h.status == 200
  rescue:
    - ansible.builtin.debug: {msg: "run your rollback tasks here: reinstall the previous version with your package module"}
    - ansible.builtin.fail: {msg: "health check failed, rolled back"}
```

## Manual triggers (write them down)
Example triggers; set your own thresholds.
- Any sev-1 incident during bake time on affected services.
- Error rate > 2x baseline for 10 minutes.
- Business metric drop (orders/min) beyond threshold.
- Data integrity concerns: stop and assess, rollback may not be safe.

## Gotchas
- Rollback that has never been tested is a hope; rehearse it.
- Irreversible changes (schema drops, firmware with anti-rollback) need roll-forward plans instead.
- Health endpoints that only check the process, not dependencies, pass broken deployments.

## Verify
Each deployment records verification results per layer; rollback triggers and actions logged; rollback rehearsal date per service.

## Checked
Date: 2026-11-08. Documentation: AWS CodeDeploy User Guide page on rollbacks and redeploys (automatic rollback on failure or monitoring threshold, redeploys last known good revision, manual rollback by redeploying a previous revision) and the botocore codedeploy model (AutoRollbackConfiguration, AlarmConfiguration, AutoRollbackEvent values); Argo Rollouts analysis page (AnalysisRun Successful/Failed/Inconclusive effects, failureCondition, failureLimit); Ansible pages on blocks (rescue), loops (until, retries, delay) and the uri module (status_code, default 200); Google SRE Workbook canarying chapter for the baseline-comparison idea. Removed: the claim that Argo shifts traffic back (the page says the update aborts) and the allow_downgrade option on ansible.builtin.package (not on its module page). The numeric manual triggers are labelled as examples.
Method: documentation only; no commands were run.
