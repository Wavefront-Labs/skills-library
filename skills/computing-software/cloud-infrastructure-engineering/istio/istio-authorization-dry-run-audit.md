---
id: computing-software.cloud-infrastructure-engineering.istio.istio-authorization-dry-run-audit
name: istio-authorization-dry-run-audit
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, authz-dry-run, dry-run, policy-rollout]
level: practitioner
status: docs-checked
description: "Use the istio.io/dry-run annotation on an AuthorizationPolicy to see what would be denied in logs and metrics before enforcing it."
sources: ["https://istio.io/latest/docs/tasks/security/authorization/authz-dry-run/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before enforcing a new deny rule on live traffic, mark it dry-run. The proxy evaluates it and records the result without blocking.

```yaml
metadata:
  name: deny-delete
  namespace: shop
  annotations:
    "istio.io/dry-run": "true"
spec:
  selector: {matchLabels: {app: web}}
  action: DENY
  rules: [{to: [{operation: {methods: ["DELETE"]}}]}]
```

To turn an existing policy into a dry run: `kubectl annotate --overwrite authorizationpolicies deny-delete -n shop istio.io/dry-run='true'`.

The docs describe the annotation as experimental. Results appear in three places: the proxy debug log, a Prometheus metric, and Zipkin trace tags. For the log, first enable debug logging for the RBAC filter with `istioctl proxy-config log deploy/<name> --level rbac:debug`, then search the sidecar log for `shadow denied`; the line names the matched policy, for example `shadow denied, matched policy ns[foo]-policy[deny-path-headers]-rule[0]`.

```sh
kubectl logs <pod> -n shop -c istio-proxy | grep "shadow denied"
```

Verify: a DELETE request still succeeds while the log shows `shadow denied` for it; after removing the annotation the policy is enforced.

## Checked

2026-11-03. Confirmed in the Istio authorization dry-run task: the `istio.io/dry-run: "true"` annotation, the `kubectl annotate` form, the experimental label, `rbac:debug` log level, the `shadow denied, matched policy ...` log format, and the Prometheus and Zipkin result paths. Removed: `shadow_effective_policy_id`, the ambient/ztunnel remark, and the audit-duration advice (not on the page).

Method: documentation only; no commands were run.
