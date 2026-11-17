---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-controller-flags-and-namespace-scope
name: sealed-secrets-controller-flags-and-namespace-scope
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, controller-flags, additional-namespaces, all-namespaces, max-unseal-retries, multi-tenant, controller-namespace]
level: advanced
status: docs-checked
description: "Restrict which namespaces the Sealed Secrets controller watches, run per-namespace controllers, tune unseal retries, and point kubeseal at a non-default controller namespace."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets controller flags and namespace scope

Watch scope. By default the controller watches SealedSecrets in all namespaces (`--all-namespaces`, default true). Two ways to narrow it:
- `--additional-namespaces=<ns1>,<ns2>` provides a comma-separated list of namespaces to manage. Make sure roles and rolebindings exist in those namespaces so the controller can manage Secrets there.
- `--all-namespaces=false` (or env `SEALED_SECRETS_ALL_NAMESPACES=false`) watches only the controller's own namespace. Useful in multi-tenant clusters where each tenant runs an isolated controller with independent sealing keys.

Unseal retries: `--max-unseal-retries` sets the maximum number of attempts to unseal a SealedSecret.

Client side, when the controller is not in `kube-system`, kubeseal needs the namespace by flag or variable:

```bash
kubeseal --controller-namespace sealed-secrets <mysecret.json >mysealedsecret.json
export SEALED_SECRETS_CONTROLLER_NAMESPACE=sealed-secrets
```

Controller name defaults to `sealed-secrets-controller`; override with `--controller-name`.

Multiple secrets in one file are supported; `kubeseal --help` lists all client flags. Controller flags are set in the Deployment's pod template, for example via `kubectl edit deployment/sealed-secrets-controller --namespace=kube-system`.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), FAQ sections on namespaces, unseal retries and controller namespace.
Confirmed: `--additional-namespaces`, `--all-namespaces` (default true), `SEALED_SECRETS_ALL_NAMESPACES`, `--max-unseal-retries`, `--controller-namespace`, `SEALED_SECRETS_CONTROLLER_NAMESPACE`, `--controller-name`, default name `sealed-secrets-controller`, multi-secret files.
Removed: a pointer line to other skills.
Method: documentation only; no commands were run.
