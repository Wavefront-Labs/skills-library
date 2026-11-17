---
id: computing-software.cloud-infrastructure-engineering.kyverno.installation
name: installation
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [install, helm, ha, replicas, fail-closed, namespaceselector, reports-server]
level: practitioner
status: docs-checked
description: "Install Kyverno with Helm or release YAML, configure HA replicas per controller, and avoid the fail-closed webhook lockout."
sources:
  - https://kyverno.io/docs/installation/installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run Kyverno in its own Namespace, never `kube-system` or a shared one. Helm is recommended for production.

`helm repo add kyverno https://kyverno.github.io/kyverno/`, `helm repo update`, then `helm install kyverno kyverno/kyverno -n kyverno --create-namespace`. Add `--devel` for alpha, beta or rc charts. Optional Pod Security policies: `helm install kyverno-policies kyverno/kyverno-policies -n kyverno`. Optional Reports Server: `--set reportsServer.enabled=true` (see `reportsServer.waitForReady`, `reportsServer.readinessTimeout`).

YAML: `kubectl create -f https://github.com/kyverno/kyverno/releases/download/<tag>/install.yaml`; only tagged release manifests are supported. `config/install-latest-testing.yaml` on `main` is for experiments only.

HA: the default is four Deployments (admission, background, reports, cleanup) with one replica each. HA needs at least 2 replicas, set per controller: `--set admissionController.replicas=3 --set backgroundController.replicas=2 --set cleanupController.replicas=2 --set reportsController.replicas=2`. The admission controller is required. More replicas do not necessarily mean more performance.

Failure modes:
- Resource webhooks are fail-closed by default; if the API server cannot reach Kyverno, matching requests fail. Chart 2.5.0+ excludes the Kyverno Namespace via a `namespaceSelector` on `kubernetes.io/metadata.name`. Without exclusions, a Pod-matching fail-closed rule plus loss of all Kyverno Pods can block the cluster; recover by manually deleting the ValidatingWebhookConfigurations.
- `objectSelector` labels can be spoofed; prefer `namespaceSelector`.
- Webhook configuration objects cannot be validated or mutated by Kyverno policies.
- If you remove default exclusions, update `resourceFilters` in the ConfigMap.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
