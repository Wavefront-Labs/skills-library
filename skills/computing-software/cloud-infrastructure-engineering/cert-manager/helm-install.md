---
id: computing-software.cloud-infrastructure-engineering.cert-manager.helm-install
name: helm-install
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [helm, crds-enabled, oci-chart, install, jetstack, apiservice]
level: intro
status: docs-checked
description: "Install cert-manager with Helm from the OCI chart with crds.enabled, handle subchart and template caveats, and clear a Terminating namespace."
sources:
  - https://cert-manager.io/docs/installation/helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: Helm 3 or later and a supported Kubernetes or OpenShift version.

Install from the OCI chart (recommended):

`helm install cert-manager oci://quay.io/jetstack/charts/cert-manager --version <version> --namespace cert-manager --create-namespace --set crds.enabled=true`

To verify the chart signature, download the GPG keyring from `cert-manager.io/public-keys/` and add `--verify --keyring <file>`.

The legacy repo (`helm repo add jetstack https://charts.jetstack.io --force-update`) updates a few hours after OCI charts. Versions earlier than v1.12 exist only there.

Other values shown: `prometheus.enabled=false`, `webhook.timeoutSeconds=4`. The full list is on ArtifactHub.

Caveats:
- Never embed cert-manager as a subchart; it manages cluster-scoped resources. If you must, override the namespace with `cert-manager.namespace`.
- `helm template ... > cert-manager.custom.yaml` emits no Namespace and ignores `--create-namespace`; create the namespace yourself.

Uninstall: delete user resources first (`kubectl get Issuers,ClusterIssuers,Certificates,CertificateRequests,Orders,Challenges --all-namespaces`), then `helm uninstall cert-manager -n cert-manager`. CRDs are kept by default; deleting them removes every resource of those kinds. Before v1.15.0 uninstall deleted CRDs, so back up first.

Failure mode: namespace stuck in Terminating because of a leftover APIService. Fix: `kubectl delete apiservice v1beta1.webhook.cert-manager.io`.

## Checked

2026-11-03: Confirmed against the Helm installation page: Helm 3 or later, OCI chart `oci://quay.io/jetstack/charts/cert-manager` with `crds.enabled=true`, `--verify --keyring` with a downloaded GPG keyring, the legacy repository lag and v1.12 cutoff, the example values `prometheus.enabled=false` and `webhook.timeoutSeconds=4`, ArtifactHub values list, the subchart warning and `cert-manager.namespace` override, `helm template` Namespace caveat, uninstall steps, CRDs kept and the pre-v1.15.0 behaviour, and the stuck-namespace APIService fix. Nothing removed.

Method: documentation only; no commands were run.
