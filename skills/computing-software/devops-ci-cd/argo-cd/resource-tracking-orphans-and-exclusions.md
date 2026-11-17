---
id: computing-software.devops-ci-cd.argo-cd.resource-tracking-orphans-and-exclusions
name: resource-tracking-orphans-and-exclusions
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, resource-tracking, tracking-method, annotation-tracking, label-tracking, annotation-plus-label, app-instance-label, application-instancelabelkey, orphaned-resources, orphaned-resources-warning, resource-exclusions, resource-inclusions, resource-customizations, shared-resources, ownership-conflict, sharedresourcewarning, install-id, cluster-scoped-resources, helm-rendered-labels, 63-char-label-limit, gitops, kubernetes]
level: practitioner
status: docs-checked
description: "Control what Argo CD claims as its own: annotation vs label tracking, the 63-char label limit, orphaned-resource warnings, resource exclusions and inclusions, shared resources."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/resource_tracking/", "https://argo-cd.readthedocs.io/en/stable/user-guide/orphaned-resources/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource tracking, orphans and exclusions

**Goal:** Argo CD knows exactly which live objects belong to which Application, flags
the ones nobody owns, and ignores the noise it should never watch.

## 1. Tracking methods (argocd-cm)
```yaml
data:
  application.resourceTrackingMethod: annotation      # annotation (default) | annotation+label | label
  application.instanceLabelKey: argocd.argoproj.io/instance   # custom label key, for label tracking
  installationID: prod-argo                            # distinguishes Argo CD instances sharing a cluster
```
- **label** (`app.kubernetes.io/instance=<app>`): other tools (several Helm charts and operators)
  also write this label and can confuse Argo CD about the owner; labels are truncated to
  **63 characters**, which matters for long app names.
- **annotation** (`argocd.argoproj.io/tracking-id: <app>:<group>/<kind>:<ns>/<name>`):
  the default; no clashes with other Kubernetes tools and Argo CD is never confused about the owner of a resource.
  If the annotation does not reference the resource it sits on (group, kind, name, namespace), the resource
  does not affect the app's sync status and is not pruned.
- **annotation+label**: annotation for tracking plus the label for humans/tools that
  select by it (label value truncated at 63 chars but not used for tracking).
Switching methods: after changing the value, sync your applications again (or wait for the
sync mechanism) to apply it; you can revert by changing the ConfigMap again.
`application.instanceLabelKey` replaces the label key used for label tracking.

## 2. Shared and conflicting resources
By default Argo CD applies all manifests in an app's Git path even if another Application
already applied the same object. With the `FailOnSharedResource=true` sync option the sync
fails when it finds a resource already applied by another Application. Resolve by moving the
object to one app rather than duplicating it.

## 3. Orphaned resources (AppProject)
```yaml
kind: AppProject
spec:
  orphanedResources:
    warn: true          # warn on apps in this project whose target namespace has orphaned resources
    ignore:
      - { group: "", kind: Secret, name: "*token*" }   # name can be a glob
      - { group: cilium.io, kind: CiliumEndpoint }
```
Orphan = a top-level namespaced resource that belongs to no Application, in a namespace an
app in this project targets. Find them on the application details page with the "Show
Orphaned" filter. Never orphaned: namespaced resources denied in the project, the `default`
ServiceAccount (and its token), Service `kubernetes` in `default`, ConfigMap `kube-root-ca.crt`.
Other operators' generated objects (for example cert-manager Secrets) count as orphans: add
them to `ignore`. `warn: false` still lets users view orphans in the UI. Enabling monitoring
has performance cost on namespaces with many unmanaged objects (for example kube-system):
use it on well-scoped projects.

## 4. Resource exclusions and inclusions (argocd-cm)
```yaml
data:
  resource.exclusions: |
    - apiGroups: ["cilium.io"]
      kinds: ["CiliumIdentity", "CiliumEndpoint"]
      clusters: ["*"]
    - apiGroups: ["*"]
      kinds: ["Event"]
      clusters: ["*"]
    - apiGroups: ["velero.io"]
      kinds: ["*"]
      clusters: ["https://prod-*"]
  resource.inclusions: |            # default is include everything; final set = inclusions minus exclusions
    - apiGroups: ["", "apps", "batch", "networking.k8s.io", "argoproj.io"]
      kinds: ["*"]
      clusters: ["*"]
```
Why: excluded resources are left out of discovery and sync, so Argo CD is unaware of them.
By default all group/kinds are included; `events.k8s.io/*`, `metrics.k8s.io/*` and
`coordination.k8s.io/Lease` are always excluded. Exclude only kinds that no app deploys,
since Argo CD will not see them.

## 5. Related knobs
- `resource.customizations` (health and diff ignores per kind) lives in the same ConfigMap;
  see the Argo CD docs for `ignoreResourceUpdates` and the health and diffing pages.

## 6. Gotchas
- Other tools (for example HNC) can copy a resource to another namespace; with annotation
  tracking a copied resource whose tracking annotation names the original does not affect the app's sync status.
- Several Argo CD instances managing one cluster need `installationID` set; each managed
  resource then carries `argocd.argoproj.io/installation-id`, and apps with the same name in
  different instances do not conflict.

## Checked
2026-10-31. Confirmed against the Argo CD Resource Tracking, Orphaned Resources Monitoring and Declarative Setup (exclusions/inclusions) pages and Sync Options (FailOnSharedResource). Corrected: annotation is the default method (not label); inclusions minus exclusions; always-excluded kinds. Removed: version gates (2.12+, 2.8+), SharedResourceWarning, `--orphaned` and `get-reconcile-results` commands, restart and rename advice, hook and whitelist notes.
Method: documentation only; no commands were run.

## Verify
- [ ] `argocd-cm` has `application.resourceTrackingMethod: annotation`; app names > 63 chars still track.
- [ ] An object applied by hand into a managed namespace appears under "Show Orphaned".
- [ ] No kind that an app deploys is excluded.
- [ ] Two apps claiming one Deployment fail the sync when `FailOnSharedResource=true` is set.
