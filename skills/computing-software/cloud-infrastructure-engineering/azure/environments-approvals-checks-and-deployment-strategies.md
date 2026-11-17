---
id: computing-software.cloud-infrastructure-engineering.azure.environments-approvals-checks-and-deployment-strategies
name: environments-approvals-checks-and-deployment-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, azure-pipelines, environments, approvals, checks, release-gates, deployment-strategies, deployment-jobs, runonce, rolling, canary, blue-green, business-hours-check, required-template, branch-control, exclusive-lock, invoke-azure-function-check, query-alerts-check, service-connection-checks, deployment-group, kubernetes-environment-resource, traceability, change-management, environment-approvals, approval-timeout]
level: practitioner
status: draft
description: "Gate production in Azure Pipelines: environment approvals, branch control, business hours, required templates, locks and Monitor gates; runOnce/rolling/canary strategies, blue/green, traceability."
sources: ["Microsoft Learn - Create and target an environment; environment approvals and checks", "Microsoft Learn - Define approvals and checks (branch control, business hours, required template, exclusive lock, invoke Azure Function, query Azure Monitor alerts)", "Microsoft Learn - Deployment jobs and strategies (runOnce, rolling, canary)", "Microsoft Learn - Deploy to Kubernetes with canary strategy and environment resources", "Microsoft Learn - Pipeline traceability: link work items, releases and environments"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Environments, approvals and deployment strategies — production gated by policy, not by luck

**Goal:** nothing reaches prod except from the main branch, through the governed
template, inside business hours, with the right human (or automated) sign-off —
and the deployment itself is staged so a bad build hits 10 % of users, not 100 %.

## 1. Environments
- `az devops`/portal: Pipelines → Environments → `dev`, `test`, `prod` (and `prod-eu` etc.); each shows deployment history, the commits/work items deployed, and optional **resources** (Kubernetes namespace via service account, VM via deployment-group agent) that give per-resource history.
- Deployment jobs target them (`environment: prod` or `environment: prod.orders-ns` for a K8s resource); only `deployment` jobs record history and honour checks.
- Permissions: *Environment Administrator* for the platform team; project-level *Creator* restricted so teams can't make their own ungated `prod`.

## 2. Checks (the control set for `prod`)
| Check | What it enforces |
|---|---|
| **Approvals** | named users/groups (≥ 1 of N), timeout (e.g. 24 h), *requester cannot approve*, instructions text; re-validate on re-run |
| **Branch control** | `refs/heads/main` (or `refs/tags/release/*`), *verify branch protection* so only policy-protected branches qualify |
| **Required template** | the run must `extends` the named template from the template repo (`@templates`, path, ref) — the enforcement half of the templates skill |
| **Business hours** | deploy window Mon–Thu 09:00–16:00 in the org time zone; pair with an *emergency* environment without it |
| **Exclusive lock** | one deployment at a time; later runs queue or cancel (`runLatest`) |
| **Invoke Azure Function / REST API** | change-management ticket exists and is approved (ServiceNow/Jira lookup), custom pre-flight (quota, feature-flag state); async mode with callback for long checks |
| **Query Azure Monitor alerts** | after deployment, hold for N minutes and fail if alerts fire in the resource group — the post-deploy gate for canary/rolling |
| **Evaluate artifact** | artifact policy (e.g. container image built by a trusted pipeline, signed) — Open Policy Agent-style rego |
Same checks exist on **service connections**, **agent pools**, **variable groups** and **secure files** — put *required template* + *branch control* on the prod service connection too, so a rogue pipeline can't use it even without the environment.

## 3. Deployment strategies in YAML
```yaml
- deployment: deploy_prod
  environment: prod
  strategy:
    canary:
      increments: [10, 50]
      preDeploy:
        steps:
        - script: ./smoke-prereqs.sh
      deploy:
        steps:
        - task: KubernetesManifest@1   # strategy: canary with percentage $(strategy.increment)
          inputs:
            action: deploy
            strategy: canary
            percentage: $(strategy.increment)
            manifests: k8s/*.yml
            trafficSplitMethod: smi
      postRouteTraffic:
        steps:
        - script: ./verify-slo.sh $(strategy.increment)   # or Query Azure Monitor alerts check on the environment
        - task: Delay@1
      on:
        failure:
          steps:
          - task: KubernetesManifest@1
            inputs: { action: reject, strategy: canary, manifests: k8s/*.yml }
        success:
          steps:
          - task: KubernetesManifest@1
            inputs: { action: promote, strategy: canary, manifests: k8s/*.yml }
```
- **runOnce**: `preDeploy` → `deploy` → `routeTraffic` → `postRouteTraffic` → `on: success/failure` — the default; hooks are where smoke tests and rollbacks live.
- **rolling** (`maxParallel: 2` or `25%`): across **VM resources** of the environment (deployment-group agents) — one batch at a time with health hooks.
- **canary** (`increments`): with the `KubernetesManifest` task (label-based or SMI traffic split) on AKS, or with App Service **slot traffic** (`az webapp traffic-routing set --distribution staging=10`) in your own steps, or Front Door weights.
- **Blue/green**: App Service slot swap with preview; AKS two Deployments + Service selector switch (or Argo Rollouts/Flagger when the cluster owns progressive delivery — then the pipeline only pushes the image tag); Traffic Manager/Front Door for whole-stack blue/green across regions.
- Rollback = redeploy the previous artifact (pipeline artifacts/immutable image tags) — make it a one-click re-run of the last good run, and test that path.

## 4. Traceability
- Work items ↔ commits (`AB#1234` in commit/PR), PR ↔ build, build ↔ environment deployment; the environment's *Deployments* tab and the work item's *Deployment* control show "deployed to prod on <date> by run <n>".
- Release notes from `Build.SourceVersion` ranges (`az boards` / REST `workitems` linked to builds); `Deployment` records are what auditors ask for — keep retention ≥ the audit period (`Project settings > Retention`).
- Approvals record *who* and *when* with the instructions shown; change-ticket IDs passed as runtime parameters and validated by the Function check close the loop.

## 5. Practical layout
- Environments: `dev` (no checks), `test` (branch control + exclusive lock), `prod` (approvals + branch control + required template + business hours + exclusive lock + post-deploy Monitor check), `prod-emergency` (approvals by on-call leads only, no business hours).
- One pipeline per service with stages per environment; **stage-level** `condition` and the environment checks together decide; use `resources.pipelines` to promote a *built* artifact rather than rebuilding per environment.
- Variable groups per environment with Key Vault linkage (see pipeline-secrets skill); service connections per environment with workload identity federation.
- Deployment windows and freezes: business-hours check + a *Query Azure Monitor* "freeze flag" (a metric/alert you flip) or a Function check reading a calendar.

## Gotchas
- Checks run **before the stage**, not before each job; a stage with multiple deployment jobs to different environments evaluates all their checks up front.
- Approval timeouts default to 30 days — a forgotten run can be approved weeks later and deploy a stale artifact; set 24 h and *requester cannot approve*.
- Branch control without *verify branch protection* can be satisfied by anyone who can push to `main` if the branch isn't policy-protected.
- Canary `increments` with `KubernetesManifest` need the baseline/canary labels the task adds; mixing with Helm/Kustomize deployments outside the task leaves orphaned `-baseline`/`-canary` workloads.
- `Query Azure Monitor alerts` only sees alerts in the configured scope and severity; an app with no alert rules passes every gate.
- Re-running a failed stage re-evaluates approvals; `on: failure` hooks don't run on cancellation (use `condition: always()` in a cleanup job for that).
- Environment resources for K8s use a service account token stored in Azure DevOps; rotate when cluster credentials rotate (workload identity for the pipeline step is the better path — the environment resource is mostly for history).

## Verify
- [ ] A run from a feature branch targeting `prod` is blocked by branch control; a run from `main` using a non-approved template is blocked by required template (both visible in the checks log).
- [ ] Prod deployment at 02:00 waits for business hours; the approval shows requester-cannot-approve enforced; exclusive lock queues a second run.
- [ ] Canary: 10 % traffic stage observed (traffic split/slot routing), SLO script passes, promotion happens; a deliberately failing verify triggers `on: failure` rollback and the environment shows the failed deployment.
- [ ] Work item linked to the PR shows the prod deployment; the environment's history lists commits and approver for the last release.
