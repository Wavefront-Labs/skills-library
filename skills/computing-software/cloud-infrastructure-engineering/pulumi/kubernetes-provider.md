---
id: computing-software.cloud-infrastructure-engineering.pulumi.kubernetes-provider
name: kubernetes-provider
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-kubernetes, kubeconfig-provider, k8s-provider, pulumi-eks]
level: practitioner
status: docs-checked
description: "Configure the Pulumi kubernetes provider: kubeconfig lookup, kubernetes:context config, explicit Provider instances, and Pulumi annotations."
sources:
  - https://www.pulumi.com/docs/iac/clouds/kubernetes/
  - https://www.pulumi.com/registry/packages/kubernetes/installation-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes provider

Pulumi uses a local kubeconfig if available (or one passed as a provider argument) and talks to the API server with the official Kubernetes client-go library, like kubectl.

**Default provider.** Looks for a kubeconfig in `$KUBECONFIG`, else `~/.kube/config`; if neither exists, authentication fails. A kubeconfig defines contexts (cluster, namespace, user). Select one with config:

```bash
pulumi config set kubernetes:context my-context
```
Settings can be given to the default provider with `pulumi config set kubernetes:<option>`, or to the constructor of a new `kubernetes.Provider` to make a specific instance (see the Provider configuration docs for the option list). Depending on an ambient default context makes a shared stack depend on information Pulumi does not know, which leads to unrepeatable deployments; prefer an explicit provider with the kubeconfig passed in.

Each Kubernetes resource in Pulumi Cloud links to the cluster view; the links are local and need `kubectl proxy` running.

## Annotations Pulumi understands
- `pulumi.com/skipAwait`: when `"true"`, create the resource without waiting for readiness. Not recommended during deletion with server-side apply (race conditions during replacement).
- `pulumi.com/waitFor` (v4.18.0+): custom readiness, e.g. `jsonpath={.phase}=Running`, `condition=Synced`, or a JSON array of expressions that must all hold. Ignored if `skipAwait` is `"true"` or `"ready"`.
- `pulumi.com/deletionPropagationPolicy` (v4.12.0+): `foreground` (default), `background`, `orphan`.
- `pulumi.com/timeoutSeconds` (consider custom timeouts instead), `pulumi.com/replaceUnready` (batch/v1 Job only), `pulumi.com/patchForce` and `pulumi.com/patchFieldManager` (server-side apply).
- Written by the provider: `pulumi.com/autonamed` (autonamed resource) and, outside SSA mode, `app.kubernetes.io/managed-by`.

## Gotchas
- Pulumi has no readiness concept for every resource and may assume some are immediately ready; use `waitFor` or set `PULUMI_K8S_AWAIT_ALL=true` to wait for arbitrary resources.
- Server-side apply is the default since the v4 provider (see `kubernetes-server-side-apply`).

## Checked
2026-11-03. Confirmed on the Kubernetes provider installation and configuration page. Removed: the Deployment/Service TypeScript example, auto-suffix example name, `kubectl get deploy` Verify paragraph, the `enableServerSideApply` setting name (not on the page), cluster-per-stack advice and the `deleteBeforeReplace` claim.
Method: documentation only; no commands were run.
