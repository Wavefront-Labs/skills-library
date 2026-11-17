---
id: computing-software.cloud-infrastructure-engineering.kubernetes.immutable-containers-at-runtime
name: immutable-containers-at-runtime
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, runtime-security, container-immutability, readonlyrootfilesystem, securitycontext, distroless]
level: practitioner
status: docs-checked
description: "Make containers immutable at runtime (readOnlyRootFilesystem, emptyDir for writable paths, no shell, dropped capabilities) and detect drift, a CKS topic."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/security-context/", "https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://github.com/falcosecurity/rules/blob/main/rules/falco_rules.yaml", "https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutable containers

Goal: an attacker with code execution cannot persist, download tools or modify binaries.
The Pod Security `restricted` standard already requires `allowPrivilegeEscalation: false`,
`runAsNonRoot` and dropping `ALL` capabilities; `readOnlyRootFilesystem` is not part of it.

## Pod spec
```yaml
spec:
  containers:
  - name: app
    image: registry.example.com/app@sha256:...      # immutable reference
    securityContext:
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
      runAsNonRoot: true
      capabilities: {drop: [ALL]}
    volumeMounts:
    - {name: tmp, mountPath: /tmp}
    - {name: cache, mountPath: /var/cache/app}
  volumes:
  - {name: tmp, emptyDir: {sizeLimit: 100Mi}}
  - {name: cache, emptyDir: {sizeLimit: 500Mi}}
```
Find the paths the app writes before enabling it: run the workload in staging with
`readOnlyRootFilesystem: true` and watch for read-only filesystem errors.

## Image side
- Distroless or minimal images: no shell, package manager or curl for an attacker.
- Pin by digest so the same bytes run everywhere.

## Common breakages
| Error | Fix |
|---|---|
| The application cannot write to its cache, run or temp directory | mount an `emptyDir` at that path |
| Python writing `.pyc` | `PYTHONDONTWRITEBYTECODE=1` |

## Detect drift anyway
the Falco rule "Drop and execute new binary in container" (an executable that is not part of the
image's base layers is run) and Tetragon TracingPolicies on process execution. Exec into
production pods should alert.

## Verify
```bash
kubectl exec <pod> -- touch /test 2>&1      # Read-only file system
kubectl get pod <pod> -o jsonpath='{.spec.containers[*].securityContext.readOnlyRootFilesystem}'
```

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time), the Falco default rules (falcosecurity/rules, main) and the CPython command line docs.

- `readOnlyRootFilesystem`, `allowPrivilegeEscalation` (defaults to true when unset) and capabilities fields confirmed in the security context page; Restricted profile requiring drop `ALL` confirmed in the Pod Security Standards page.
- Falco rule "Drop and execute new binary in container" confirmed in the default rules; "Write below binary dir" is not in the current stable or incubating rule files, so it was removed.
- `PYTHONDONTWRITEBYTECODE` confirmed in the CPython docs.
- Removed unconfirmed claims: nginx and Java error strings, the `find -newer /proc/1` heuristic, Tetragon execve-of-new-files claim.

Method: documentation only; no commands were run.
