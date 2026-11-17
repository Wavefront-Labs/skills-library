---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-policy-k8s-filtering-demo
name: tetragon-policy-k8s-filtering-demo
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [k8s-filtering-demo, tetragon, kubernetes, tracingpolicynamespaced, lseek]
level: practitioner
status: docs-checked
description: "Walk through Tetragon namespaced, pod-label and container-name policy filtering using an lseek Sigkill policy on minikube or kind."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/k8s-filtering/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon Kubernetes filtering demo

Goal: see namespace, pod-label and container filters change where a policy bites. The demo policy kills a process that calls `sys_lseek` with fd `-1` (a Sigkill is used only because it is easy to observe). The default result of `os.lseek(-1,0,0)` in Python is `OSError: [Errno 9] Bad file descriptor`.

## Setup

Use containerd, install the OCI hooks, then Helm install in `kube-system` with `tetragon.grpc.address="unix:///var/run/tetragon/tetragon.sock"` (minikube: `minikube start --container-runtime=containerd` and `./contrib/tetragon-rthooks/scripts/minikube-install-hook.sh`; kind: `kind create cluster` and `./contrib/tetragon-rthooks/scripts/kind-hook-setup.sh`). Operator logs should show `TracingPolicyNamespaced/v1alpha1` CRD installed; agent logs should include `Enabling policy filtering`.

## Shared policy body

```yaml
  kprobes:
  - call: "sys_lseek"
    syscall: true
    args:
    - index: 0
      type: "int"
    selectors:
    - matchArgs:
      - index: 0
        operator: "Equal"
        values:
        - "-1"
      matchActions:
      - action: Sigkill
```

## Variants

1. Namespaced: `kind: TracingPolicyNamespaced`, name `lseek-namespaced`, applied with `kubectl apply -n default`. A python pod in `default` is killed (`pod default/test terminated (Error)`), including newly started ones; a pod in namespace `test` still gets Errno 9.
2. Pod label: `kind: TracingPolicy`, name `lseek-podfilter`, add `spec.podSelector.matchLabels: {app: "lseek-test"}`. Only pods run with `--labels "app=lseek-test"` are killed.
3. Container field: name `lseek-containerfilter`, add `spec.containerSelector.matchExpressions` with key `name`, operator `In`, values `main`. In a pod with containers `main` and `sidecar`, exec into `main` ends with `command terminated with exit code 137`; `sidecar` is unaffected.

Run the python containers with `kubectl run test --image=python -it --rm --restart=Never -- python`.

## Checked

2026-11-08. Read the Kubernetes identity aware policies page in full, including the demo section (raw docs markdown). Checked setup, shared policy body and the three variants against it; no claims removed.

Method: documentation only; no commands were run.
