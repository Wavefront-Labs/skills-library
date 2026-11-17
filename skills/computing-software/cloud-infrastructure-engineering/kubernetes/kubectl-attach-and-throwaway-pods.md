---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-attach-and-throwaway-pods
name: kubectl-attach-and-throwaway-pods
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-debug, kubectl-attach, kubectl-run, interactive, troubleshooting]
level: practitioner
status: docs-checked
description: "Use kubectl attach and kubectl run -it --rm for interactive throwaway pods and for attaching to a running container's stdin and stdout, and detach safely."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_attach/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_run/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kubectl/pkg/cmd/run/run.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl attach and throwaway pods

## attach vs exec
- `kubectl exec` starts a new process in the container.
- `kubectl attach` connects to the container's main process streams (stdin, stdout, stderr); you
  see what it prints and can type into it if the container has `stdin: true`.

```bash
kubectl attach web-7c9 -c app            # stream output of the main process
kubectl attach -it shell-pod             # interactive, container must have stdin and tty
```
`kubectl attach` and `kubectl run` accept `--detach-keys` to set the detach key sequence;
the `kubectl run` flag defaults to `ctrl-p,ctrl-q`. `Ctrl-C` or `exit` goes to the process and
may end it; with `restartPolicy: Never` the pod then completes.

## Throwaway interactive pods
```bash
kubectl run tmp --rm -it --image=busybox:1.36 --restart=Never -- sh
```
`--rm` deletes the pod after it exits and is only valid for attached containers (`-i` or
`--attach`). `--restart=Never` creates a bare pod that is not restarted (the flag defaults to
`Always`). `kubectl run` labels the pod `run=<name>` unless you pass `--labels`, so a pod left
behind after a dropped session can be found with `kubectl get pods -l run=tmp`.
`-t` requires `-i`.

## Reattach to a pod started with -it
```bash
kubectl run sh --image=alpine:3.20 -it --restart=Never -- sh   # then Ctrl-P Ctrl-Q to detach
kubectl attach sh -c sh -i -t
```
By default stdin is closed after the first attach completes unless you pass
`--leave-stdin-open`.

## Gotchas
- `Unable to use a TTY - container <name> did not allocate one`: the container lacks `tty: true`.
- Attach shows nothing for apps that log to files; use `kubectl exec ... tail -f`.
- Pod Security admission in restricted namespaces can reject a default busybox run; supply a
  compliant securityContext with `--overrides` or use an allowed namespace.

## Checked
Date: 2026-10-27. Documentation: kubectl `run.go` and `attach.go` source on Kubernetes main
(latest release v1.37.1), whose flag help is the source of the generated reference pages.
Confirmed: `--rm` condition, `--restart` default `Always`, default `run=<name>` label,
`--detach-keys` default `ctrl-p,ctrl-q` on run, TTY error text, `--leave-stdin-open`,
`-t` needs `-i`. Removed the unconfirmed `--field-selector` lookup and the "logs -f" comparison.
Method: documentation only; no commands were run.
