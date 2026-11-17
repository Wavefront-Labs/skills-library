---
id: computing-software.cloud-infrastructure-engineering.istio.istio-ext-authz-custom-action
name: istio-ext-authz-custom-action
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, ext-authz, custom-authz, extension-provider]
level: practitioner
status: docs-checked
description: "Configure an ext_authz provider in meshConfig and reference it from an AuthorizationPolicy with action CUSTOM, and plan for failure behaviour."
sources: ["https://istio.io/latest/docs/tasks/security/authorization/authz-custom/", "https://istio.io/latest/docs/reference/config/istio.mesh.v1alpha1/", "https://istio.io/latest/docs/reference/config/security/authorization-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Istio can call an external authorization server (OPA, oauth2-proxy). Declare the provider in mesh config, then select it from a policy.

```yaml
# meshConfig
extensionProviders:
- name: my-authz
  envoyExtAuthzGrpc: {service: authz.auth.svc.cluster.local, port: 9000}
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: ext, namespace: shop}
spec:
  selector: {matchLabels: {app: web}}
  action: CUSTOM
  provider: {name: my-authz}
  rules: [{to: [{operation: {paths: ["/admin/*"]}}]}]
```

Gotchas: `failOpen` defaults to false, so a request is rejected with Forbidden if the authorization service cannot be reached or returns a 5xx; set `failOpen: true` only deliberately. The provider `timeout` defaults to 600s; when it expires the call counts as failed and `failOpen` decides the outcome. When CUSTOM, DENY and ALLOW policies apply to one workload, CUSTOM is evaluated first, then DENY, then ALLOW.

Verify: a request to `/admin/x` calls the authorization service and returns its decision, while `/public` does not call it.

## Checked

2026-11-03. Confirmed in the Istio external authorization task (`extensionProviders`, `envoyExtAuthzGrpc`, `action: CUSTOM`, `provider.name`), the mesh config reference (`failOpen` default false, `timeout` default 600s) and the AuthorizationPolicy reference (CUSTOM, then DENY, then ALLOW). Removed: the replica and load-test advice and the ownership advice.

Method: documentation only; no commands were run.
