---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-usecase-process-lifecycle
name: tetragon-usecase-process-lifecycle
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [usecase-proc-exec, tetragon, process-execution, container-escape, kubernetes]
level: practitioner
status: docs-checked
description: "Monitor process execution, exit, privileged pods and namespace escapes with Tetragon events and TracingPolicies on Kubernetes."
sources:
  - "https://tetragon.io/docs/use-cases/process-lifecycle/"
  - "https://tetragon.io/docs/use-cases/process-lifecycle/process-execution/"
  - "https://tetragon.io/docs/use-cases/process-lifecycle/advanced-process-execution/"
  - "https://tetragon.io/docs/use-cases/process-lifecycle/privileged-execution/"
  - "https://tetragon.io/docs/use-cases/process-lifecycle/namespace-access/"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/tracingpolicy/process-exec/process-exec-elf-begin.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon process lifecycle monitoring

Goal: see which binaries run, with what privileges, and whether a process tries to leave its container.

## Default exec and exit events
With default configuration Tetragon emits `process_exec` and `process_exit` events. They carry binary, arguments, UID, parent, start time, exit status and signals, plus Kubernetes namespace, pod and labels. `exec_id` correlates all activity of one process.

Watch a pod in compact form:

```bash
kubectl logs -n kube-system -l app.kubernetes.io/name=tetragon -c export-stdout -f | tetra getevents -o compact --namespace default --pod xwing
```

Raw JSON: pipe the same logs into `jq 'select(.process_exec.process.pod.name=="xwing" or .process_exit.process.pod.name=="xwing")'`.

## ELF binary execution
Apply the `process-exec-elf-begin` TracingPolicy, which hooks `security_bprm_creds_from_file`:

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: "process-exec-elf-begin"
spec:
  kprobes:
  - call: "security_bprm_creds_from_file"
    syscall: false
    args:
    - index: 0
      type: "nop"
    - index: 1
      type: "file"
```

It yields `process_kprobe` events with `function_name` and a `file_arg` path (the final ELF or flat binary, not script handlers). Remove with `kubectl delete -f`.

## Capabilities and namespaces
Edit the configmap (`kubectl edit cm -n kube-system tetragon-config`), set `enable-process-cred: true` and `enable-process-ns: true`, then `kubectl rollout restart -n kube-system ds/tetragon`. Privileged pods then show, for example, a `CAP_SYS_ADMIN` marker in compact output.

## Container escape via setns
Hook `sys_setns` (syscall: true) with two `int` args (index 0 namespace fd, index 1 namespace type flag) to catch `nsenter -t 1 -m -u -n -i -p`. To block, add a selector with `matchPIDs` (operator `NotIn`, `followForks: true`, `isNamespacePID: true`, values 0 and 1) and `matchActions` action `Sigkill`. Consult the Enforcement docs before production use.

## Checked

2026-11-08. Read the process lifecycle index and its four subpages in full (process execution, advanced process execution, privileged execution, namespace access) plus the process-exec-elf-begin example policy; added those pages as sources because the claims come from them. No claims removed.

Method: documentation only; no commands were run.
