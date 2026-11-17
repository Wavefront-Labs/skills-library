---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-webhook-provider-debugging
name: external-secrets-operator-webhook-provider-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [webhook-provider, troubleshooting, secretstore-status, labels]
level: advanced
status: docs-checked
description: "Debug the ESO webhook provider through store status, label requirements and templating pitfalls."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/webhook.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start with `kubectl describe secretstore NAME -n NS` (or `clustersecretstore NAME`). `Ready=False` with reason `InvalidProviderConfig` means client creation or validation failed, and the event holds the specific error; `ProviderNotFound` means the provider could not be resolved at all. For per-secret failures describe the `ExternalSecret`. Run the controller with `--loglevel debug` for reconcile decisions.

There is deliberately no request or response dump, since templated url, headers and body contain credentials. `GODEBUG=http2debug=2` does dump frames with authorization headers unredacted; never use it in production. Use a logging proxy instead.

Pitfalls:
- Every Secret the webhook reads, including NTLM secrets and generator `spec.secrets`, needs the label `external-secrets.io/type: webhook`, otherwise lookup fails.
- Secrets are exposed as `.<name>.<keyInSecret>` (two levels), so `{{ .creds.username }}`; `{{ .creds }}` renders a Go map, and a `key` on the secretRef does not narrow it.
- The `url` is checked for reachability before templating, so a templated host fails validation. Keep the host literal and template only path or query.

## Checked

2026-11-03. Claims were read against provider/webhook.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
