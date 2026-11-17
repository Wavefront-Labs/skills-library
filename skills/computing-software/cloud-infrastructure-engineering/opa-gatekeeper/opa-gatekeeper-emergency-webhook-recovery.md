---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-emergency-webhook-recovery
name: opa-gatekeeper-emergency-webhook-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, emergency, recovery, webhook, validatingwebhookconfiguration, kubectl]
level: intro
status: docs-checked
description: "Restore a cluster blocked by Gatekeeper by deleting its ValidatingWebhookConfiguration, and know what that disables."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/emergency.md", "https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/failing-closed.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper emergency webhook recovery

If Gatekeeper is preventing the cluster from operating correctly, disable the validating webhook. This removes all Gatekeeper admission checks. With the default name:

```sh
kubectl delete validatingwebhookconfigurations.admissionregistration.k8s.io gatekeeper-validating-webhook-configuration
```

Redeploying the webhook configuration re-enables Gatekeeper. This works even when Gatekeeper is fail-closed and down, because Kubernetes does not apply admission webhooks to requests that edit webhook configurations.

Things to prepare before you need it:
- The command assumes the default webhook name was used; if you renamed it, substitute your name.
- If an operator or other process enforces the existence of the webhook resource, it may interfere with recovery, so plan how to deal with it.
- Remember that deleting the configuration drops all Gatekeeper admission checks until it is restored.

The same step is the documented way out of the admission deadlock that can occur when the webhook fails closed.

## Checked

2026-11-08. Confirmed against emergency.md (delete command, default name, redeploy re-enables) and failing-closed.md (webhook configuration edits are not subject to admission webhooks, deadlock mitigation, external-enforcement gotcha). Both read in full. Removed or corrected: the claim that audit flags objects created during the gap (the docs only say that for the default fail-open case); operator wording generalised to match the source.

Method: documentation only; no commands were run.
