---
id: computing-software.cloud-infrastructure-engineering.cert-manager.uninstalling
name: uninstalling
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [uninstall, helm-uninstall, backup, crds, cleanup]
level: intro
status: docs-checked
description: "Remove cert-manager by following the uninstall path that matches how it was installed, after backing up custom resources you cannot recreate."
sources:
  - https://cert-manager.io/docs/installation/uninstall/
  - https://cert-manager.io/docs/installation/kubectl/
  - https://cert-manager.io/docs/installation/helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The uninstall landing page applies to Kubernetes and OpenShift, and only routes you: pick the section matching your install method (kubectl or Helm). It lists no commands itself.

Before removing anything, back up Certificate, Issuer and other custom resources that are not in version control (see the backup and restore guide).

Helm path:
1. List user resources: `kubectl get Issuers,ClusterIssuers,Certificates,CertificateRequests,Orders,Challenges --all-namespaces` and delete them.
2. `helm uninstall cert-manager -n cert-manager`.
3. CRDs are kept by default to prevent data loss; deleting a CRD deletes all its resources. Releases before v1.15.0 deleted the CRDs on uninstall.

kubectl path: after clearing user resources, `kubectl delete -f` the original `cert-manager.yaml` release URL. This also deletes the CRDs and every cert-manager custom resource. TLS Secrets carrying cert-manager owner references may go too (`--enable-certificate-owner-ref` defaults to false).

Leftovers to clear if they appear:
- Namespace stuck Terminating: `kubectl delete apiservice v1beta1.webhook.cert-manager.io`.
- Orphaned leader-election leases: delete `cert-manager-cainjector-leader-election` and `cert-manager-controller` leases in their namespace (default `kube-system`).

## Checked

2026-11-03: Confirmed against the Uninstalling landing page and the kubectl and Helm installation pages: the landing page only routes by install method and points to backup and restore, the shared pre-uninstall resource listing, `helm uninstall cert-manager -n cert-manager`, CRDs kept by default with the pre-v1.15.0 exception, `kubectl delete -f` of the release manifest removing CRDs, `--enable-certificate-owner-ref` default false, the stuck-namespace APIService fix, and orphaned lease cleanup with default `kube-system`. Nothing removed.

Method: documentation only; no commands were run.
