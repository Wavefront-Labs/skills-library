---
id: computing-software.cloud-infrastructure-engineering.kubernetes.containercannotrun-start-errors
name: containercannotrun-start-errors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshoot-pods, containercannotrun, starterror, runcontainererror, exec-format-error]
level: practitioner
status: docs-checked
description: "Diagnose containers that fail at start (RunContainerError, ContainerCannotRun): read the runtime message, then check command/args, user, root filesystem and workingDir."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/", "https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/", "https://github.com/kubernetes/kubernetes/blob/v1.37.1/pkg/kubelet/container/sync_result.go", "https://kubernetes.io/docs/concepts/containers/images/#multi-architecture-images-with-image-indexes", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ContainerCannotRun and start errors

The image pulled, but the runtime could not start the process. The kubelet reports a waiting
reason `RunContainerError` when the runtime fails to start a container, and runtimes can record
terminated reasons such as `ContainerCannotRun`. The message is what matters:
```bash
kubectl get pod <p> -o jsonpath='{range .status.containerStatuses[*]}{.name}: {.lastState.terminated.reason} {.lastState.terminated.message}{.state.waiting.message}{"\n"}{end}'
```

## Typical causes
The runtime's message names the exact problem; these are the Kubernetes-side settings to check first.
| Area | What to check |
|---|---|
| Entrypoint | the pod `command` corresponds to the image ENTRYPOINT and `args` to CMD; a wrong `command` or a path missing from the image fails at start |
| User and permissions | `securityContext.runAsUser` and the file mode of the entrypoint inside the image |
| Root filesystem | with `readOnlyRootFilesystem: true`, an app that writes to its own directory needs an `emptyDir` volume mounted there |
| Working directory | `workingDir` in the container spec |
| Architecture | the image must provide a variant for the node's CPU architecture |

## Reproduce
Copy the pod with a shell instead of the entrypoint and run the original command by hand:
```bash
kubectl debug <p> -it --copy-to=<p>-dbg --container=<container> -- sh
```

## Verify
Container status shows `Running` with `restartCount` steady.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- `RunContainerError` is the kubelet error returned when the runtime failed to start a container, and the kubelet code
  refers to the terminated reason `ContainerCannotRun`: v1.37.1 `sync_result.go` and `kuberuntime_container.go`.
- `command` corresponds to ENTRYPOINT and `args` to CMD: define-command-argument-container page.
- Image indexes carry architecture-specific images: container images page. Container spec fields `workingDir`,
  `securityContext.runAsUser` and `readOnlyRootFilesystem` are API fields; the behaviour of a failing start is runtime-reported.
- `kubectl debug --copy-to --container <name> -- sh` copies a pod with a shell command: debug-running-pod page.
- Removed: the `StartError` reason, the quoted runtime error strings and their cause mapping, the CRLF and architecture
  explanations, and the `docker` and `crane` commands, none of which the checked sources document.

Method: documentation only; no commands were run.
