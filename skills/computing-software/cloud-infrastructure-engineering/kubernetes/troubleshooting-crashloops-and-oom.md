---
id: computing-software.cloud-infrastructure-engineering.kubernetes.troubleshooting-crashloops-and-oom
name: troubleshooting-crashloops-and-oom
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, crashloopbackoff, oomkilled, exit-code-137, exit-code-139, exit-code-143, exit-code-1, sigkill, sigterm, segfault, cgroup-v2, memory-working-set, rss, page-cache, eviction, memorypressure, kubectl-logs-previous, kubectl-debug, ephemeral-containers, createcontainerconfigerror, imagepullbackoff, runcontainererror, jvm-heap, gomemlimit, node-oom, dmesg, troubleshooting, incident-response]
level: practitioner
status: docs-checked
description: "Diagnose CrashLoopBackOff and OOMKilled pods: read exit codes and Last State, tell cgroup OOM from eviction, get a shell into a dying container, size memory for JVM/Go/Node."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy", "https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/", "https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/", "https://go.dev/doc/gc-guide", "https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting CrashLoopBackOff and OOM — from symptom to root cause

**Goal:** within ten minutes, know *why* the container died (app error, kill signal, memory,
config, probe) and have the evidence. Probe and request design themselves are in
`computing-software.cloud-infrastructure-engineering.kubernetes.deployments-services-and-probes`.

## 1. CrashLoopBackOff is a symptom, not a cause
It means "the container keeps exiting and kubelet is backing off restarts" — delay starts at
10 s and doubles to a 300 s (5 min) cap, resetting after 10 min of running cleanly. The alpha
`ReduceDefaultCrashLoopBackOffDecay` gate (off by default) lowers those defaults, and
`KubeletCrashLoopBackOffMax` (beta, on by default since v1.35) lets a node set a maximum between
1s and 300s. First, collect:
```bash
kubectl get pod <POD> -o jsonpath='{range .status.containerStatuses[*]}{.name}{" "}{.restartCount}{" "}{.lastState.terminated.reason}{" "}{.lastState.terminated.exitCode}{"\n"}{end}'
kubectl logs <POD> -c <CONTAINER> --previous --tail=200
kubectl describe pod <POD>     # Last State, Events: probe failures, Killing, BackOff
kubectl get events -n <NS> --sort-by=.lastTimestamp | tail -30
```

## 2. Read the exit code
| Exit / reason | Meaning | Next step |
|---|---|---|
| `Completed`, 0 | process exited normally | it is a batch job in a Deployment, or the entrypoint backgrounds itself |
| 1, 2 (`Error`) | app error | `--previous` logs; usually config, missing env, failed dependency at boot |
| 126 / 127 | not executable / not found | wrong `command`, missing binary in distroless, CRLF shebang |
| 137 + `OOMKilled` | cgroup memory limit hit, SIGKILL | §3 |
| 137 without OOMKilled | SIGKILL from kubelet: liveness failure or grace period exceeded | describe Events for `Liveness probe failed` |
| 139 | SIGSEGV | native crash; architecture mismatch (amd64 image on arm64), bad native lib |
| 143 | SIGTERM, exited on shutdown | normal during rollouts; abnormal if repeated → liveness or eviction |

When the entrypoint runs under a shell, exit status 128+N means the process died on signal N, and
126 / 127 mean found-but-not-executable / not found (bash documentation).

Non-running states that are *not* crashloops: `CreateContainerConfigError` (missing
ConfigMap/Secret key), `ImagePullBackOff`/`ErrImagePull` (tag, auth, rate limit — read the
event text), `RunContainerError` (the runtime failed to start the container),
`Init:CrashLoopBackOff` (check the init container's logs with `-c <INIT>`).

## 3. Three different "out of memory" events
1. **Container OOMKilled** — the container's cgroup exceeded its `limits.memory`; the
   kernel kills a process inside it. Reason `OOMKilled`, exit 137. Only that container restarts.
2. **Node-pressure eviction** — kubelet sees node memory below the eviction threshold and
   evicts whole pods, those using more than their requests first. Pod status
   `Failed`, reason `Evicted`; the controller creates a new pod elsewhere.
3. **Node-level kernel OOM** — the node itself ran out before kubelet acted; random
   processes die, possibly kubelet. Check `journalctl -k | grep -i oom` / `dmesg` on the node.

What gets measured: for node-pressure eviction the kubelet derives `memory.available` from the
**working set** (usage minus inactive file cache), not RSS. Active page cache still counts, so
apps doing heavy file I/O can look larger than their heap.

## 4. Fixing memory
- Graph `container_memory_working_set_bytes` against the limit over days: a sawtooth that
  hits the limit = undersized; a steady climb = leak.
- **JVM**: heap is not total memory. Use `-XX:MaxRAMPercentage` and budget metaspace, thread
  stacks and direct buffers. Native memory tracking: `-XX:NativeMemoryTracking=summary`
  (see the `java` command documentation).
- **Go**: set `GOMEMLIMIT` with 5-10% headroom below the container limit (Go GC guide) so the GC
  works harder before the kernel kills.
- **Node.js**: `--max-old-space-size` (MiB) below the container limit.
- Raising the limit is a valid fix only once you have shown usage is legitimate.

## 5. Getting inside a dying or shell-less container
```bash
kubectl debug -it <POD> --image=busybox:1.36 --target=<CONTAINER>       # ephemeral, shares PID ns
kubectl debug <POD> -it --copy-to=<POD>-dbg --container=<CONTAINER> -- sh   # copy with a shell instead of the entrypoint
kubectl debug node/<NODE> -it --image=ubuntu                            # host at /host
```
- For a container that crashes instantly, `--copy-to` with a shell or a long-running command lets
  you inspect config and run the entrypoint by hand.
- `--target` must be supported by the container runtime; otherwise the ephemeral container may
  not start or may get an isolated process namespace.

## Gotchas
- `--previous` logs exist only for the last terminated instance; ship logs centrally or
  you lose earlier crashes.
- A liveness probe killing a slow-booting app looks exactly like a crash — exit 137, no
  OOMKilled. Check Events before touching memory.
- A Job pod template accepts only `restartPolicy` `Never` or `OnFailure`.
- Sidecar crash (mesh proxy) can make the app look broken; check every container's status.

## Verify
- [ ] Root cause recorded with exit code, reason and the log line or metric that proves it.
- [ ] Fix deployed and `restartCount` stops increasing over at least one traffic peak.
- [ ] Memory working set peaks comfortably below the limit under load test.
- [ ] Alerts exist on `kube_pod_container_status_restarts_total` increase and on OOMKilled reason.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Restart backoff 10s doubling to 300s, reset after 10 minutes; `ReduceDefaultCrashLoopBackOffDecay` alpha (v1.33) and
  `KubeletCrashLoopBackOffMax` beta default-on (v1.35): pod-lifecycle page and v1.37.1 `kube_features.go`.
- `OOMKilled` reason with exit code 137: assign-memory-resource and manage-resources-containers pages.
- Eviction ordering (usage above requests first) and `memory.available` derived from the working set excluding inactive file
  cache: node-pressure eviction page.
- `kubectl debug` ephemeral, `--copy-to --container` and node forms, and `--target` runtime support note: debug-running-pod page.
- Job `restartPolicy` limited to `Never` or `OnFailure`: Job page.
- 128+N, 126 and 127: bash Exit Status manual; `GOMEMLIMIT` headroom 5-10%: Go GC guide.
- Removed: JVM percentage range and thread stack size, the Node.js container-awareness remark, Python worker advice, the
  `backoffLimit` remark, the 80-85% working-set target and the seccomp/mount causes of `RunContainerError`, which no checked
  source covers.

Method: documentation only; no commands were run.
