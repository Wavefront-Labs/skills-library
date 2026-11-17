---
id: computing-software.cloud-infrastructure-engineering.kubernetes.tetragon-ebpf-enforcement-policies
name: tetragon-ebpf-enforcement-policies
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, tetragon, ebpf, tracingpolicy, runtime-security, runtime-enforcement, cilium, cks]
level: advanced
status: docs-checked
description: "Observe and block process, file and network behaviour in-kernel with Tetragon TracingPolicies: kprobe selectors, Sigkill and Override actions, namespacing, and safe rollout."
sources: ["https://tetragon.io/docs/getting-started/install-k8s/", "https://tetragon.io/docs/concepts/tracing-policy/", "https://tetragon.io/docs/concepts/tracing-policy/selectors/", "https://tetragon.io/docs/concepts/tracing-policy/k8s-filtering/", "https://github.com/cilium/tetragon/blob/main/examples/quickstart/file_monitoring.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon eBPF enforcement

Falco detects after the syscall returns. Tetragon runs eBPF programs on kernel functions and
can **kill the process or fail the call synchronously**, so the action never completes.

## Install and watch
```bash
helm repo add cilium https://helm.cilium.io
helm install tetragon cilium/tetragon -n kube-system
kubectl -n kube-system rollout status ds/tetragon
# process exec/exit events are on by default
kubectl exec -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact --pods <pod>
```
The `ds/tetragon` form reaches one Tetragon pod: on a multi-node cluster exec into the Tetragon pod
on the same node as the workload. Events from `kube-system` are filtered by default.

## Policy: observe first
```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata: {name: watch-etc-writes}
spec:
  kprobes:
  - call: security_file_permission
    syscall: false
    args:
    - {index: 0, type: file}
    - {index: 1, type: int}          # access mask, 2 = MAY_WRITE
    selectors:
    - matchArgs:
      - {index: 0, operator: Prefix, values: [/etc/]}
      - {index: 1, operator: Equal, values: ["2"]}
```
Events show pod, container, binary and full process ancestry.

## Then enforce
Add an action to the selector:
```yaml
      matchActions:
      - action: Sigkill            # kill the offending process
```
or `action: Override` with `argError: -1` to make the call return an error. Override uses the
kernel error-injection framework: it needs `CONFIG_BPF_KPROBE_OVERRIDE`, works on functions annotated
for error injection (listed in `/sys/kernel/debug/error_injection/list`), and on `security_` hooks
from kernel 5.7.

## Scope it
- `TracingPolicyNamespaced` restricts the policy to one namespace.
- `podSelector` and `containerSelector` in the spec narrow further.
- `matchBinaries` (`operator: NotIn`) to allow the legitimate writer (e.g. a config agent).

## Rollout rules
1. Ship observe-only, collect events for a release cycle (export JSON to your log
   pipeline using Tetragon's event export options).
2. Enforce in staging with real traffic; a too-broad Sigkill on a hot kernel function
   kills system daemons.
3. Scope by namespace in production; never enforce on kube-system first.
4. Kernel versions differ in function names/signatures: test on every node OS image you run.

## Verify
```bash
kubectl exec -n kube-system ds/tetragon -c tetragon -- tetra tracingpolicy list
kubectl exec -n shop deploy/api -- sh -c 'echo x >> /etc/hosts'    # the shell is killed when the policy has Sigkill
kubectl exec -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact --pods <pod>
```

## Checked

Checked 2026-10-27 against the Tetragon docs source (cilium/tetragon, main branch docs) and the quickstart `file_monitoring.yaml`.

- Helm install (`cilium` repo, `cilium/tetragon`, namespace `kube-system`, `rollout status ds/tetragon`), `tetra getevents -o compact --pods`, default filtering of `kube-system` events confirmed.
- `security_file_permission` kprobe with `file` and `int` args, `Prefix`/`Equal` operators and the MAY_WRITE (2) and MAY_READ (4) masks confirmed in the quickstart policy.
- `Sigkill` and `Override` actions, `argError`, `CONFIG_BPF_KPROBE_OVERRIDE`, error-injection function list and `security_` hooks from kernel 5.7 confirmed in the selectors page; `matchBinaries` with `In`/`NotIn`, `TracingPolicyNamespaced`, `podSelector` and `containerSelector` confirmed.
- Removed unconfirmed claims: operation without Cilium CNI, exit code 137, `kubectl get tracingpolicies,...` resource names (replaced with `tetra tracingpolicy list`), the exec command's `--namespace` flag.

Method: documentation only; no commands were run.
