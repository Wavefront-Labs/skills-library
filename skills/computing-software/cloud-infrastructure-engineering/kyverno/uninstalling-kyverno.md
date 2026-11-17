---
id: computing-software.cloud-infrastructure-engineering.kyverno.uninstalling-kyverno
name: uninstalling-kyverno
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [uninstall, webhook-cleanup, autodeletewebhooks, helm-uninstall, finalizer]
level: practitioner
status: docs-checked
description: "Uninstall Kyverno by Helm or YAML and make sure its webhook configurations are removed, including the autoDeleteWebhooks finalizer option."
sources:
  - https://kyverno.io/docs/installation/uninstallation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
YAML install: `kubectl delete -f https://github.com/kyverno/kyverno/releases/download/<tag>/install.yaml`, using the tag that matches your installed version.

Helm install: find the release namespace and name, then with defaults `helm uninstall kyverno kyverno/kyverno -n kyverno`. Deployments, supporting resources and policy reports are removed.

Webhook cleanup:
- On Helm installs Kyverno by default tries to remove all its webhooks when it terminates. If its RBAC resources are deleted first, it loses permission to do so.
- Make removal finalizer-based with the flag `--autoDeleteWebhooks` on the admission-controller and cleanup-controller Deployments (the page says it will become the default).
- After a YAML uninstall, verify that the webhooks are gone, otherwise matching requests may keep failing with a dead webhook.

Manual removal:
- `kubectl delete mutatingwebhookconfigurations kyverno-policy-mutating-webhook-cfg kyverno-resource-mutating-webhook-cfg kyverno-verify-mutating-webhook-cfg`
- `kubectl delete validatingwebhookconfigurations kyverno-policy-validating-webhook-cfg kyverno-resource-validating-webhook-cfg kyverno-cleanup-validating-webhook-cfg kyverno-exception-validating-webhook-cfg`

CRD removal and stuck resources beyond the finalizer note are not covered by this page.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
