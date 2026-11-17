---
id: computing-software.devops-ci-cd.argo-cd.flux-v2-kustomization-helmrelease-and-bootstrap
name: flux-v2-kustomization-helmrelease-and-bootstrap
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, flux, fluxcd, flux-v2, flux-bootstrap, gitrepository, ocirepository, helmrepository, bucket, source-controller, kustomize-controller, helm-controller, notification-controller, flux-kustomization, helmrelease, dependson, health-checks, prune, substitute, postbuild-substitution, flux-reconcile, flux-suspend, flux-resume, flux-diff, flux-trace, flux-events, sops-decryption, flux-alerts, flux-receiver, multi-tenancy, gitops, kubernetes]
level: practitioner
status: docs-checked
description: "Operate Flux v2: bootstrap, Git/OCI/Helm sources, Kustomization with dependsOn, health checks, prune and substitution, HelmRelease remediation, SOPS decryption, alerts, the flux CLI."
sources: ["https://fluxcd.io/flux/installation/bootstrap/", "https://fluxcd.io/flux/components/kustomize/kustomizations/", "https://fluxcd.io/flux/components/helm/helmreleases/", "https://fluxcd.io/flux/guides/mozilla-sops/", "https://fluxcd.io/flux/cmd/", "https://github.com/fluxcd/kustomize-controller/blob/main/docs/spec/v1/kustomizations.md", "https://github.com/fluxcd/helm-controller/blob/main/docs/spec/v2/helmreleases.md", "https://github.com/fluxcd/notification-controller/blob/main/docs/spec/v1/alerts.md", "https://github.com/fluxcd/source-controller/blob/main/docs/spec/v1/ocirepositories.md", "https://github.com/fluxcd/flux2/tree/main/cmd/flux"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flux v2: Kustomization, HelmRelease and bootstrap

**Goal:** a cluster that pulls its own desired state from Git/OCI, applies it in
dependency order, heals drift, and reports — with no UI to run.

## 1. Bootstrap
```bash
flux check --pre
flux bootstrap github --owner=example --repository=fleet --branch=main \
  --path=clusters/prod-eu --team=platform --personal=false \
  --components-extra=image-reflector-controller,image-automation-controller
# gitlab: flux bootstrap gitlab --owner=group --repository=fleet --path=clusters/prod-eu --deploy-token-auth
# generic: flux bootstrap git --url=ssh://git@git.example.com/fleet.git --path=clusters/prod-eu --private-key-file=key
```
Bootstrap installs the controllers in `flux-system`, commits `flux-system/gotk-components.yaml`
+ `gotk-sync.yaml` to `<path>`, and creates a deploy key. Re-running bootstrap with a
newer CLI **upgrades** Flux (it rewrites `gotk-components.yaml`). The `flux-system`
`Kustomization` reconciles `<path>` — everything else (apps, infra) is Kustomizations
referenced from there.

## 2. Sources
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata: { name: apps, namespace: flux-system }
spec:
  interval: 1m
  url: ssh://git@github.com/example/apps.git
  ref: { branch: main }            # or tag / semver: ">=1.0.0 <2.0.0" / commit
  secretRef: { name: apps-deploy-key }
  ignore: |                        # .sourceignore semantics; reduce artifact size
    /*
    !/deploy
---
apiVersion: source.toolkit.fluxcd.io/v1
kind: OCIRepository                 # manifests pushed with `flux push artifact oci://ghcr.io/example/manifests:main`
metadata: { name: manifests, namespace: flux-system }
spec: { interval: 5m, url: oci://ghcr.io/example/manifests, ref: { tag: main }, verify: { provider: cosign } }
---
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata: { name: charts, namespace: flux-system }
spec: { interval: 1h, type: oci, url: oci://registry.example.com/charts }   # type oci is in maintenance mode; prefer OCIRepository + chartRef
```
Sources produce an **artifact** (tarball) that other controllers consume; `flux get sources all`
shows revision and readiness. `flux create secret git apps-deploy-key --url=… ` generates
keys. Webhook receivers (`Receiver` CR + notification-controller) make pushes instant.

## 3. Kustomization (the apply unit)
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: { name: apps, namespace: flux-system }
spec:
  interval: 10m                    # reconcile period: server-side apply dry-run to detect and correct drift
  retryInterval: 2m
  timeout: 5m
  sourceRef: { kind: GitRepository, name: apps }
  path: ./deploy/prod
  prune: true                      # delete objects removed from Git (garbage collection by label)
  wait: true                       # health-check ALL applied objects (healthChecks is ignored when set)
  dependsOn: [{ name: infra-controllers }]
  targetNamespace: web             # override namespace for all resources
  serviceAccountName: team-web     # multi-tenancy: impersonate for RBAC
  postBuild:
    substitute: { CLUSTER: prod-eu }
    substituteFrom: [{ kind: ConfigMap, name: cluster-vars }, { kind: Secret, name: cluster-secrets, optional: true }]
  decryption: { provider: sops, secretRef: { name: sops-age } }
  patches:
    - patch: |
        - op: add
          path: /spec/template/spec/nodeSelector
          value: { pool: apps }
      target: { kind: Deployment }
  healthChecks:                    # explicit, when wait: true is too broad
    - { apiVersion: apps/v1, kind: Deployment, name: web, namespace: web }
```
Rules: `dependsOn` only waits for the other Kustomization to be **Ready** (its last applied
status condition) — pair with `wait: true`/`healthChecks` on the dependency or it is just
ordering by apply. Variable substitution supports bash-style `${var:=default}`; use `$${var}`
to keep literal curly braces. Per-object annotations in the source manifests:
`kustomize.toolkit.fluxcd.io/force: Enabled` recreates objects on immutable-field changes,
`kustomize.toolkit.fluxcd.io/prune: Disabled` opts out of pruning, and
`kustomize.toolkit.fluxcd.io/ssa` sets the apply policy (`Override` default, `Merge`,
`IfNotPresent`, `Ignore`; use `IfNotPresent` or `Ignore` to stop drift correction on an object).
If `path` has no `kustomization.yaml`, one is generated for all manifests under it (every YAML
file there must be a valid Kubernetes manifest unless excluded by `.sourceignore` or
`spec.ignore`); generating your own and committing it is recommended.

## 4. HelmRelease
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata: { name: redis, namespace: cache }
spec:
  interval: 30m
  chart:
    spec:
      chart: redis
      version: "<semver-range>"           # a new matching version triggers an upgrade
      sourceRef: { kind: HelmRepository, name: charts, namespace: flux-system }
      interval: 12h
  # or chartRef: { kind: OCIRepository, name: redis-chart }   (one of chart or chartRef, not both)
  releaseName: redis
  install: { remediation: { retries: 3 }, crds: CreateReplace }
  upgrade: { remediation: { retries: 3, remediateLastFailure: true, strategy: rollback }, crds: CreateReplace, cleanupOnFail: true }
  driftDetection: { mode: enabled, ignore: [{ paths: ["/spec/replicas"], target: { kind: Deployment } }] }
  values: { architecture: standalone }
  valuesFrom:
    - { kind: Secret, name: redis-creds, valuesKey: password, targetPath: auth.password }
  postRenderers:
    - kustomize: { patches: [...] }
```
helm-controller runs real Helm (release secrets exist; `helm list -n cache` works).
`remediation` is what makes upgrades self-healing (`retries` defaults to 0). `crds: CreateReplace` because Helm never upgrades CRDs by
itself. `driftDetection` (v2) re-applies manually changed objects — ignore HPA-managed fields.
To preview changes, use `flux diff kustomization` or `flux build kustomization`; for a chart, render it locally with `helm template`.

## 5. Day-2 CLI
```bash
flux get all -A                                  # readiness overview
flux reconcile source git apps && flux reconcile kustomization apps --with-source
flux suspend kustomization apps  /  flux resume kustomization apps     # freeze during incidents (also HelmRelease)
flux diff kustomization apps --path ./deploy/prod                        # server-side dry-run diff vs cluster (CI gate)
flux build kustomization apps --path ./deploy/prod | kubectl apply --dry-run=server -f -
flux trace deployment web -n web                 # which Kustomization/source/revision owns this object
flux events --for Kustomization/apps
flux logs --level=error
flux stats; flux tree kustomization apps
```
Common failures: `kustomize build failed` (path/overlay), `dependency 'x' is not ready`,
`health check failed after timeout` (look at the Deployment), exhausted HelmRelease retries
(`flux reconcile hr <name> --reset` resets the failure count), `Secret 'sops-age' not found`.

## 6. Secrets, alerts, tenancy
- SOPS: the Flux SOPS guide stores an age key (file `age.agekey`) in a Secret referenced by
  `decryption.secretRef`; its `.sops.yaml` uses `encrypted_regex: ^(data|stringData)$` so only
  those fields are encrypted.
- Alerts: `Provider` + `Alert` (`notification.toolkit.fluxcd.io/v1`, with `providerRef`,
  `eventSeverity: error` and `eventSources: [{kind: Kustomization, name: '*'}]`) →
  notification-controller dispatches; a `Receiver` ingests Git webhooks.
- Multi-tenancy: `serviceAccountName` per tenant Kustomization, the `--no-cross-namespace-refs=true`
  and `--default-service-account` controller flags (see the Flux multi-tenancy lockdown docs).
- Upgrade Flux: `flux bootstrap` again with the new CLI, or `flux install --export` diff;
  check `flux check` and the release notes for API version changes.

## Verify
- [ ] `flux check` passes; `flux get all -A` is all `Ready=True`.
- [ ] Deleting a manifest from Git prunes the object; `kubectl edit` on a managed Deployment is reverted at next interval.
- [ ] A broken Helm upgrade rolls back automatically (`remediation.strategy: rollback`) and an Alert reaches the channel.
- [ ] `flux diff kustomization` runs in CI on PRs and shows the expected changes.

## Checked

2026-10-25, against the kustomize-controller Kustomization v1 spec, helm-controller HelmRelease v2 spec, source-controller OCIRepository, HelmRepository and GitRepository v1 specs, notification-controller Alert v1 spec, the Flux SOPS and upgrade guides, and flux2 CLI source (`bootstrap*.go`, `push_artifact.go`, `events.go`, `logs.go`, `diff_kustomization.go`, command list). Confirmed: bootstrap flags (`--team`, `--personal`, `--components-extra`, `--deploy-token-auth`, `--private-key-file`), `wait` ignoring `healthChecks`, `dependsOn` readiness, substitution syntax, `force`/`prune`/`ssa` annotations, generated kustomization.yaml, `chartRef`, CRD policy values, `flux events --for`, `flux diff kustomization --path`. Wrong earlier: OCIRepository is `v1` (not v1beta2); Alert uses `eventSeverity`, not `severity`, and is v1; `reconcile: disabled` is not in the documented annotation table (use the `ssa` policy); `flux logs` has no `--since` flag; HelmRepository `type: oci` is in maintenance mode. Removed: Kyverno remark and pinned chart versions.

Method: documentation only; no commands were run.
