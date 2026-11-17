---
id: computing-software.cloud-infrastructure-engineering.linkerd.renew-webhook-tls-secrets
name: renew-webhook-tls-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, webhooks, certificates, rotation, secrets]
level: advanced
status: docs-checked
description: "Check and renew the 365-day TLS certificates used by Linkerd's admission webhooks by deleting the secrets and re-running upgrade."
sources:
  - https://linkerd.io/2.19/tasks/rotating_webhooks_certificates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd's admission webhooks, such as proxy injection and service profile validation, and the Viz tap injector use TLS certificates issued by self-signed CAs embedded in the webhook configuration. They are valid for 365 days by default. Secrets:

- namespace `linkerd`: `linkerd-policy-validator-k8s-tls`, `linkerd-proxy-injector-k8s-tls`, `linkerd-sp-validator-k8s-tls`
- namespace `linkerd-viz`: `tap-injector-k8s-tls`

Check validity with `step`:

```bash
kubectl -n linkerd get secret linkerd-proxy-injector-k8s-tls \
  -ojsonpath='{.data.tls\.crt}' | base64 --decode - | \
  step certificate inspect - | grep -iA2 validity
```

Repeat for each secret (the docs loop over arrays of secret and namespace names).

To renew, delete the secrets and let install or upgrade recreate them. The guide's loop deletes each secret in its namespace, then you re-apply the manifests, for example `linkerd upgrade | kubectl apply -f -` for the control plane and the matching `linkerd viz install` for Viz, or a Helm upgrade for chart installs. This recreates the secrets without restarting Linkerd. Restarting the webhook pods is usually not necessary, but on a large or high-churn cluster it may be advisable, and you should restart them if you see certificate expiry errors or mismatched CA certs. Confirm with `linkerd check`.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/tasks/rotating_webhooks_certificates/. Webhook TLS purpose, 365-day default, secret names and namespaces, the step check command, delete-and-recreate procedure, Helm note, restart guidance.

Removed or reworded: The calendar-reminder and admission-blocking claim (not on the cited page).

Method: documentation only; no commands were run.
