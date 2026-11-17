---
id: computing-software.cloud-infrastructure-engineering.cert-manager.kubectl-install
name: kubectl-install
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [kubectl-apply, static-manifest, cmctl-check-api, install, leases, finalizers]
level: intro
status: docs-checked
description: "Install, verify and uninstall cert-manager from the static kubectl manifest, with fixes for orphaned leases, stuck namespaces and stuck Challenges."
sources:
  - https://cert-manager.io/docs/installation/kubectl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Needs kubectl v1.19.0 or later (older versions have trouble updating CRDs).

Install: `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/<version>/cert-manager.yaml`. The default namespace is `cert-manager`; any other requires editing the Deployment manifests.

Verify: `kubectl get pods --namespace cert-manager` should show `cert-manager`, `cert-manager-cainjector` and `cert-manager-webhook` Running (the webhook may start later). With cmctl, `cmctl check api` (add `--wait=2m` to block) prints "The cert-manager API is ready".

Uninstall: delete your own resources first (`kubectl get Issuers,ClusterIssuers,Certificates,CertificateRequests,Orders,Challenges --all-namespaces`), then `kubectl delete -f` the same manifest URL. This also deletes CRDs and all custom resources. TLS Secrets with cert-manager owner references may be deleted; `--enable-certificate-owner-ref` defaults to false.

Failure modes:
- Orphaned leases (default namespace `kube-system`): `kubectl delete lease -n <namespace> cert-manager-cainjector-leader-election cert-manager-controller`.
- Namespace stuck Terminating: `kubectl delete apiservice v1beta1.webhook.cert-manager.io`.
- Challenges stuck pending: delete the `cert-manager-webhook` mutatingwebhookconfigurations and validatingwebhookconfigurations, then `kubectl edit challenge <name>` and empty `.metadata.finalizers`.

## Checked

2026-11-03: Confirmed against the kubectl installation page: kubectl v1.19.0 or later, the `cert-manager.yaml` release manifest, default `cert-manager` namespace, the three pods to verify, `cmctl check api` with `--wait=2m`, the uninstall order and pre-uninstall resource listing, CRD deletion with the manifest, the `--enable-certificate-owner-ref` default of false, orphaned lease cleanup with default `kube-system`, the `v1beta1.webhook.cert-manager.io` APIService fix, and the stuck Challenge finalizer procedure. Nothing removed.

Method: documentation only; no commands were run.
