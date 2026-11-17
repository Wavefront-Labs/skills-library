---
id: computing-software.devops-ci-cd.argo-cd.built-in-health-checks
name: built-in-health-checks
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, built-in-health-checks, resource-health-kinds, application-health-app-of-apps]
level: practitioner
status: docs-checked
description: "Know which Kubernetes kinds Argo CD assesses natively and how (Deployments, Services, Ingress, PVCs, Jobs...), the bundled CRD checks, and the missing Application health check."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/health/", "https://github.com/argoproj/argo-cd/tree/master/resource_customizations", "https://github.com/argoproj/argo-cd/tree/master/gitops-engine/pkg/health"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in health checks

## 1. Core kinds
| Kind | Healthy when |
|---|---|
| Deployment, ReplicaSet, StatefulSet, DaemonSet | observed generation equals desired generation and updated replicas equal desired replicas (a paused Deployment is Suspended) |
| Service | always, except `type: LoadBalancer` → has `status.loadBalancer.ingress` hostname/IP |
| Ingress | `status.loadBalancer.ingress` populated |
| PersistentVolumeClaim | `status.phase: Bound` |
| Pod | `restartPolicy: Always`: Healthy once ready, Degraded on error states (`CrashLoopBackOff`, `ImagePullBackOff`) or termination. `Never`/`OnFailure`: Progressing while running, Healthy only once succeeded (annotation `argocd.argoproj.io/ignore-restart-policy: "true"` assesses long-running ones like `Always`) |
| CronJob | Degraded if the last scheduled job failed, Healthy if it is running |
| Job | complete → Healthy, failed → Degraded, `.spec.suspend` true → Suspended, otherwise Progressing |
| HorizontalPodAutoscaler | assessed from its status conditions |
| APIService | `Available` condition true |
| Argo Rollout | rollout status (paused → Suspended) |
Kinds with no check have no health assessment of their own.

## 2. Bundled CRD checks
Argo CD ships Lua checks for many CRDs (cert-manager, Crossplane, Flux, Strimzi, KEDA, External Secrets, Sealed Secrets (`bitnami.com`), Argo Workflows, ...) in
`resource_customizations/<group>/<kind>/health.lua`. Check the repo for your version before writing your own.

## 3. The Application gotcha (app-of-apps)
The health assessment of `argoproj.io/Application` was removed in Argo CD 1.8. If you use app-of-apps and orchestrate synchronisation with sync waves you may need to restore it with this resource customization in `argocd-cm`:
```yaml
data:
  resource.customizations.health.argoproj.io_Application: |
    hs = {}
    hs.status = "Progressing"
    hs.message = ""
    if obj.status ~= nil and obj.status.health ~= nil then
      hs.status = obj.status.health.status
      if obj.status.health.message ~= nil then hs.message = obj.status.health.message end
    end
    return hs
```

## 4. Gotchas
- A Deployment whose Progressing condition reports `ProgressDeadlineExceeded` (after `progressDeadlineSeconds`) becomes **Degraded**.
- LoadBalancer Services and Ingresses are Healthy only once `status.loadBalancer.ingress` has a hostname or IP, so without a load-balancer controller the app stays Progressing.
- `argocd.argoproj.io/ignore-healthcheck: "true"` excludes a child resource from the application health.

## Verify
- [ ] `argocd app get <app>` resource list shows expected health per kind; with the Application check restored, a parent app reports its children's health.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: per-kind rules in the health documentation and in the gitops-engine health code (Deployment paused and `ProgressDeadlineExceeded`, Pod, CronJob, Job, PVC, Service, Ingress, APIService), Rollout paused to Suspended, bundled CRD check groups in `resource_customizations`, removal of the Application check in 1.8, `ignore-healthcheck` annotation. Removed unconfirmed claims (always-Healthy kinds, sync-wave wait detail).

Method: documentation only; no commands were run.
