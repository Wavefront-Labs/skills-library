---
id: computing-software.devops-ci-cd.helm.kubernetes-api-deprecations
name: kubernetes-api-deprecations
category: computing-software
field: devops-ci-cd
product: helm
tags: [api-deprecations, deprecated-apis, capabilities, apiversion, removed-apis, mapkubeapis]
level: advanced
status: docs-checked
description: "Handling removed Kubernetes APIs in charts and releases: Capabilities checks, kubeVersion and fixing stored manifests."
sources:
  - "https://helm.sh/docs/topics/kubernetes_apis/"
  - "https://helm.sh/docs/chart_template_guide/builtin_objects/"
  - "https://helm.sh/docs/helm/helm_template/"
  - "https://helm.sh/docs/helm/helm_lint/"
  - "https://helm.sh/docs/topics/charts/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Kubernetes retires API versions over time (see its deprecation policy). The release manifest is stored in the cluster in a Secret (default) or ConfigMap, one per revision, so after a cluster upgrade removes an API version used by the deployed release, `helm upgrade` fails: "UPGRADE FAILED: current release manifest contains removed kubernetes api(s) ... no matches for kind ... in version ...". Helm cannot build the diff against the old objects and can no longer manage such a release until its stored manifest is repaired.

Audit: chart maintainers check templates for deprecated or removed `apiVersion`/`kind` pairs (for example `apps/v1beta1` Deployment, removed in Kubernetes 1.16) and release a new chart version. Users audit the charts they use and their deployed releases, for example with `helm get manifest`.

If only deprecated (not yet removed) versions are found, run `helm upgrade` with a chart version using supported APIs, and note in the upgrade description not to roll back to a release before it. The recommended practice is to upgrade releases to supported APIs before upgrading to a cluster that removes the old ones.

Prevention:

- Update templates to the supported `apiVersion` before the cluster upgrade.
- Guard by capability so one chart works across versions (`Capabilities.APIVersions.Has` accepts a version such as `batch/v1` or a resource such as `apps/v1/Deployment`):

```yaml
{{- if .Capabilities.APIVersions.Has "networking.k8s.io/v1/Ingress" }}
apiVersion: networking.k8s.io/v1
{{- else }}
apiVersion: networking.k8s.io/v1beta1
{{- end }}
```

- Declare the supported range in `kubeVersion`.
- Render for a target version without a cluster: `helm template --kube-version 1.31.0 --api-versions networking.k8s.io/v1 ./chart` (`--kube-version` sets `Capabilities.KubeVersion`, `-a/--api-versions` sets `Capabilities.APIVersions`).
- `helm lint --kube-version` sets the Kubernetes version used for capabilities and deprecation checks.

Repair when the stored manifest already holds removed APIs:

- The Helm `mapkubeapis` plugin (helm/helm-mapkubeapis) updates a release to supported APIs; see its readme.
- Manually: take the latest deployed release Secret or ConfigMap (labels `owner=helm,status=deployed,name=<release_name>`), back it up, decode `data.release` (Secret: base64 twice then gzip; ConfigMap: base64 then gzip), change API versions in the `manifest` field, re-encode, replace `data.release`, apply it, then `helm upgrade` with a chart using supported APIs.

## Checked

2026-11-08. Read the Deprecated Kubernetes APIs page in full, plus helm template, helm lint, Built-in Objects and Charts topic pages. Corrected the failure mode (helm upgrade fails; rollback claim removed), removed an unsupported CI tip, added the audit steps, mapkubeapis and manual repair procedure.

Method: documentation only; no commands were run.
