---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-debugging-request-objects-and-tracing
name: opa-gatekeeper-debugging-request-objects-and-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, debug, tracing, config, deny-all, log-level, templates]
level: practitioner
status: docs-checked
description: "Debug Gatekeeper policies by dumping the review object with a deny-all template, enabling traces in the Config resource, and reading template build errors."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/debug.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper debugging request objects and tracing

Verbose logs: `--log-level=DEBUG` (default INFO; values DEBUG, INFO, WARNING, ERROR). Do not leave DEBUG on in production.

See the request object: apply a template that denies everything and prints the input, scoped by a constraint:

```yaml
targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package k8sdenyall
      violation[{"msg": msg}] {
        msg := sprintf("REVIEW OBJECT: %v", [input.review])
      }
```

Tracing is deliberately opt-in because dumping cached data, evaluation traces and input for every request is expensive. Configure the Config resource in `gatekeeper-system`:

```yaml
spec:
  validation:
    traces:
      - user: "user_to_trace@company.com"
        kind: {group: "", version: "v1", kind: "Namespace"}
        dump: "All"
```

`user` is required (use a controller service account to trace controllers); `dump: All` also dumps OPA state. Traces go to the controller stdout.

Rego errors: a template with bad Rego may still be created. Applying a constraint then fails with `no matches for kind ... in version constraints.gatekeeper.sh/v1beta1`. Run `kubectl get -f <template-file> -o yaml` and read build errors in `status`.

## Checked

2026-11-08. Confirmed against debug.md, read in full (log-level values and default, deny-all template and constraint, traces fields and required user, dump All, stdout, build-error behaviour and status field). Removed or corrected: nothing.

Method: documentation only; no commands were run.
